from telegram import Update
from telegram.ext import ContextTypes
from database.manager import db_manager
from config.settings import config

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员广播消息"""
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("❌ 权限不足")
        return
    
    if not context.args:
        await update.message.reply_text("用法: /broadcast 消息内容")
        return
    
    message = ' '.join(context.args)
    session = db_manager.Session()
    
    try:
        users = session.query(User).filter_by(is_active=True).all()
        sent_count = 0
        
        for user in users:
            try:
                await context.bot.send_message(
                    user.telegram_id,
                    f"📢 系统公告:\n\n{message}"
                )
                sent_count += 1
            except Exception:
                continue  # 无法发送给某些用户
        
        await update.message.reply_text(f"✅ 广播发送完成，成功发送给 {sent_count}/{len(users)} 用户")
    finally:
        session.close()

async def admin_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """用户统计"""
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("❌ 权限不足")
        return
    
    session = db_manager.Session()
    try:
        from sqlalchemy import func
        
        total_users = session.query(User).count()
        active_users = session.query(User).filter_by(is_active=True).count()
        
        membership_stats = session.query(
            User.membership_level,
            func.count(User.id)
        ).group_by(User.membership_level).all()
        
        stats_text = "📊 **用户统计**\n\n"
        stats_text += f"👥 总用户数: {total_users}\n"
        stats_text += f"✅ 活跃用户: {active_users}\n\n"
        stats_text += "💎 会员分布:\n"
        
        for level, count in membership_stats:
            stats_text += f"• {level.upper()}: {count} 用户\n"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    finally:
        session.close()
