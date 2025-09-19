"""
Real Gold Price API - Multiple reliable sources for live XAUUSD data
Uses free APIs that actually work for real-time gold prices
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Optional

class RealGoldPriceAPI:
    """
    Reliable real-time gold price fetcher using multiple free APIs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        
    def get_live_gold_price(self) -> Optional[Dict]:
        """
        Get live gold price from the best available free API
        
        Returns:
            Dict with current gold price and details
        """
        # Try multiple working APIs in order of reliability
        apis = [
            self._get_metals_live_price,
            self._get_goldapi_price, 
            self._get_fcsapi_price,
            self._get_currencyapi_price,
            self._get_exchangerate_price
        ]
        
        for api_func in apis:
            try:
                result = api_func()
                if result and result.get('price', 0) > 2000:  # Sanity check for gold price
                    print(f"✅ Got real gold price: ${result['price']:.2f} from {result['source']}")
                    return result
            except Exception as e:
                print(f"⚠️ API error: {e}")
                continue
        
        print("❌ All real APIs failed")
        return None
    
    def _get_metals_live_price(self) -> Optional[Dict]:
        """Get gold price from metals-api.com"""
        try:
            # Metals API - sometimes has free tier
            url = "https://api.metals.live/v1/spot/gold"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    return {
                        'price': float(data['price']),
                        'currency': 'USD',
                        'timestamp': datetime.now(),
                        'source': 'Metals.live API',
                        'high': float(data.get('high', data['price'])),
                        'low': float(data.get('low', data['price'])),
                        'change': float(data.get('change', 0))
                    }
        except:
            pass
        return None
    
    def _get_goldapi_price(self) -> Optional[Dict]:
        """Get gold price from goldapi.io"""
        try:
            # Gold API - free tier available
            url = "https://www.goldapi.io/api/XAU/USD"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    return {
                        'price': float(data['price']),
                        'currency': 'USD',
                        'timestamp': datetime.now(),
                        'source': 'GoldAPI.io',
                        'high': float(data.get('high_price', data['price'])),
                        'low': float(data.get('low_price', data['price'])),
                        'change': float(data.get('ch', 0))
                    }
        except:
            pass
        return None
    
    def _get_fcsapi_price(self) -> Optional[Dict]:
        """Get gold price from fcsapi.com"""
        try:
            # FCS API - has free tier
            url = "https://fcsapi.com/api-v3/forex/latest?symbol=XAU/USD&access_key=demo"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and data['response']:
                    price_data = data['response'][0]
                    return {
                        'price': float(price_data['c']),  # Current price
                        'currency': 'USD',
                        'timestamp': datetime.now(),
                        'source': 'FCS API',
                        'high': float(price_data.get('h', price_data['c'])),
                        'low': float(price_data.get('l', price_data['c'])),
                        'change': float(price_data.get('ch', 0))
                    }
        except:
            pass
        return None
    
    def _get_currencyapi_price(self) -> Optional[Dict]:
        """Get gold price from currencyapi.com"""
        try:
            # Currency API - free tier
            url = "https://api.currencyapi.com/v3/latest?apikey=cur_live_demo&currencies=XAU&base_currency=USD"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'XAU' in data['data']:
                    xau_data = data['data']['XAU']
                    # Convert from USD/XAU to XAU/USD
                    price = 1.0 / float(xau_data['value']) if xau_data['value'] > 0 else 0
                    
                    if price > 2000:  # Sanity check
                        return {
                            'price': price,
                            'currency': 'USD',
                            'timestamp': datetime.now(),
                            'source': 'CurrencyAPI.com',
                            'high': price,
                            'low': price,
                            'change': 0
                        }
        except:
            pass
        return None
    
    def _get_exchangerate_price(self) -> Optional[Dict]:
        """Get gold price from exchangerate-api.com"""
        try:
            # Exchange Rate API - free tier
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'rates' in data:
                    # Look for gold-related rates
                    for rate_key in ['XAU', 'GOLD']:
                        if rate_key in data['rates']:
                            rate = float(data['rates'][rate_key])
                            price = 1.0 / rate if rate > 0 else 0
                            
                            if 2000 < price < 5000:  # Gold price range check
                                return {
                                    'price': price,
                                    'currency': 'USD', 
                                    'timestamp': datetime.now(),
                                    'source': 'ExchangeRate API',
                                    'high': price,
                                    'low': price,
                                    'change': 0
                                }
        except:
            pass
        return None

# Test the API
if __name__ == "__main__":
    api = RealGoldPriceAPI()
    
    print("🥇 Testing Real Gold Price APIs")
    print("=" * 50)
    
    for i in range(3):
        price_data = api.get_live_gold_price()
        
        if price_data:
            print(f"✅ Real Gold Price: ${price_data['price']:,.2f}")
            print(f"📡 Source: {price_data['source']}")
            print(f"🕐 Time: {price_data['timestamp']}")
            
            if price_data.get('change'):
                print(f"📈 Change: {price_data['change']:+.2f}")
            
            print("-" * 30)
        else:
            print(f"❌ Attempt {i+1}: No real data available")
        
        if i < 2:
            time.sleep(2)
    
    print("🎯 Test complete!")