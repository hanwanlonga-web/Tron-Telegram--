import secrets
from datetime import datetime, timedelta
from database.manager import db_manager
from config.settings import config

class PaymentService:
    """支付服务"""
    
    def generate_payment_address(self, telegram_id: int, membership_level: str) -> Dict[str, Any]:
        """生成支付地址和信息"""
        amount = config.PAYMENT_AMOUNTS.get(membership_level, 0)
        if amount == 0:
            return {'success': False, 'error': '无效的会员等级'}
        
        # 创建支付记录
        payment = db_manager.create_payment(telegram_id, amount, membership_level)
        
        return {
            'success': True,
            'payment_id': payment.id,
            'amount': amount,
            'address': config.PAYMENT_WALLET,
            'membership_level': membership_level,
            'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
    
    def verify_payment(self, payment_id: int, tx_hash: str) -> Dict[str, Any]:
        """验证支付（简化版，实际需要连接节点验证）"""
        # 这里应该连接Tron节点验证交易
        # 简化实现：假设交易存在并确认
        try:
            success = db_manager.confirm_payment(tx_hash)
            return {
                'success': success,
                'message': '支付验证成功' if success else '支付验证失败'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

payment_service = PaymentService()
