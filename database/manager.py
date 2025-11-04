from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import config
from .models import Base, User, Payment, TransactionMonitor, PriceAlert

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_user(self, telegram_id: int) -> User:
        """获取用户，如果不存在则创建"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                session.commit()
            return user
        finally:
            session.close()
    
    def update_user_query_count(self, telegram_id: int) -> bool:
        """更新用户查询次数，返回是否允许查询"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                return False
            
            # 重置每日查询计数
            if user.last_query_date.date() != datetime.utcnow().date():
                user.query_count = 0
                user.last_query_date = datetime.utcnow()
            
            # 检查查询限制
            max_queries = self.get_user_max_queries(user.membership_level)
            if user.query_count >= max_queries:
                return False
            
            user.query_count += 1
            session.commit()
            return True
        finally:
            session.close()
    
    def get_user_max_queries(self, membership_level: str) -> int:
        """获取用户最大查询次数"""
        limits = {
            'free': config.FREE_USER_QUERIES_PER_DAY,
            'basic': config.BASIC_USER_QUERIES_PER_DAY,
            'premium': config.PREMIUM_USER_QUERIES_PER_DAY,
            'vip': config.VIP_USER_QUERIES_PER_DAY
        }
        return limits.get(membership_level, config.FREE_USER_QUERIES_PER_DAY)
    
    def create_payment(self, telegram_id: int, amount: float, membership_level: str) -> Payment:
        """创建支付记录"""
        session = self.Session()
        try:
            payment = Payment(
                telegram_id=telegram_id,
                amount=amount,
                membership_level=membership_level
            )
            session.add(payment)
            session.commit()
            return payment
        finally:
            session.close()
    
    def confirm_payment(self, tx_hash: str) -> bool:
        """确认支付"""
        session = self.Session()
        try:
            payment = session.query(Payment).filter_by(tx_hash=tx_hash).first()
            if payment and payment.status == 'pending':
                payment.status = 'confirmed'
                payment.confirmed_at = datetime.utcnow()
                
                # 更新用户会员等级
                user = session.query(User).filter_by(telegram_id=payment.telegram_id).first()
                if user:
                    user.membership_level = payment.membership_level
                
                session.commit()
                return True
            return False
        finally:
            session.close()

db_manager = DatabaseManager()
