import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """配置类"""
    # Telegram Bot配置
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Tron API配置
    TRON_API_KEY = os.getenv('TRON_API_KEY', '')
    TRON_API_BASE_URL = os.getenv('TRON_API_BASE_URL', 'https://api.trongrid.io')
    
    # 价格API配置
    COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY', '')
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tron_bot.db')
    
    # 支付配置
    PAYMENT_WALLET = os.getenv('PAYMENT_WALLET', '你的收款钱包地址')
    PAYMENT_AMOUNTS = {
        'basic': 100,      # 基础会员 100 TRX
        'premium': 500,    # 高级会员 500 TRX
        'vip': 1000        # VIP会员 1000 TRX
    }
    
    # 管理员配置
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]
    
    # 功能限制
    FREE_USER_QUERIES_PER_DAY = 10
    BASIC_USER_QUERIES_PER_DAY = 50
    PREMIUM_USER_QUERIES_PER_DAY = 200
    VIP_USER_QUERIES_PER_DAY = 1000
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN 环境变量未设置")

config = Config()
