import requests
from typing import Dict, Any, List
from config.settings import config

class PriceClient:
    """价格查询客户端"""
    
    def __init__(self):
        self.coingecko_url = config.COINGECKO_API_URL
    
    def get_trx_price(self) -> Dict[str, Any]:
        """获取TRX价格"""
        try:
            url = f"{self.coingecko_url}/simple/price"
            params = {
                'ids': 'tron',
                'vs_currencies': 'usd,eur,cny',
                'include_24hr_change': 'true',
                'include_market_cap': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            return {
                'success': True,
                'data': {
                    'usd': data['tron']['usd'],
                    'eur': data['tron']['eur'],
                    'cny': data['tron']['cny'],
                    'change_24h': data['tron']['usd_24h_change'],
                    'market_cap': data['tron']['usd_market_cap']
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Any]:
        """获取多个币种价格"""
        try:
            # 将符号映射到CoinGecko ID
            coin_ids = {
                'trx': 'tron',
                'btc': 'bitcoin',
                'eth': 'ethereum',
                'usdt': 'tether'
            }
            
            ids = [coin_ids.get(symbol.lower()) for symbol in symbols if symbol.lower() in coin_ids]
            ids = [id for id in ids if id]  # 移除None值
            
            url = f"{self.coingecko_url}/simple/price"
            params = {
                'ids': ','.join(ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

price_client = PriceClient()
