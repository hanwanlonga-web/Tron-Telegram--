from telegram import Update
from telegram.ext import ContextTypes
from database.manager import db_manager
from services.payment import payment_service
from tron.price_client import price_client
from utils.formatters import *
from bot.keyboards import *

# 在原有导入基础上添加新的导入...

async def membership_center(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """会员中心"""
    user = db_manager.get_user(update.effective_user.id)
    
    membership_info = f"""
👤 **会员中心**

🆔 **用户ID**: `{user.telegram_id}`
📊 **会员等级**: {user.membership_level.upper()}
🔢 **今日查询**: {user.query_count}/{db_manager.get_user_max_queries(user.membership_level)}
📅 **注册时间**: {user.created_at.strftime('%Y-%m-%d %H:%M')}

💎 **会员特权**:
• 🆓 免费会员: {db_manager.get_user_max_queries('free')} 次/天
• 🥉 基础会员: {db_manager.get_user_max_queries('basic')} 次/天
• 🥈 高级会员: {db_manager.get_user_max_queries('premium')} 次/天  
• 🥇 VIP会员: {db_manager.get_user_max_queries('vip')} 次/天

💡 升级会员享受更多查询次数和高级功能！
    """.strip()
    
    await update.message.reply_text(
        membership_info,
        reply_markup=get_membership_keyboard(),
        parse_mode='Markdown'
    )

async def handle_payment_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理支付选择"""
    await update.message.reply_text(
        "💎 **选择会员套餐**\n\n"
        "🥉 基础会员 - 100 TRX\n"
        "• 50次每日查询\n"
        "• 基础价格提醒\n\n"
        "🥈 高级会员 - 500 TRX\n"  
        "• 200次每日查询\n"
        "• 高级价格提醒\n"
        "• 交易监控\n\n"
        "🥇 VIP会员 - 1000 TRX\n"
        "• 1000次每日查询\n"
        "• 所有高级功能\n"
        "• 优先技术支持",
        reply_markup=get_payment_keyboard(),
        parse_mode='Markdown'
    )

async def handle_price_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理价格查询"""
    price_data = price_client.get_trx_price()
    
    if not price_data['success']:
        await update.message.reply_text("❌ 获取价格数据失败，请稍后重试")
        return
    
    data = price_data['data']
    
    price_info = f"""
💰 **TRX 实时价格**

🇺🇸 **美元**: ${data['usd']:.4f}
🇪🇺 **欧元**: €{data['eur']:.4f}  
🇨🇳 **人民币**: ¥{data['cny']:.4f}
📊 **24H涨跌**: {data['change_24h']:+.2f}%
🏦 **市值**: ${data['market_cap']:,.0f}

⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """.strip()
    
    await update.message.reply_text(
        price_info,
        reply_markup=get_price_keyboard(),
        parse_mode='Markdown'
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员面板"""
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("❌ 权限不足")
        return
    
    # 获取系统统计
    session = db_manager.Session()
    try:
        total_users = session.query(User).count()
        active_users = session.query(User).filter_by(is_active=True).count()
        total_payments = session.query(Payment).count()
        confirmed_payments = session.query(Payment).filter_by(status='confirmed').count()
        
        stats_text = f"""
👨‍💼 **管理员面板**

👥 **用户统计**:
• 总用户数: {total_users}
• 活跃用户: {active_users}
• 付费用户: {confirmed_payments}

💰 **支付统计**:
• 总支付数: {total_payments}
• 成功支付: {confirmed_payments}
• 成功率: {confirmed_payments/total_payments*100:.1f}% if total_payments > 0 else 0

🔧 **管理功能**:
• 用户管理
• 支付审核  
• 系统通知
• 数据统计
        """.strip()
        
        await update.message.reply_text(
            stats_text,
            reply_markup=get_admin_keyboard(),
            parse_mode='Markdown'
        )
    finally:
        session.close()

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理回调查询（扩展）"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('payment:'):
        level = data.split(':')[1]
        if level == 'cancel':
            await query.edit_message_text("❌ 支付已取消")
            return
        
        user_id = query.from_user.id
        payment_info = payment_service.generate_payment_address(user_id, level)
        
        if payment_info['success']:
            response_text = f"""
💎 **支付信息 - {level.upper()}会员**

💰 **金额**: {payment_info['amount']} TRX
📍 **收款地址**: `{payment_info['address']}`
⏰ **有效期**: 1小时

📝 **支付说明**:
1. 向上述地址转账 {payment_info['amount']} TRX
2. 转账完成后，回复本对话提供交易哈希
3. 系统会自动验证并升级您的会员等级

💡 注意: 请确保转账金额准确，仅支持TRX主网转账
            """.strip()
            
            await query.edit_message_text(
                response_text,
                parse_mode='Markdown'
            )
            context.user_data['waiting_payment'] = payment_info['payment_id']
        else:
            await query.edit_message_text("❌ 生成支付信息失败")
    
    elif data.startswith('refresh_account:'):
        # 原有账户刷新逻辑...
        pass

# 添加新的文本消息处理
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理文本消息（扩展）"""
    text = update.message.text
    user_id = update.effective_user.id
    
    # 原有文本处理逻辑...
    
    # 新增功能处理
    if text == '👤 会员中心':
        await membership_center(update, context)
        
    elif text == '💰 价格查询':
        await update.message.reply_text(
            "选择价格查询选项:",
            reply_markup=get_price_keyboard()
        )
        
    elif text == '💳 会员充值':
        await handle_payment_selection(update, context)
        
    elif text == '📊 我的信息':
        await membership_center(update, context)
        
    elif text == '👨‍💼 管理员' and user_id in config.ADMIN_IDS:
        await admin_panel(update, context)
        
    elif text == '📈 TRX价格':
        await handle_price_query(update, context)
    
    # 处理支付交易哈希
    elif context.user_data.get('waiting_payment'):
        payment_id = context.user_data['waiting_payment']
        tx_hash = text.strip()
        
        if len(tx_hash) >= 64:  # 基本的交易哈希验证
            result = payment_service.verify_payment(payment_id, tx_hash)
            if result['success']:
                await update.message.reply_text(
                    "✅ 支付验证成功！您的会员等级已升级。",
                    reply_markup=get_main_keyboard()
                )
            else:
                await update.message.reply_text(
                    f"❌ 支付验证失败: {result.get('error', '未知错误')}"
                )
            context.user_data.pop('waiting_payment', None)
        else:
            await update.message.reply_text("❌ 无效的交易哈希格式")
    
    else:
        # 原有的等待输入处理...
        pass
