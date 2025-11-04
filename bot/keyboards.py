from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """主菜单键盘"""
    keyboard = [
        ['🔍 查询账户', '🔗 查询交易'],
        ['💰 价格查询', '📦 最新区块'],
        ['👤 会员中心', '⚡ 快速功能']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_membership_keyboard():
    """会员中心键盘"""
    keyboard = [
        ['💳 会员充值', '📊 我的信息'],
        ['🔔 交易监控', '💸 价格提醒'],
        ['📋 充值记录', '🔙 返回主菜单']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_payment_keyboard():
    """支付选择键盘"""
    keyboard = [
        [
            InlineKeyboardButton("🥉 基础会员 - 100 TRX", callback_data="payment:basic"),
            InlineKeyboardButton("🥈 高级会员 - 500 TRX", callback_data="payment:premium")
        ],
        [
            InlineKeyboardButton("🥇 VIP会员 - 1000 TRX", callback_data="payment:vip"),
            InlineKeyboardButton("❌ 取消", callback_data="payment:cancel")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """管理员键盘"""
    keyboard = [
        ['📊 系统统计', '👥 用户管理'],
        ['💰 支付管理', '🔔 发送通知'],
        ['🔙 返回主菜单']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_price_keyboard():
    """价格查询键盘"""
    keyboard = [
        ['📈 TRX价格', '💰 多币种价格'],
        ['🔔 设置提醒', '📊 价格图表'],
        ['🔙 返回主菜单']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
