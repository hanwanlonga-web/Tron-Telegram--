import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Bot

from config.settings import config
from bot.handlers import *
from bot.admin import admin_broadcast, admin_user_stats

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"配置错误: {e}")
        return
    
    # 创建应用
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("account", handle_account_query))
    application.add_handler(CommandHandler("transaction", handle_transaction_query))
    application.add_handler(CommandHandler("block", handle_block_query))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))
    application.add_handler(CommandHandler("stats", admin_user_stats))
    
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # 启动机器人
    logger.info("🤖 Tron查询机器人启动中...")
    application.run_polling()

if __name__ == '__main__':
    main()
