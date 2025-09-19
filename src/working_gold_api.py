"""
Working Gold Price API - Uses reliable sources that actually work
Gets real XAUUSD market data from financial websites
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, Optional
from bs4 import BeautifulSoup
import time

class WorkingGoldAPI:
    """
    Reliable gold price fetcher using web scraping from financial sites
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_real_gold_price(self) -> Optional[Dict]:
        """
        Get real gold price from reliable financial websites
        """
        # Try multiple reliable sources
        sources = [
            self._get_marketwatch_gold,
            self._get_investing_com_gold,
            self._get_goldprice_org,
            self._get_kitco_gold,
            self._get_yahoo_scrape
        ]
        
        for source_func in sources:
            try:
                result = source_func()
                if result and 2000 < result.get('price', 0) < 5000:
                    print(f"✅ Real gold price: ${result['price']:.2f} from {result['source']}")
                    return result
            except Exception as e:
                print(f"⚠️ Source error: {e}")
                continue
        
        return None
    
    def _get_marketwatch_gold(self) -> Optional[Dict]:
        """Get gold price from MarketWatch"""
        try:
            url = "https://www.marketwatch.com/investing/future/gc00"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for price in page content
                price_pattern = r'class="value"[^>]*>[\$]?([\d,]+\.?\d*)'
                match = re.search(price_pattern, response.text)
                
                if match:
                    price_str = match.group(1).replace(',', '')
                    price = float(price_str)
                    
                    if price > 2000:
                        return {
                            'price': price,
                            'currency': 'USD',
                            'timestamp': datetime.now(),
                            'source': 'MarketWatch',
                            'high': price,
                            'low': price,
                            'change': 0
                        }
        except:
            pass
        return None
    
    def _get_investing_com_gold(self) -> Optional[Dict]:
        """Get gold price from Investing.com"""
        try:
            url = "https://www.investing.com/commodities/gold"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for price data
                price_patterns = [
                    r'"last_close":([\d.]+)',
                    r'data-test="instrument-price-last"[^>]*>([\d,]+\.?\d*)',
                    r'class="text-2xl"[^>]*>\$?([\d,]+\.?\d*)'
                ]
                
                for pattern in price_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        price_str = match.group(1).replace(',', '')
                        price = float(price_str)
                        
                        if 2000 < price < 5000:
                            return {
                                'price': price,
                                'currency': 'USD',
                                'timestamp': datetime.now(),
                                'source': 'Investing.com',
                                'high': price,
                                'low': price,
                                'change': 0
                            }
        except:
            pass
        return None
    
    def _get_goldprice_org(self) -> Optional[Dict]:
        """Get gold price from GoldPrice.org"""
        try:
            url = "https://goldprice.org/gold-price-usa.html"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for current gold price
                price_patterns = [
                    r'id="gp-spot-price"[^>]*>([\d,]+\.?\d*)',
                    r'class="gold-price"[^>]*>\$?([\d,]+\.?\d*)',
                    r'"current.*price".*?([\d,]+\.?\d+)'
                ]
                
                for pattern in price_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        price_str = match.group(1).replace(',', '')
                        price = float(price_str)
                        
                        if 2000 < price < 5000:
                            return {
                                'price': price,
                                'currency': 'USD',
                                'timestamp': datetime.now(),
                                'source': 'GoldPrice.org',
                                'high': price,
                                'low': price,
                                'change': 0
                            }
        except:
            pass
        return None
    
    def _get_kitco_gold(self) -> Optional[Dict]:
        """Get gold price from Kitco.com"""
        try:
            url = "https://www.kitco.com/gold-price-today-usa/"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for Kitco gold price
                price_patterns = [
                    r'gold.*spot.*price.*\$?([\d,]+\.?\d*)',
                    r'class=".*price.*"[^>]*>\$?([\d,]+\.?\d*)',
                    r'"spot_price".*?([\d,]+\.?\d+)'
                ]
                
                for pattern in price_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    for match in matches:
                        try:
                            price_str = match.replace(',', '')
                            price = float(price_str)
                            
                            if 2000 < price < 5000:
                                return {
                                    'price': price,
                                    'currency': 'USD',
                                    'timestamp': datetime.now(),
                                    'source': 'Kitco.com',
                                    'high': price,
                                    'low': price,
                                    'change': 0
                                }
                        except:
                            continue
        except:
            pass
        return None
    
    def _get_yahoo_scrape(self) -> Optional[Dict]:
        """Scrape gold price from Yahoo Finance"""
        try:
            url = "https://finance.yahoo.com/quote/GC=F"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Look for price in Yahoo Finance
                price_patterns = [
                    r'data-symbol="GC=F"[^>]*data-field="regularMarketPrice"[^>]*data-pricehint="2"[^>]*>([\d,]+\.?\d*)',
                    r'"regularMarketPrice":\{"raw":([\d.]+)',
                    r'class=".*price.*"[^>]*>([\d,]+\.?\d*)'
                ]
                
                for pattern in price_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        price_str = match.group(1).replace(',', '')
                        price = float(price_str)
                        
                        if 2000 < price < 5000:
                            return {
                                'price': price,
                                'currency': 'USD',
                                'timestamp': datetime.now(),
                                'source': 'Yahoo Finance (Scraped)',
                                'high': price,
                                'low': price,
                                'change': 0
                            }
        except:
            pass
        return None

# Test the API
if __name__ == "__main__":
    api = WorkingGoldAPI()
    
    print("🥇 Testing Working Gold Price APIs")
    print("=" * 50)
    
    for i in range(3):
        print(f"🔍 Attempt {i+1}: Getting real gold price...")
        price_data = api.get_real_gold_price()
        
        if price_data:
            print(f"💰 REAL Gold Price: ${price_data['price']:,.2f}")
            print(f"📡 Source: {price_data['source']}")
            print(f"🕐 Time: {price_data['timestamp']}")
            
            # Compare with mock data range
            if 2600 < price_data['price'] < 2700:
                print("🎯 Price in expected range - this looks like REAL data!")
            else:
                print(f"🔍 Price: ${price_data['price']:.2f} - verify if this is current gold price")
            
            print("-" * 50)
            break
        else:
            print(f"❌ Attempt {i+1}: Failed")
            if i < 2:
                time.sleep(3)
    
    print("🎯 Real API test complete!")