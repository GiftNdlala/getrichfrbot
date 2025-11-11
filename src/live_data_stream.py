"""
Live Data Streaming Module for XAUUSD Trading Signals
Fetches real-time price data and generates live trading signals
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable, List
import json
import os
from dataclasses import dataclass, asdict

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(__file__))

from indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from .config import get_config
try:
    from .mt5_connector import MT5Connector
except ImportError:
    MT5Connector = None
try:
    from .persistence import PersistenceManager
except ImportError:
    PersistenceManager = None
try:
    from .executor import AutoTrader
except ImportError:
    AutoTrader = None
try:
    from .order_manager import OrderManager, CampaignManager
except ImportError:
    OrderManager = None
    CampaignManager = None
try:
    from .event_engine import EventEngine
except ImportError:
    EventEngine = None

from .strategies import (
    NYUPIPStrategy,
    NYUPIPSignal,
    ICTSwingPointsStrategy,
    ICTSwingSignal,
    ICTATMStrategy,
    ICTATMSignal,
)

# Import WORKING real gold API for actual market data
try:
    from simple_real_gold import SimpleRealGold
except ImportError:
    try:
        from .simple_real_gold import SimpleRealGold
    except ImportError:
        SimpleRealGold = None

# Keep working gold API as backup
try:
    from working_gold_api import WorkingGoldAPI
except ImportError:
    try:
        from .working_gold_api import WorkingGoldAPI
    except ImportError:
        WorkingGoldAPI = None
# Remove the conflicting import
# from robust_data_source import RobustXAUUSDDataSource

@dataclass
class LiveSignal:
    """Data class for live trading signals with risk management and alert categorization"""
    timestamp: str
    symbol: str
    current_price: float
    signal: int  # -1: SELL, 0: HOLD, 1: BUY
    signal_type: str  # "BUY", "SELL", "HOLD"
    confidence: float
    rsi: float
    macd: float
    macd_signal: float
    sma_20: float
    sma_50: float
    price_change: float
    price_change_pct: float
    
    # Signal Alert Category System
    alert_level: str  # "HIGH", "MEDIUM", "LOW", "HOLD"
    alert_color: str  # Color code for UI
    target_pips: int  # Target pips for this signal category
    success_rate: float  # Expected success rate percentage
    
    # Risk Management Details
    entry_price: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_3: float
    risk_reward_ratio: float
    atr_value: float
    position_size_percent: float
    risk_amount_dollars: float
    potential_profit_tp1: float
    potential_profit_tp2: float
    potential_profit_tp3: float

class LiveDataStream:
    """
    Real-time data streaming and signal generation for XAUUSD
    """
    
    @staticmethod
    def _coerce_positive_int(value, default: int, minimum: Optional[int] = None, maximum: Optional[int] = None) -> int:
        """Convert arbitrary input to a positive integer with safety guards."""
        try:
            ivalue = int(value)
            if ivalue <= 0:
                raise ValueError
        except Exception:
            ivalue = int(default)
        if minimum is not None:
            ivalue = max(ivalue, int(minimum))
        if maximum is not None:
            ivalue = min(ivalue, int(maximum))
        return ivalue

    def __init__(self, symbol: str = "XAUUSD", update_interval: int = 30):
        """
        Initialize live data streaming
        
        Args:
            symbol (str): Symbol for Gold (XAUUSD)
            update_interval (int): Update interval in seconds
        """
        self.symbol = symbol  # XAUUSD for Gold
        self.update_interval = update_interval
        self.indicators = TechnicalIndicators()
        self.signal_generator = SignalGenerator()
        
        # Config
        self.config = get_config()

        # Resolve data mapping once for transparency/debug
        try:
            self.yf_symbol = self._map_symbol_to_yfinance()
            feeds = self.config.get('data_feed', {})
            primary = feeds.get('primary', 'MT5')
            backups = feeds.get('backups', [])
            print(f"✅ Stream init for {self.symbol} | primary={primary} | backups={backups} | yfinance={self.yf_symbol} | gold={self._is_gold_symbol()}")
        except Exception:
            self.yf_symbol = self.symbol

        # Initialize WORKING real gold API only for gold symbols
        self.simple_gold_api = SimpleRealGold() if (SimpleRealGold and self._is_gold_symbol()) else None
        if self.simple_gold_api:
            print("✅ WORKING Real Gold API initialized - getting ACTUAL $3,700+ market data")
        
        # Keep other gold APIs as backups (gold only)
        self.working_gold_api = WorkingGoldAPI() if (WorkingGoldAPI and self._is_gold_symbol()) else None
        
        try:
            from robust_data_source import RobustXAUUSDDataSource
            # This robust data source is gold-focused; use only for gold symbols
            self.data_source = RobustXAUUSDDataSource() if self._is_gold_symbol() else None
            if self.data_source:
                print("✅ Backup data sources available")
        except:
            self.data_source = None
        
        # MT5 primary connector (if available)
        self.mt5 = MT5Connector() if MT5Connector else None

        # Data storage
        self.current_data = pd.DataFrame()
        self.current_signal = None
        self.last_update = None
        self.is_running = False
        self.trading_enabled = False  # Default: OFF - user must enable manually
        self.persistence = PersistenceManager() if PersistenceManager else None
        self.autotrader = AutoTrader(symbol=self.symbol) if AutoTrader else None
        # Managers
        exec_cfg = self.config.get('execution', {})
        window_min = int(exec_cfg.get('campaign_window_minutes', 10))
        max_map = exec_cfg.get('campaign_max_trades', { 'LOW': 6, 'MEDIUM': 6, 'HIGH': 9 })
        min_spacing = int(exec_cfg.get('min_seconds_between_entries', 60))
        self.campaign = CampaignManager(window_minutes=window_min, max_per_level=max_map, min_spacing_seconds=min_spacing) if CampaignManager else None
        self.order_manager = OrderManager(self.symbol) if OrderManager else None
        # Session control override
        self.ignore_session_filter = False
        # Per-symbol event mode (manual toggle for now)
        self.event_mode_enabled = False
        # Farmer state
        self._farmer_last_cycle = None
        farmer_cfg = self.config.get('execution', {}).get('farmer', {})
        self.farmer_enabled = bool(farmer_cfg.get('enabled', False))
        self._farmer_default_enabled = self.farmer_enabled
        self.farmer_cycle_seconds = int(farmer_cfg.get('cycle_seconds', 120))
        # Engine toggles - Default: OFF - user must enable manually
        self.enable_low = False
        self.enable_medium = False
        self.enable_high = False
        # Event engine
        self.event_engine = EventEngine(self.symbol) if EventEngine else None
        # Ensure MT5 uses this stream's symbol and reinitialize if needed
        try:
            if self.mt5:
                self.mt5.symbol = self.symbol
                import MetaTrader5 as mt5
                mt5.symbol_select(self.symbol, True)
                # Re-initialize after symbol override so connector keeps it
                self.mt5.initialize()
        except Exception:
            pass
        # Global engine mode - Default: NONE - user must manually select a mode
        self.engine_mode = 'NONE'
        
        # Callbacks for signal updates
        self.signal_callbacks = []
        
        # History buffers (configurable)
        history_limits_cfg = self.config.get('data_feed', {}).get('history_limits', {})
        indicator_default = history_limits_cfg.get('indicator_m1', 400)
        nyupip_default = history_limits_cfg.get('nyupip_m1', 7200)
        self._history_limit_default = self._coerce_positive_int(indicator_default, 400, minimum=200)
        self._nyupip_history_limit = self._coerce_positive_int(nyupip_default, 7200, minimum=4800)

        # Historical data for indicators (need minimum 200 periods)
        self.historical_data = self._fetch_initial_data()
        base_cols = [col for col in ["Open", "High", "Low", "Close", "Volume"] if col in self.historical_data.columns]
        if base_cols:
            self.nyupip_history = self.historical_data[base_cols].copy()
        else:
            self.nyupip_history = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])

        # NYUPIP strategy integration
        tz_name = self.config.get('sessions', {}).get('timezone', 'UTC')

        self.nyupip_strategy = NYUPIPStrategy(symbol=self.symbol)
        self.nyupip_enabled = False
        self.nyupip_state: Dict[str, object] = {
            'enabled': False,
            'last_signal': None,
            'auto_last_ticket': None,
            'last_diagnostics': self.nyupip_strategy.get_last_diagnostics(),
        }

        self.ict_swing_strategy = (
            ICTSwingPointsStrategy(symbol=self.symbol, timezone=tz_name)
            if self._is_gold_symbol()
            else None
        )
        self.ict_atm_strategy = (
            ICTATMStrategy(symbol=self.symbol, timezone=tz_name)
            if self._is_gold_symbol()
            else None
        )

        self.ict_swing_enabled = False
        self.ict_atm_enabled = False
        self.ict_swing_state: Dict[str, object] = {
            'enabled': False,
            'last_signal': None,
            'last_diagnostics': None,
            'auto_last_ticket': None,
        }
        self.ict_atm_state: Dict[str, object] = {
            'enabled': False,
            'last_signal': None,
            'last_diagnostics': None,
            'auto_last_ticket': None,
        }
        
    def _is_gold_symbol(self) -> bool:
        try:
            s = (self.symbol or "").upper()
            return ("XAU" in s) or ("GOLD" in s)
        except Exception:
            return False

    def _map_symbol_to_yfinance(self) -> str:
        s = (self.symbol or "").upper()
        # Simple mappings for common CFD symbols
        if "US30" in s or s == "DJI" or s == "US30M":
            return "^DJI"
        if "XAU" in s or "GOLD" in s:
            return "GC=F"
        # Default: try the raw symbol
        return self.symbol

    def _yf_get_historical(self) -> pd.DataFrame:
        try:
            df = yf.download(tickers=self.yf_symbol, period="365d", interval="1d", progress=False)
            if df is None or df.empty:
                return pd.DataFrame()
            df = df.rename(columns={
                'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'
            })
            # Ensure expected columns
            df = df[['Open','High','Low','Close','Volume']]
            df.index.name = 'Date'
            return df
        except Exception:
            return pd.DataFrame()

    def _yf_get_current_quote(self) -> Optional[Dict]:
        try:
            df = yf.download(tickers=self.yf_symbol, period="2d", interval="1m", progress=False)
            if df is None or df.empty:
                return None
            last = df.tail(1)
            prev = df.tail(2).head(1)
            price = float(last['Close'].iloc[0])
            prev_close = float(prev['Close'].iloc[0]) if not prev.empty else price
            ts = last.index[-1].to_pydatetime()
            vol = float(last['Volume'].iloc[0]) if 'Volume' in last.columns else 0.0
            return {
                'price': price,
                'prev_close': prev_close,
                'timestamp': ts,
                'volume': vol,
                'source': f"YF-{self.yf_symbol}"
            }
        except Exception:
            return None

    def _resolve_path(self, path: str, ensure_dir: bool = False) -> Optional[str]:
        if not path:
            return None
        try:
            formatted = path.format(symbol=self.symbol)
        except Exception:
            formatted = path
        if os.path.isabs(formatted):
            resolved = formatted
        else:
            resolved = os.path.join(WORKSPACE_ROOT, formatted)
        if ensure_dir:
            directory = os.path.dirname(resolved)
            if directory:
                os.makedirs(directory, exist_ok=True)
        return resolved

    def _hydrate_from_csv(self, path: str, min_rows: int) -> Optional[pd.DataFrame]:
        resolved = self._resolve_path(path) if path else None
        if not resolved:
            return None
        if not os.path.exists(resolved):
            return None
        try:
            df = pd.read_csv(resolved)
            if df is None or df.empty:
                return None
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
            else:
                df.index = pd.to_datetime(df.index)
            rename_map = {
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume',
                'tick_volume': 'Volume',
            }
            for src, dst in rename_map.items():
                if src in df.columns and dst not in df.columns:
                    df.rename(columns={src: dst}, inplace=True)
            expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                print(f"⚠️ Cached history missing columns {missing}; ignoring {resolved}")
                return None
            df = df[expected_cols].copy()
            # Drop duplicate column labels if any (e.g., both tick_volume and real_volume mapped to Volume)
            if getattr(df.columns, "duplicated", None) is not None:
                df = df.loc[:, ~df.columns.duplicated(keep='last')]
            df.sort_index(inplace=True)
            df = df[~df.index.duplicated(keep='last')]
            if len(df) >= min_rows:
                print(f"📦 Hydrated {len(df)} rows for {self.symbol} from cache {resolved}")
            else:
                print(f"ℹ️ Cache {resolved} contains {len(df)} rows (< {min_rows}); will top up from live sources")
            return df
        except Exception as exc:
            print(f"⚠️ Failed to hydrate history from {resolved}: {exc}")
            return None

    def _write_history_csv(self, path: str, df: pd.DataFrame) -> None:
        if path is None or df is None or df.empty:
            return
        try:
            resolved = self._resolve_path(path, ensure_dir=True)
            export_df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            export_df = export_df.sort_index()
            export_df.to_csv(resolved, index_label='Date')
            print(f"💾 Cached {len(export_df)} rows for {self.symbol} to {resolved}")
        except Exception as exc:
            print(f"⚠️ Failed to cache history to {path}: {exc}")

    def _mt5_fetch_initial_history(self, count: int) -> pd.DataFrame:
        if not self.mt5:
            return pd.DataFrame()
        try:
            import MetaTrader5 as mt5
            count = self._coerce_positive_int(count, count, minimum=1000, maximum=50000)
            rates = self.mt5.get_rates(mt5.TIMEFRAME_M1, count)
            if rates is None or len(rates) == 0:
                return pd.DataFrame()
            df = pd.DataFrame(rates)
            if df.empty:
                return pd.DataFrame()
            if 'time' not in df.columns:
                return pd.DataFrame()
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.rename(columns={'time': 'Date', 'real_volume': 'Volume'}, inplace=True)
            df.set_index('Date', inplace=True)
            column_map = {
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'tick_volume': 'Volume'
            }
            df = df.rename(columns=column_map)
            expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df[[c for c in expected_cols if c in df.columns]]
            # Drop duplicate column labels if any after renames
            if getattr(df.columns, "duplicated", None) is not None:
                df = df.loc[:, ~df.columns.duplicated(keep='last')]
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                print(f"⚠️ MT5 history missing columns {missing}")
                return pd.DataFrame()
            df.sort_index(inplace=True)
            df = df[~df.index.duplicated(keep='last')]
            return df.tail(count)
        except Exception as exc:
            print(f"⚠️ MT5 history error: {exc}")
            return pd.DataFrame()

    def _merge_history_frames(self, frames: List[pd.DataFrame]) -> pd.DataFrame:
        merged = None
        for frame in frames:
            if frame is None or frame.empty:
                continue
            merged = frame if merged is None else pd.concat([merged, frame])
        if merged is None or merged.empty:
            return pd.DataFrame()
        merged.sort_index(inplace=True)
        # Ensure no duplicate column labels after merges
        if getattr(merged.columns, "duplicated", None) is not None:
            merged = merged.loc[:, ~merged.columns.duplicated(keep='last')]
        merged = merged[~merged.index.duplicated(keep='last')]
        if len(merged) > self._nyupip_history_limit:
            merged = merged.tail(self._nyupip_history_limit)
        return merged

    def _fetch_initial_data(self) -> pd.DataFrame:
        """Fetch initial historical data for indicator calculations"""
        try:
            print("📊 Fetching initial historical data...")
            feeds_cfg = self.config.get('data_feed', {})
            startup_cfg = feeds_cfg.get('startup_history', {})
            min_rows = self._coerce_positive_int(startup_cfg.get('min_rows'), 4800, minimum=1000)
            mt5_m1_bars = self._coerce_positive_int(startup_cfg.get('mt5_m1_bars'), self._nyupip_history_limit, minimum=min_rows)
            hydrate_path = startup_cfg.get('hydrate_csv')
            auto_cache = bool(startup_cfg.get('auto_cache', False))

            sources: List[str] = []
            frames: List[pd.DataFrame] = []

            cached_df = self._hydrate_from_csv(hydrate_path, min_rows) if hydrate_path else None
            if cached_df is not None and not cached_df.empty:
                frames.append(cached_df)
                sources.append(f"cache:{len(cached_df)}")

            needs_mt5 = (cached_df is None) or len(cached_df) < min_rows
            mt5_df = pd.DataFrame()
            if self.mt5 and needs_mt5:
                mt5_df = self._mt5_fetch_initial_history(mt5_m1_bars)
                if mt5_df is not None and not mt5_df.empty:
                    frames.append(mt5_df)
                    sources.append(f"MT5:{len(mt5_df)}")

            data = self._merge_history_frames(frames)

            if auto_cache and hydrate_path and mt5_df is not None and not mt5_df.empty:
                cache_payload = data if data is not None and not data.empty else mt5_df
                self._write_history_csv(hydrate_path, cache_payload)

            if data is None or data.empty or len(data) < min_rows:
                fallback_data = None
                if self.data_source is not None:
                    try:
                        fallback_data = self.data_source.get_historical_data(days=365)
                    except Exception as exc:
                        print(f"⚠️ Backup data source error: {exc}")
                        fallback_data = None
                if fallback_data is not None and not fallback_data.empty:
                    try:
                        fallback_data = fallback_data[["Open", "High", "Low", "Close", "Volume"]]
                    except Exception:
                        pass
                    data = fallback_data
                    source_label = getattr(self.data_source, 'data_source', 'DataSource')
                    sources.append(f"{source_label}:{len(fallback_data)}")

            if data is None or data.empty or len(data) < min_rows:
                backups = feeds_cfg.get('backups', [])
                if 'YF' in [b.upper() if isinstance(b, str) else b for b in backups]:
                    yf_data = self._yf_get_historical()
                    if yf_data is not None and not yf_data.empty:
                        data = yf_data
                        sources.append(f"YF:{len(yf_data)}")

            if data is None or data.empty:
                print("⚠️ No data received, using mock data")
                return self._generate_mock_data()

            data = data.sort_index()
            # Drop duplicate column labels defensively before indicators
            if getattr(data.columns, "duplicated", None) is not None:
                data = data.loc[:, ~data.columns.duplicated(keep='last')]
            data = data[~data.index.duplicated(keep='last')]

            if len(data) > self._nyupip_history_limit:
                data = data.tail(self._nyupip_history_limit)

            data = self.indicators.calculate_all_indicators(data)

            if len(data) < min_rows:
                print(f"⚠️ Startup history only has {len(data)} rows (< {min_rows}); NYUPIP will wait for additional bars")

            try:
                source_name = " + ".join(sources) if sources else 'unknown'
            except Exception:
                source_name = 'unknown'
            print(f"✅ Loaded {len(data)} historical data points from {source_name}")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching initial data: {e}")
            return self._generate_mock_data()
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """Generate mock historical data if real data fails"""
        print("🎭 Generating mock historical data...")
        
        # Generate 365 days of mock data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), 
                            end=datetime.now(), 
                            freq='D')
        
        # Start around typical gold price
        base_price = 2640.0
        prices = []
        
        for i in range(len(dates)):
            # Add some realistic price movement
            change = np.random.normal(0, 20)  # Gold typically moves $10-30/day
            base_price += change
            prices.append(base_price)
        
        data = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 15)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 15)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(50000, 200000, len(dates))
        }, index=dates)
        
        # Calculate indicators
        data = self.indicators.calculate_all_indicators(data)
        return data
    
    def _fetch_current_quote(self) -> Optional[Dict]:
        """Fetch current market quote from primary (MT5) with fallbacks"""
        # Primary: MT5
        if self.mt5:
            try:
                q = self.mt5.get_current_quote()
                if q and q.get('price', 0) > 0:
                    return q
            except Exception as e:
                print(f"⚠️ MT5 quote error: {e}")
        
        # Fallbacks based on symbol type
        if self._is_gold_symbol():
            # Fallback 1: Simple Real Gold API
            if self.simple_gold_api:
                try:
                    real_data = self.simple_gold_api.get_real_gold_price()
                    if real_data and real_data.get('price', 0) > 0:
                        print(f"✅ REAL MARKET DATA: ${real_data['price']:.2f} from {real_data['source']}")
                        
                        # Calculate realistic price change
                        if hasattr(self, 'last_real_price'):
                            prev_price = self.last_real_price
                        else:
                            prev_price = real_data['price'] - np.random.normal(0, 5)
                        
                        self.last_real_price = real_data['price']
                        
                        return {
                            'price': float(real_data['price']),
                            'prev_close': prev_price,
                            'timestamp': real_data['timestamp'],
                            'volume': float(real_data.get('volume', 75000)),  # Typical gold volume
                            'source': f"REAL-{real_data['source']}"
                        }
                except Exception as e:
                    print(f"⚠️ Simple Real Gold API error: {e}")
            
            # Fallback 2: Working Gold API as backup
            if self.working_gold_api:
                try:
                    real_data = self.working_gold_api.get_real_gold_price()
                    if real_data and real_data.get('price', 0) > 0:
                        print(f"✅ BACKUP REAL DATA: ${real_data['price']:.2f} from {real_data['source']}")
                        return {
                            'price': float(real_data['price']),
                            'prev_close': real_data['price'] - np.random.normal(0, 3),
                            'timestamp': real_data['timestamp'],
                            'volume': float(real_data.get('volume', 50000)),
                            'source': f"REAL-{real_data['source']}"
                        }
                except Exception as e:
                    print(f"⚠️ Working Gold API error: {e}")
            
            # Fallback 3: robust data source (gold)
            if self.data_source:
                try:
                    current_data = self.data_source.get_current_price()
                    if current_data and current_data.get('price', 0) > 0:
                        print(f"✅ ROBUST DATA: ${current_data['price']:.2f}")
                        return {
                            'price': current_data['price'],
                            'prev_close': current_data.get('prev_close', current_data['price']),
                            'timestamp': current_data['timestamp'],
                            'volume': current_data.get('volume', 50000)
                        }
                except Exception as e:
                    print(f"⚠️ Robust data source error: {e}")
        else:
            # Non-gold symbols: use Yahoo Finance only if configured as a backup
            feeds = self.config.get('data_feed', {})
            backups = feeds.get('backups', [])
            if 'YF' in [b.upper() if isinstance(b, str) else b for b in backups]:
                yf_quote = self._yf_get_current_quote()
                if yf_quote and yf_quote.get('price', 0) > 0:
                    print(f"✅ YF DATA {yf_quote['source']}: ${yf_quote['price']:.2f}")
                    return yf_quote
        
        # Method 4: ONLY use realistic mock as absolute last resort
        print("🚨 WARNING: All REAL sources failed - using realistic mock")
        return self._generate_realistic_quote()
    
    def _generate_mock_quote(self) -> Dict:
        """Generate mock current quote"""
        if not self.historical_data.empty:
            last_price = self.historical_data['Close'].iloc[-1]
            # Add small random movement
            current_price = last_price + np.random.normal(0, 5)
        else:
            current_price = 2640.0 + np.random.normal(0, 10)
        
        return {
            'price': current_price,
            'prev_close': current_price - np.random.normal(0, 3),
            'timestamp': datetime.now(),
            'volume': np.random.randint(1000, 5000),
            'source': 'Old Mock Data'
        }
    
    def _generate_realistic_quote(self) -> Dict:
        """Generate realistic quote around latest historical close"""
        base_price = float(self.historical_data['Close'].iloc[-1]) if not self.historical_data.empty else 2000.0
        current_price = base_price + np.random.normal(0, 8)
        prev_price = current_price - np.random.normal(0, 3)
        
        return {
            'price': current_price,
            'prev_close': prev_price,
            'timestamp': datetime.now(),
            'volume': np.random.randint(50000, 150000),  # Realistic gold volume
            'source': 'Realistic Mock'
        }
    
    def _update_historical_data(self, current_quote: Dict):
        """Update historical data with new quote"""
        # Session/blackout gating (minimal): if blocked, skip adding tradeable signal but keep data
        if self._is_blackout_or_off_session():
            pass
        new_row = pd.DataFrame({
            'Open': [current_quote['price']],
            'High': [current_quote['price']],
            'Low': [current_quote['price']],
            'Close': [current_quote['price']],
            'Volume': [current_quote['volume']]
        }, index=[current_quote['timestamp']])
        
        # Add to historical data
        self.historical_data = pd.concat([self.historical_data, new_row])

        # Keep only recent window for fast indicator recalculation
        if len(self.historical_data) > self._history_limit_default:
            self.historical_data = self.historical_data.tail(self._history_limit_default)

        # Recalculate indicators
        self.historical_data = self.indicators.calculate_all_indicators(self.historical_data)

        # Maintain a deeper buffer for NYUPIP strategy analysis
        nyupip_row = new_row.reindex(columns=["Open", "High", "Low", "Close", "Volume"])
        self._update_nyupip_history(nyupip_row)

    def _update_nyupip_history(self, row: pd.DataFrame):
        """Keep a long-running buffer of raw OHLC data for NYUPIP analysis."""
        if row is None or row.empty:
            return

        base_cols = ["Open", "High", "Low", "Close", "Volume"]

        if not hasattr(self, 'nyupip_history') or self.nyupip_history is None:
            self.nyupip_history = pd.DataFrame(columns=base_cols)

        row = row.reindex(columns=base_cols)
        self.nyupip_history = pd.concat([self.nyupip_history, row])

        if len(self.nyupip_history) > self._nyupip_history_limit:
            self.nyupip_history = self.nyupip_history.tail(self._nyupip_history_limit)

    def _get_nyupip_history(self) -> pd.DataFrame:
        """Return the long-form history buffer used by the NYUPIP strategy."""
        if not hasattr(self, 'nyupip_history') or self.nyupip_history is None:
            return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
        return self.nyupip_history

    def _is_blackout_or_off_session(self) -> bool:
        # Allow override to trade anytime
        if getattr(self, 'ignore_session_filter', False):
            return False
        try:
            cfg = self.config
            tz_name = cfg.get('sessions', {}).get('timezone', 'Africa/Johannesburg')
            import pytz
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            days = cfg.get('sessions', {}).get('days', ['Mon','Tue','Wed','Thu','Fri'])
            day = now.strftime('%a')
            start = cfg.get('sessions', {}).get('trade_start', '10:00')
            end = cfg.get('sessions', {}).get('trade_end', '19:00')
            start_h, start_m = map(int, start.split(':'))
            end_h, end_m = map(int, end.split(':'))
            start_dt = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
            end_dt = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
            # Same-day window (e.g., 08:00 -> 19:00)
            if end_dt >= start_dt:
                if day not in days:
                    return True
                return not (start_dt <= now <= end_dt)
            # Overnight window crossing midnight (e.g., 20:00 -> 03:00)
            prev_day = (now - timedelta(days=1)).strftime('%a')
            on_session = (
                (now >= start_dt and day in days) or  # after start today and today allowed
                (now <= end_dt and prev_day in days)   # before end today and previous day allowed
            )
            return not on_session
        except Exception:
            return False
        return False
    
    def _determine_signal_category(self, confidence: float, atr_value: float, signal: int, latest_data: pd.Series) -> Dict:
        """Determine signal alert category based on confidence and market conditions"""
        
        # Default values for HOLD
        if signal == 0:
            return {
                'alert_level': 'HOLD',
                'alert_color': '#FF9800',  # Orange
                'target_pips': 0,
                'success_rate': 50.0
            }
        
        try:
            # Get additional indicators for categorization
            rsi = latest_data.get('RSI_14', 50)
            macd = latest_data.get('MACD_12_26', 0)
            macd_signal = latest_data.get('MACD_Signal_9', 0)
            
            # Calculate indicator strength
            indicator_strength = 0
            
            # RSI strength (0-3 points)
            if signal == 1:  # BUY
                if rsi < 30:  # Oversold (good for buy)
                    indicator_strength += 3
                elif rsi < 40:
                    indicator_strength += 2
                elif rsi < 50:
                    indicator_strength += 1
            else:  # SELL
                if rsi > 70:  # Overbought (good for sell)
                    indicator_strength += 3
                elif rsi > 60:
                    indicator_strength += 2
                elif rsi > 50:
                    indicator_strength += 1
            
            # MACD strength (0-2 points)
            macd_divergence = abs(macd - macd_signal)
            if macd_divergence > atr_value * 0.5:  # Strong MACD signal
                indicator_strength += 2
            elif macd_divergence > atr_value * 0.2:
                indicator_strength += 1
            
            # Volatility factor (higher volatility = potentially higher rewards)
            volatility_factor = min(atr_value / 20.0, 2.0)  # Normalize ATR
            
            # Combined score for categorization
            total_score = confidence + (indicator_strength * 10) + (volatility_factor * 10)
            
            # Determine category based on tightened thresholds
            if total_score >= 90 and confidence >= 85:
                # HIGH ALERT: 40-50 pips target
                return {
                    'alert_level': 'HIGH',
                    'alert_color': '#f44336',  # Red - High attention
                    'target_pips': int(16 + (volatility_factor * 5)),  # 16-10 pips
                    'success_rate': min(confidence * 0.9, 85.0)  # Slightly lower success due to higher target
                }
            elif total_score >= 75 and confidence >= 65:
                # MEDIUM ALERT: 20-30 pips target
                return {
                    'alert_level': 'MEDIUM',
                    'alert_color': '#FF9800',  # Orange - Medium attention
                    'target_pips': int(10 + (volatility_factor * 5)),  # 10-5 pips
                    'success_rate': min(confidence * 0.95, 80.0)  # Balanced success rate
                }
            else:
                # LOW ALERT: 10-15 pips target (Conservative, highest success rate)
                return {
                    'alert_level': 'LOW',
                    'alert_color': '#4CAF50',  # Green - Safe/Conservative
                    'target_pips': int(5 + (volatility_factor * 3)),  # 1-5 pips
                    'success_rate': min(confidence * 1.1, 95.0)  # Highest success rate
                }
                
        except Exception as e:
            print(f"⚠️ Error determining signal category: {e}")
            return {
                'alert_level': 'LOW',
                'alert_color': '#4CAF50',
                'target_pips': 12,
                'success_rate': 70.0
            }

    def _calculate_risk_management(self, current_price: float, signal: int, latest_data: pd.Series, alert_category: Dict) -> Dict:
        """Calculate comprehensive risk management parameters based on alert category"""
        
        # Default values
        risk_mgmt = {
            'entry_price': current_price,
            'stop_loss': current_price,
            'take_profit_1': current_price,
            'take_profit_2': current_price, 
            'take_profit_3': current_price,
            'risk_reward_ratio': 1.0,
            'atr_value': 20.0,
            'position_size_percent': 2.0,
            'risk_amount_dollars': 200.0,
            'potential_profit_tp1': 0.0,
            'potential_profit_tp2': 0.0,
            'potential_profit_tp3': 0.0
        }
        
        try:
            # Get ATR for volatility-based stops
            atr_value = latest_data.get('ATR_14', 20.0)  # Default to $20 for gold
            if pd.isna(atr_value) or atr_value <= 0:
                atr_value = 20.0
            
            risk_mgmt['atr_value'] = float(atr_value)
            
            # Get target pips from alert category
            target_pips = alert_category.get('target_pips', 15)
            
            if signal == 1:  # BUY signal
                entry_price = current_price + (atr_value * 0.05)  # Small entry buffer
                
                # Adaptive stop loss based on alert level
                if alert_category['alert_level'] == 'HIGH':
                    stop_loss = current_price - (atr_value * 2.0)  # Wider stop for high targets
                elif alert_category['alert_level'] == 'MEDIUM':
                    stop_loss = current_price - (atr_value * 1.5)  # Balanced stop
                else:  # LOW
                    stop_loss = current_price - (atr_value * 1.0)  # Tight stop for conservative trades
                
                # Take profit levels based on target pips
                take_profit_1 = current_price + target_pips  # Primary target
                take_profit_2 = current_price + (target_pips * 1.5)  # Extended target
                take_profit_3 = current_price + (target_pips * 2.0)  # Maximum target
                
            elif signal == -1:  # SELL signal
                entry_price = current_price - (atr_value * 0.05)  # Small entry buffer
                
                # Adaptive stop loss based on alert level
                if alert_category['alert_level'] == 'HIGH':
                    stop_loss = current_price + (atr_value * 2.0)  # Wider stop for high targets
                elif alert_category['alert_level'] == 'MEDIUM':
                    stop_loss = current_price + (atr_value * 1.5)  # Balanced stop
                else:  # LOW
                    stop_loss = current_price + (atr_value * 1.0)  # Tight stop for conservative trades
                
                # Take profit levels based on target pips
                take_profit_1 = current_price - target_pips  # Primary target
                take_profit_2 = current_price - (target_pips * 1.5)  # Extended target
                take_profit_3 = current_price - (target_pips * 2.0)  # Maximum target
                
            else:  # HOLD signal
                entry_price = current_price
                stop_loss = current_price
                take_profit_1 = current_price
                take_profit_2 = current_price
                take_profit_3 = current_price
            
            # Calculate risk/reward ratio
            if signal != 0:
                risk_amount = abs(entry_price - stop_loss)
                reward_amount = abs(take_profit_1 - entry_price)
                risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 1.0
            else:
                risk_reward_ratio = 1.0
            
            # Adaptive position sizing based on alert level
            account_balance = 10000  # Assume $10K account
            
            # Risk percentage based on alert level
            if alert_category['alert_level'] == 'HIGH':
                risk_percentage = 0.015  # 1.5% for high-risk, high-reward trades
            elif alert_category['alert_level'] == 'MEDIUM':
                risk_percentage = 0.02   # 2.0% for medium trades
            else:  # LOW
                risk_percentage = 0.025  # 2.5% for conservative, high-success trades
            
            risk_per_trade = account_balance * risk_percentage
            
            if signal != 0:
                risk_per_share = abs(entry_price - stop_loss)
                if risk_per_share > 0:
                    position_size_dollars = risk_per_trade / risk_per_share
                    position_size_percent = (position_size_dollars / account_balance) * 100
                else:
                    position_size_percent = risk_percentage * 100
                    position_size_dollars = account_balance * risk_percentage
            else:
                position_size_percent = 0.0
                position_size_dollars = 0.0
            
            # Calculate potential profits
            if signal == 1:  # BUY
                potential_profit_tp1 = (take_profit_1 - entry_price) * (position_size_dollars / entry_price)
                potential_profit_tp2 = (take_profit_2 - entry_price) * (position_size_dollars / entry_price)
                potential_profit_tp3 = (take_profit_3 - entry_price) * (position_size_dollars / entry_price)
            elif signal == -1:  # SELL
                potential_profit_tp1 = (entry_price - take_profit_1) * (position_size_dollars / entry_price)
                potential_profit_tp2 = (entry_price - take_profit_2) * (position_size_dollars / entry_price)
                potential_profit_tp3 = (entry_price - take_profit_3) * (position_size_dollars / entry_price)
            else:
                potential_profit_tp1 = potential_profit_tp2 = potential_profit_tp3 = 0.0
            
            # Update risk management dictionary
            risk_mgmt.update({
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit_1': take_profit_1,
                'take_profit_2': take_profit_2,
                'take_profit_3': take_profit_3,
                'risk_reward_ratio': risk_reward_ratio,
                'position_size_percent': min(position_size_percent, 10.0),  # Cap at 10%
                'risk_amount_dollars': min(risk_per_trade, 500),  # Cap at $500
                'potential_profit_tp1': potential_profit_tp1,
                'potential_profit_tp2': potential_profit_tp2,
                'potential_profit_tp3': potential_profit_tp3
            })
            
        except Exception as e:
            print(f"⚠️ Error calculating risk management: {e}")
        
        return risk_mgmt

    def _generate_live_signal(self, current_quote: Dict) -> LiveSignal:
        """Generate live trading signal with categorized alerts and risk management"""
        
        # Respect session/blackout: if off, force HOLD signal but continue updating UI
        off = self._is_blackout_or_off_session()

        # Get latest indicator values
        latest_data = self.historical_data.iloc[-1]
        
        # Generate signal using signal generator
        signal_data = self.signal_generator.generate_all_signals(self.historical_data.tail(50))
        current_signal = signal_data['signal'].iloc[-1] if 'signal' in signal_data.columns else 0
        if off:
            current_signal = 0
        
        # Calculate confidence based on indicator alignment
        confidence = self._calculate_confidence(latest_data, current_signal)
        
        # Get ATR for alert categorization
        atr_value = latest_data.get('ATR_14', 20.0)
        
        # Determine signal alert category
        alert_category = self._determine_signal_category(confidence, atr_value, current_signal, latest_data)
        
        # Determine signal type
        if current_signal == 1:
            signal_type = "BUY"
        elif current_signal == -1:
            signal_type = "SELL"
        else:
            signal_type = "HOLD"
        
        # Calculate price changes
        price_change = current_quote['price'] - current_quote['prev_close']
        price_change_pct = (price_change / current_quote['prev_close']) * 100
        
        # Calculate risk management parameters with alert category
        risk_mgmt = self._calculate_risk_management(current_quote['price'], current_signal, latest_data, alert_category)
        
        return LiveSignal(
            timestamp=current_quote['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            symbol=self.symbol,
            current_price=current_quote['price'],
            signal=int(current_signal),
            signal_type=signal_type,
            confidence=confidence,
            rsi=float(latest_data.get('RSI_14', 50)),
            macd=float(latest_data.get('MACD_12_26', 0)),
            macd_signal=float(latest_data.get('MACD_Signal_9', 0)),
            sma_20=float(latest_data.get('SMA_20', current_quote['price'])),
            sma_50=float(latest_data.get('SMA_50', current_quote['price'])),
            price_change=price_change,
            price_change_pct=price_change_pct,
            
            # Alert Categorization
            alert_level=alert_category['alert_level'],
            alert_color=alert_category['alert_color'],
            target_pips=alert_category['target_pips'],
            success_rate=alert_category['success_rate'],
            
            # Risk Management Parameters
            entry_price=risk_mgmt['entry_price'],
            stop_loss=risk_mgmt['stop_loss'],
            take_profit_1=risk_mgmt['take_profit_1'],
            take_profit_2=risk_mgmt['take_profit_2'],
            take_profit_3=risk_mgmt['take_profit_3'],
            risk_reward_ratio=risk_mgmt['risk_reward_ratio'],
            atr_value=risk_mgmt['atr_value'],
            position_size_percent=risk_mgmt['position_size_percent'],
            risk_amount_dollars=risk_mgmt['risk_amount_dollars'],
            potential_profit_tp1=risk_mgmt['potential_profit_tp1'],
            potential_profit_tp2=risk_mgmt['potential_profit_tp2'],
            potential_profit_tp3=risk_mgmt['potential_profit_tp3']
        )
    
    def _calculate_confidence(self, latest_data: pd.Series, signal: int) -> float:
        """Calculate signal confidence based on indicator alignment"""
        confidence_score = 50.0  # Base confidence
        
        try:
            rsi = latest_data.get('RSI_14', 50)
            macd = latest_data.get('MACD_12_26', 0)
            macd_signal = latest_data.get('MACD_Signal_9', 0)
            price = latest_data.get('Close', 0)
            sma_20 = latest_data.get('SMA_20', price)
            sma_50 = latest_data.get('SMA_50', price)
            
            if signal == 1:  # BUY signal
                if rsi < 70 and rsi > 30:  # Not overbought
                    confidence_score += 10
                if macd > macd_signal:  # MACD bullish
                    confidence_score += 15
                if price > sma_20 > sma_50:  # Price above SMAs
                    confidence_score += 15
                if rsi > 50:  # RSI bullish
                    confidence_score += 10
                    
            elif signal == -1:  # SELL signal
                if rsi > 30 and rsi < 70:  # Not oversold
                    confidence_score += 10
                if macd < macd_signal:  # MACD bearish
                    confidence_score += 15
                if price < sma_20 < sma_50:  # Price below SMAs
                    confidence_score += 15
                if rsi < 50:  # RSI bearish
                    confidence_score += 10
            
            # Cap confidence at 95%
            confidence_score = min(confidence_score, 95.0)
            
        except Exception as e:
            print(f"⚠️ Error calculating confidence: {e}")
        
        return confidence_score
    
    def add_signal_callback(self, callback: Callable):
        """Add callback function to be called when new signals are generated"""
        self.signal_callbacks.append(callback)
    
    def _notify_callbacks(self, signal: LiveSignal):
        """Notify all registered callbacks of new signal"""
        for callback in self.signal_callbacks:
            try:
                callback(signal)
            except Exception as e:
                print(f"⚠️ Error in callback: {e}")
    
    def start_streaming(self):
        """Start the live data streaming"""
        self.is_running = True
        
        def stream_loop():
            print(f"🚀 Starting live data stream for {self.symbol}")
            print(f"⏱️ Update interval: {self.update_interval} seconds")
            
            while self.is_running:
                try:
                    # Fetch current quote
                    current_quote = self._fetch_current_quote()
                    
                    if current_quote:
                        # Pre-trade guard: spread and ATR floors
                        try:
                            filters = self.config.get('filters', {})
                            max_spread = float(filters.get('max_spread_points', 30))
                            min_atr_pips = float(filters.get('min_atr_pips', 3))
                            latest_atr = float(self.historical_data.iloc[-1].get('ATR_14', 0)) if not self.historical_data.empty else 0
                            if current_quote.get('spread_points') and current_quote['spread_points'] > max_spread:
                                print(f"⛔ Spread guard: {current_quote['spread_points']:.1f} > {max_spread}")
                                # Still update data/UI but skip sends this tick
                                spread_block = True
                            else:
                                spread_block = False
                            atr_block = latest_atr < min_atr_pips
                            if atr_block:
                                print(f"⛔ ATR guard: ATR_14 {latest_atr:.2f} < {min_atr_pips}")
                        except Exception:
                            spread_block = False
                            atr_block = False
                        # Update historical data
                        self._update_historical_data(current_quote)
                        
                        # Generate signal
                        live_signal = self._generate_live_signal(current_quote)
                        
                        # Store current signal
                        self.current_signal = live_signal
                        self.last_update = datetime.now()

                        # Persist signal
                        if self.persistence:
                            try:
                                self.persistence.save_signal(asdict(live_signal))
                            except Exception as e:
                                print(f"⚠️ Persist error: {e}")
                        
                        # Notify callbacks
                        self._notify_callbacks(live_signal)
                        
                        # Print update
                        print(f"🔄 {live_signal.timestamp} | {live_signal.symbol} | ${live_signal.current_price:.2f} | {live_signal.signal_type} ({live_signal.confidence:.1f}%)")

                        # Event override path
                        if self.event_mode_enabled and self.event_engine:
                            try:
                                latest = self.historical_data.iloc[-1]
                                high = float(latest.get('High', current_quote['price']))
                                low = float(latest.get('Low', current_quote['price']))
                                atr_val = float(latest.get('ATR_14', 0))
                                self.event_engine.try_detect_spike(high, low, atr_val)
                                idea = self.event_engine.generate_signal(current_quote['price'])
                                if idea and not spread_block and self.trading_enabled:
                                    side = idea['direction']
                                    entry = idea['entry']
                                    sl = idea['sl']
                                    tp = idea['tp']
                                    trade = self.autotrader.place_market_order(side, entry, sl, tp)
                                    if trade and self.persistence:
                                        self.persistence.save_trade({
                                            'timestamp': live_signal.timestamp,
                                            'symbol': live_signal.symbol,
                                            'direction': side,
                                            'entry': entry,
                                            'sl': sl,
                                            'tp': tp,
                                            'lots': trade.get('volume', 0.0),
                                            'ticket': trade.get('ticket', 0),
                                            'status': 'SENT',
                                            'alert_level': 'EVENT',
                                            'tier': 'EVENT',
                                            'engine': 'EVENT'
                                        })
                                        print(f"⚡ [EVENT] order sent: ticket={trade.get('ticket')} entry={entry:.2f} sl={sl:.2f} tp={tp:.2f}")
                            except Exception as e:
                                print(f"⚠️ Event engine error: {e}")

                        # Auto-trading (opt-in) with campaign and per-alert logic
                        if (
                            self.autotrader
                            and self.autotrader.enabled
                            and self.trading_enabled
                            and live_signal.signal != 0
                            and not self._is_blackout_or_off_session()
                            and not spread_block
                            and not atr_block
                            and not self.event_mode_enabled
                        ):
                            # Respect per-symbol daily loss cap halt
                            if self.order_manager and getattr(self.order_manager, 'halt_new_orders', False):
                                print(f"⏸️ Halt new orders (daily cap) for {self.symbol}")
                                continue
                            level = (live_signal.alert_level or 'LOW').upper()
                            side = 1 if live_signal.signal == 1 else -1
                            engine_mode = getattr(self, 'engine_mode', 'ALL')
                            general_allowed = True
                            farmer_allowed = self.farmer_enabled

                            if engine_mode == 'NONE':
                                general_allowed = False
                                farmer_allowed = False
                            elif engine_mode == 'FARMER_ONLY':
                                general_allowed = False
                            elif engine_mode == 'LOW_ONLY':
                                general_allowed = (level == 'LOW')
                                farmer_allowed = False
                            elif engine_mode == 'MEDIUM_ONLY':
                                general_allowed = (level == 'MEDIUM')
                                farmer_allowed = False
                            elif engine_mode == 'HIGH_ONLY':
                                general_allowed = (level == 'HIGH')
                                farmer_allowed = False
                            elif engine_mode == 'EVENT_ONLY':
                                general_allowed = False
                                farmer_allowed = False

                            if general_allowed:
                                # Per-engine gating
                                if level == 'LOW' and not self.enable_low:
                                    print("⏸️ Engine gated: LOW disabled")
                                elif level == 'MEDIUM' and not self.enable_medium:
                                    print("⏸️ Engine gated: MEDIUM disabled")
                                elif level == 'HIGH' and not self.enable_high:
                                    print("⏸️ Engine gated: HIGH disabled")
                                else:
                                    # campaign check
                                    if self.campaign and not self.campaign.allow(self.symbol, side, level):
                                        print(f"⛔ Campaign limit reached for {level} {('BUY' if side==1 else 'SELL')}")
                                    else:
                                        # Determine TP by level/tiering
                                        tp = live_signal.take_profit_1
                                        cfg_exec = self.config.get('execution', {})
                                        if level == 'LOW':
                                            tp_pips = int(cfg_exec.get('low_tp_pips', 5))
                                            tp_low_abs = live_signal.entry_price + (tp_pips if side==1 else -tp_pips)
                                            tp = tp_low_abs
                                        elif level == 'MEDIUM':
                                            tp_pips = int(cfg_exec.get('medium_tp_primary_pips', 9))
                                            tp_med_abs = live_signal.entry_price + (tp_pips if side==1 else -tp_pips)
                                            tp = tp_med_abs
                                        # HIGH: allow tiered spawning counts
                                        tiers = []
                                        if level == 'HIGH':
                                            tier_cfg = cfg_exec.get('high_tier_tp_pips', { 'tier1_count':2,'tier1_pips':6,'tier2_count':3,'tier2_pips':9 })
                                            tiers = (
                                                [('TIER1', tier_cfg.get('tier1_pips',6))]*int(tier_cfg.get('tier1_count',2)) +
                                                [('TIER2', tier_cfg.get('tier2_pips',9))]*int(tier_cfg.get('tier2_count',3))
                                            )
                                        # Spawn orders
                                        def send_one(tier_name: Optional[str], tp_pips_override: Optional[int], tp_absolute: Optional[float] = None, engine: str = "INTRADAY"):
                                            nonlocal live_signal
                                            sl = live_signal.stop_loss
                                            entry = live_signal.entry_price
                                            local_tp = live_signal.take_profit_1
                                            if tp_absolute is not None:
                                                local_tp = tp_absolute
                                            elif tp_pips_override is not None:
                                                local_tp = entry + (tp_pips_override if side==1 else -tp_pips_override)
                                            trade = self.autotrader.place_market_order(side, entry, sl, local_tp)
                                            if trade and self.persistence:
                                                try:
                                                    self.persistence.save_trade({
                                                        'timestamp': live_signal.timestamp,
                                                        'symbol': live_signal.symbol,
                                                        'direction': side,
                                                        'entry': entry,
                                                        'sl': sl,
                                                        'tp': local_tp,
                                                        'lots': trade.get('volume', 0.0),
                                                        'ticket': trade.get('ticket', 0),
                                                        'status': 'SENT',
                                                        'alert_level': level,
                                                        'tier': tier_name or '',
                                                        'engine': engine
                                                    })
                                                    print(f"✅ [{engine}] Order sent: ticket={trade.get('ticket')} lots={trade.get('volume')} tier={tier_name or 'BASE'}")
                                                    if self.order_manager:
                                                        self.order_manager.register_new_order(trade.get('ticket'), side, entry, sl, local_tp, level, tier=tier_name)
                                                    if self.campaign:
                                                        self.campaign.record(self.symbol, side, level)
                                                except Exception as e:
                                                    print(f"⚠️ Trade persist error: {e}")
                                        if level == 'HIGH' and tiers:
                                            # Send tiered partials first
                                            for tier_name, pips in tiers:
                                                if not self.campaign or self.campaign.allow(self.symbol, side, level):
                                                    send_one(tier_name, pips, engine="SWING_HIGH")
                                            # Remaining up to campaign limit use base TP
                                            if not self.campaign or self.campaign.allow(self.symbol, side, level):
                                                send_one(None, None, engine="SWING_HIGH")
                                        else:
                                            # LOW/MEDIUM use absolute TP we computed
                                            engine_name = "INTRADAY_LOW" if level=="LOW" else ("INTRADAY_MED" if level=="MEDIUM" else "INTRADAY")
                                            send_one(None, None, tp_absolute=tp, engine=engine_name)
                            else:
                                if engine_mode == 'NONE':
                                    print("⏸️ Engine mode NONE blocking automated entries")
                                elif engine_mode == 'FARMER_ONLY':
                                    print("⏸️ Engine mode FARMER_ONLY skipping tiered engines")
                                elif engine_mode.endswith('_ONLY'):
                                    print(f"⏸️ Engine mode {engine_mode} skipping {level} signal")

                            # 2-pip farmer (runs alongside, subject to farmer cycle)
                            try:
                                # Farmer runs independently every cycle when a non-HOLD signal exists,
                                # but piggybacks the HIGH campaign gate.
                                if farmer_allowed and self.trading_enabled and live_signal.signal != 0:
                                    now = datetime.now()
                                    if not self._farmer_last_cycle or (now - self._farmer_last_cycle).total_seconds() >= self.farmer_cycle_seconds:
                                        self._farmer_last_cycle = now
                                        farmer_cfg = self.config.get('execution', {}).get('farmer', {})
                                        # Dynamic TP by ATR if enabled
                                        dyn = bool(farmer_cfg.get('dynamic_tp', True))
                                        atr_val = float(self.historical_data.iloc[-1].get('ATR_14', 0)) if not self.historical_data.empty else 0
                                        base_tp = int(farmer_cfg.get('tp_pips', 2))
                                        if dyn:
                                            if atr_val >= 20:
                                                tp_pips = min(5, base_tp + 2)
                                            elif atr_val >= 12:
                                                tp_pips = min(4, base_tp + 1)
                                            else:
                                                tp_pips = base_tp
                                        else:
                                            tp_pips = base_tp
                                        sl_pips = int(farmer_cfg.get('sl_pips', 6))
                                        count = int(farmer_cfg.get('trades_per_cycle', 3))
                                        # place burst of small TP orders
                                        for i in range(count):
                                            # piggyback HIGH gate regardless of current alert level
                                            if self.campaign and not self.campaign.allow(self.symbol, side, 'HIGH'):
                                                break
                                            entry = live_signal.entry_price
                                            sl = entry - sl_pips if side == 1 else entry + sl_pips
                                            tp_small = entry + tp_pips if side == 1 else entry - tp_pips
                                            trade = self.autotrader.place_market_order(side, entry, sl, tp_small)
                                            if trade and self.persistence:
                                                try:
                                                    self.persistence.save_trade({
                                                        'timestamp': live_signal.timestamp,
                                                        'symbol': live_signal.symbol,
                                                        'direction': side,
                                                        'entry': entry,
                                                        'sl': sl,
                                                        'tp': tp_small,
                                                        'lots': trade.get('volume', 0.0),
                                                        'ticket': trade.get('ticket', 0),
                                                        'status': 'SENT',
                                                        'alert_level': 'HIGH',
                                                        'tier': 'FARMER',
                                                        'engine': 'FARMER'
                                                    })
                                                    if self.order_manager:
                                                        self.order_manager.register_new_order(trade.get('ticket'), side, entry, sl, tp_small, 'HIGH', tier='FARMER')
                                                    if self.campaign:
                                                        self.campaign.record(self.symbol, side, 'HIGH')
                                                    print(f"🌾 Farmer order sent: ticket={trade.get('ticket')} tp={tp_pips}p atr={atr_val:.2f}")
                                                except Exception as e:
                                                    print(f"⚠️ Farmer persist error: {e}")
                            except Exception:
                                pass

                        if self.nyupip_enabled:
                            try:
                                eval_time = datetime.now().strftime("%H:%M:%S")
                                nyupip_history = self._get_nyupip_history()
                                
                                if nyupip_history is None or nyupip_history.empty:
                                    print(f"🔍 [{eval_time}] NYUPIP: Evaluating | ⚠️ No history data available")
                                else:
                                    print(f"🔍 [{eval_time}] NYUPIP: Evaluating | History: {len(nyupip_history)} bars")
                                
                                nyupip_signals = self.nyupip_strategy.evaluate(nyupip_history.copy(), current_quote)
                                self.nyupip_state['last_diagnostics'] = self.nyupip_strategy.get_last_diagnostics()
                                
                                diag = self.nyupip_state.get('last_diagnostics', {})
                                status = diag.get('status', 'unknown')
                                reason = diag.get('reason', 'no_reason')
                                
                                if nyupip_signals:
                                    print(f"✅ [{eval_time}] NYUPIP: {len(nyupip_signals)} signal(s) generated | Status: {status}")
                                    for nyupip_signal in nyupip_signals:
                                        self._process_nyupip_signal(nyupip_signal, spread_block, atr_block)
                                else:
                                    # Format reason for readability
                                    reason_display = reason.replace('_', ' ').title() if reason else 'No signal conditions met'
                                    print(f"⏸️ [{eval_time}] NYUPIP: No signals | Status: {status} | Reason: {reason_display}")
                                    
                                    # Show detailed diagnostics if available
                                    if diag.get('summary'):
                                        summary = diag['summary']
                                        zone_status = "✓" if summary.get('zone_valid') else "✗"
                                        atr_status = "✓" if summary.get('atr_valid') else "✗"
                                        trendline_status = "✓" if summary.get('trendline_valid') else "✗"
                                        print(f"   └─ Zone: {zone_status} | ATR: {atr_status} | Trendline: {trendline_status}")
                                        
                            except Exception as e:
                                print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] NYUPIP processing error: {e}")

                        strategy_history = None
                        try:
                            history_source = self._get_nyupip_history()
                            if history_source is not None and not history_source.empty:
                                strategy_history = history_source.copy()
                        except Exception:
                            strategy_history = None
                        if strategy_history is None or strategy_history.empty:
                            strategy_history = self.historical_data["Open"].to_frame().join(
                                self.historical_data[[c for c in ["High", "Low", "Close", "Volume"] if c in self.historical_data.columns]],
                                how="outer"
                            ).dropna()

                        if self.ict_swing_enabled and self.ict_swing_strategy and self._is_gold_symbol():
                            try:
                                eval_time = datetime.now().strftime("%H:%M:%S")
                                
                                if strategy_history is None or strategy_history.empty:
                                    print(f"🔍 [{eval_time}] ICT Swing: Evaluating | ⚠️ No history data available")
                                else:
                                    print(f"🔍 [{eval_time}] ICT Swing: Evaluating | History: {len(strategy_history)} bars")
                                
                                swing_signals, swing_diag = self.ict_swing_strategy.evaluate(strategy_history, current_quote)
                                self.ict_swing_state['last_diagnostics'] = swing_diag
                                
                                status = swing_diag.get('status', 'unknown')
                                reason = swing_diag.get('reason', 'no_reason')
                                
                                if swing_signals:
                                    print(f"✅ [{eval_time}] ICT Swing: {len(swing_signals)} signal(s) generated | Status: {status}")
                                    for swing_signal in swing_signals:
                                        self._process_ict_swing_signal(swing_signal, spread_block, atr_block)
                                else:
                                    # Format reason for readability
                                    reason_display = reason.replace('_', ' ').title() if reason else 'No signal conditions met'
                                    print(f"⏸️ [{eval_time}] ICT Swing: No signals | Status: {status} | Reason: {reason_display}")
                                    
                                    # Show session alignment info if available
                                    summary = swing_diag.get('summary', {})
                                    if summary:
                                        sessions = summary.get('sessions', {})
                                        if sessions:
                                            asian = sessions.get('asian', {})
                                            london = sessions.get('london', {})
                                            ny = sessions.get('new_york', {})
                                            print(f"   └─ Asian: {asian.get('open', 'N/A')} | London: {london.get('open', 'N/A')} | NY: {ny.get('open', 'N/A')}")
                                        
                            except Exception as e:
                                print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] ICT Swing processing error: {e}")

                        if self.ict_atm_enabled and self.ict_atm_strategy and self._is_gold_symbol():
                            try:
                                eval_time = datetime.now().strftime("%H:%M:%S")
                                
                                if strategy_history is None or strategy_history.empty:
                                    print(f"🔍 [{eval_time}] ICT ATM: Evaluating | ⚠️ No history data available")
                                else:
                                    print(f"🔍 [{eval_time}] ICT ATM: Evaluating | History: {len(strategy_history)} bars")
                                
                                atm_signals, atm_diag = self.ict_atm_strategy.evaluate(strategy_history, current_quote)
                                self.ict_atm_state['last_diagnostics'] = atm_diag
                                
                                status = atm_diag.get('status', 'unknown')
                                reason = atm_diag.get('reason', 'no_reason')
                                
                                if atm_signals:
                                    print(f"✅ [{eval_time}] ICT ATM: {len(atm_signals)} signal(s) generated | Status: {status}")
                                    for atm_signal in atm_signals:
                                        self._process_ict_atm_signal(atm_signal, spread_block, atr_block)
                                else:
                                    # Format reason for readability
                                    reason_display = reason.replace('_', ' ').title() if reason else 'No signal conditions met'
                                    print(f"⏸️ [{eval_time}] ICT ATM: No signals | Status: {status} | Reason: {reason_display}")
                                    
                                    # Show detailed diagnostics if available
                                    summary = atm_diag.get('summary', {})
                                    if summary:
                                        atr_current = summary.get('atr_current')
                                        atr_avg = summary.get('atr_avg')
                                        if atr_current is not None and atr_avg is not None:
                                            atr_ratio = atr_current / atr_avg if atr_avg > 0 else 0
                                            print(f"   └─ ATR Current: {atr_current:.2f} | ATR Avg: {atr_avg:.2f} | Ratio: {atr_ratio:.2f}x")
                                        
                            except Exception as e:
                                print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] ICT ATM processing error: {e}")
                        
                    else:
                        print("⚠️ Failed to fetch current quote")
                
                except Exception as e:
                    print(f"❌ Error in streaming loop: {e}")
                
                # Reconcile positions periodically
                try:
                    if self.order_manager:
                        self.order_manager.reconcile()
                except Exception:
                    pass
                # Wait for next update
                time.sleep(self.update_interval)
        
        # Start streaming in background thread
        self.stream_thread = threading.Thread(target=stream_loop, daemon=True)
        self.stream_thread.start()
    
    def stop_streaming(self):
        """Stop the live data streaming"""
        self.is_running = False
        print("🛑 Live data streaming stopped")
    
    def get_current_signal(self) -> Optional[LiveSignal]:
        """Get the current live signal"""
        return self.current_signal
    
    def get_status(self) -> Dict:
        """Get current streaming status"""
        # Compute farmer next seconds
        next_in = None
        if self.farmer_enabled:
            if self._farmer_last_cycle is None:
                next_in = self.farmer_cycle_seconds
            else:
                elapsed = (datetime.now() - self._farmer_last_cycle).total_seconds()
                next_in = max(0, self.farmer_cycle_seconds - int(elapsed))
        return {
            'is_running': self.is_running,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'symbol': self.symbol,
            'update_interval': self.update_interval,
            'current_signal': asdict(self.current_signal) if self.current_signal else None,
            'farmer_enabled': self.farmer_enabled,
            'farmer_next_in_seconds': next_in,
            'engine_low_enabled': self.enable_low,
            'engine_medium_enabled': self.enable_medium,
            'engine_high_enabled': self.enable_high,
            'event_mode_enabled': self.event_mode_enabled,
            'engine_mode': self.engine_mode,
            'nyupip_enabled': self.nyupip_enabled,
            'nyupip_last_signal': self.nyupip_state.get('last_signal'),
            'nyupip_last_diagnostics': self.nyupip_state.get('last_diagnostics'),
            'trading_enabled': self.trading_enabled,
            'ict_swing_enabled': self.ict_swing_enabled,
            'ict_swing_state': self.get_ict_swing_state(),
            'ict_atm_enabled': self.ict_atm_enabled,
            'ict_atm_state': self.get_ict_atm_state(),
        }

    def set_farmer_enabled(self, enabled: bool):
        self.farmer_enabled = bool(enabled)

    def set_engine_enabled(self, level: str, enabled: bool):
        lv = (level or '').upper()
        if lv == 'LOW':
            self.enable_low = bool(enabled)
        elif lv == 'MEDIUM':
            self.enable_medium = bool(enabled)
        elif lv == 'HIGH':
            self.enable_high = bool(enabled)

    def set_event_mode(self, enabled: bool):
        self.event_mode_enabled = bool(enabled)

    def set_trading_enabled(self, enabled: bool):
        self.trading_enabled = bool(enabled)

    def set_engine_mode(self, mode: str):
        allowed = {'ALL', 'FARMER_ONLY', 'LOW_ONLY', 'MEDIUM_ONLY', 'HIGH_ONLY', 'EVENT_ONLY', 'NONE'}
        mode = (mode or 'ALL').upper()
        if mode not in allowed:
            raise ValueError(f"Invalid engine mode: {mode}")

        self.engine_mode = mode

        if mode == 'ALL':
            self.enable_low = True
            self.enable_medium = True
            self.enable_high = True
            self.event_mode_enabled = False
            self.farmer_enabled = self._farmer_default_enabled
        elif mode == 'NONE':
            self.enable_low = False
            self.enable_medium = False
            self.enable_high = False
            self.event_mode_enabled = False
            self.farmer_enabled = False
        elif mode == 'FARMER_ONLY':
            self.enable_low = False
            self.enable_medium = False
            self.enable_high = False
            self.event_mode_enabled = False
            self.farmer_enabled = True
        elif mode == 'LOW_ONLY':
            self.enable_low = True
            self.enable_medium = False
            self.enable_high = False
            self.event_mode_enabled = False
            self.farmer_enabled = False
        elif mode == 'MEDIUM_ONLY':
            self.enable_low = False
            self.enable_medium = True
            self.enable_high = False
            self.event_mode_enabled = False
            self.farmer_enabled = False
        elif mode == 'HIGH_ONLY':
            self.enable_low = False
            self.enable_medium = False
            self.enable_high = True
            self.event_mode_enabled = False
            self.farmer_enabled = False
        elif mode == 'EVENT_ONLY':
            self.enable_low = False
            self.enable_medium = False
            self.enable_high = False
            self.event_mode_enabled = True
            self.farmer_enabled = False
        elif mode == 'NONE':
            self.enable_low = False
            self.enable_medium = False
            self.enable_high = False
            self.event_mode_enabled = False
            self.farmer_enabled = False

    # ------------------------------------------------------------------
    # NYUPIP strategy helpers
    # ------------------------------------------------------------------
    def set_nyupip_enabled(self, enabled: bool):
        self.nyupip_enabled = bool(enabled)
        self.nyupip_state['enabled'] = self.nyupip_enabled
        if self.nyupip_enabled:
            self.nyupip_state['last_diagnostics'] = self.nyupip_strategy.get_last_diagnostics()
        else:
            self.nyupip_state['last_diagnostics'] = None
        status = 'enabled' if self.nyupip_enabled else 'disabled'
        print(f"🟣 NYUPIP strategy {status} for {self.symbol}")

    def get_nyupip_state(self) -> Dict[str, object]:
        return {
            'enabled': self.nyupip_enabled,
            'last_signal': self.nyupip_state.get('last_signal'),
            'auto_last_ticket': self.nyupip_state.get('auto_last_ticket'),
            'last_diagnostics': self.nyupip_state.get('last_diagnostics'),
        }

    def set_ict_swing_enabled(self, enabled: bool):
        if not self._is_gold_symbol() or not self.ict_swing_strategy:
            self.ict_swing_enabled = False
            self.ict_swing_state['enabled'] = False
            print("🟠 ICT Swing strategy unavailable for non-gold symbol")
            return
        self.ict_swing_enabled = bool(enabled)
        self.ict_swing_state['enabled'] = self.ict_swing_enabled
        if self.ict_swing_enabled:
            self.ict_swing_state['last_diagnostics'] = self.ict_swing_strategy.get_last_diagnostics()
        status = 'enabled' if self.ict_swing_enabled else 'disabled'
        print(f"🟠 ICT Swing strategy {status} for {self.symbol}")

    def get_ict_swing_state(self) -> Dict[str, object]:
        return {
            'enabled': self.ict_swing_enabled,
            'last_signal': self.ict_swing_state.get('last_signal'),
            'auto_last_ticket': self.ict_swing_state.get('auto_last_ticket'),
            'last_diagnostics': self.ict_swing_state.get('last_diagnostics'),
        }

    def set_ict_atm_enabled(self, enabled: bool):
        if not self._is_gold_symbol() or not self.ict_atm_strategy:
            self.ict_atm_enabled = False
            self.ict_atm_state['enabled'] = False
            print("🟣 ICT ATM strategy unavailable for non-gold symbol")
            return
        self.ict_atm_enabled = bool(enabled)
        self.ict_atm_state['enabled'] = self.ict_atm_enabled
        if self.ict_atm_enabled:
            self.ict_atm_state['last_diagnostics'] = self.ict_atm_strategy.get_last_diagnostics()
        status = 'enabled' if self.ict_atm_enabled else 'disabled'
        print(f"🟣 ICT ATM strategy {status} for {self.symbol}")

    def get_ict_atm_state(self) -> Dict[str, object]:
        return {
            'enabled': self.ict_atm_enabled,
            'last_signal': self.ict_atm_state.get('last_signal'),
            'auto_last_ticket': self.ict_atm_state.get('auto_last_ticket'),
            'last_diagnostics': self.ict_atm_state.get('last_diagnostics'),
        }

    def _process_nyupip_signal(self, signal: NYUPIPSignal, spread_block: bool, atr_block: bool):
        payload = signal.to_payload()
        self.nyupip_state['last_signal'] = payload
        self.nyupip_state['last_diagnostics'] = self.nyupip_strategy.get_last_diagnostics()

        direction = 'BUY' if signal.direction == 1 else 'SELL'
        print(
            f"🟣 [NYUPIP-{signal.module}] {direction} @ {signal.entry_price:.2f} | "
            f"SL {signal.stop_loss:.2f} | TP {signal.take_profit_primary:.2f} | RR {signal.risk_reward:.2f}"
        )

        if self.persistence:
            try:
                record = payload.copy()
                record.update({
                    'engine': f'NYUPIP_{signal.module}',
                    'strategy': 'NYUPIP',
                    'timestamp': signal.timestamp.isoformat(),
                    'direction': signal.direction,
                })
                self.persistence.save_signal(record)
            except Exception as exc:
                print(f"⚠️ NYUPIP persist error: {exc}")

        can_trade = (
            self.autotrader
            and self.autotrader.enabled
            and self.trading_enabled
            and not spread_block
            and not atr_block
            and not self.event_mode_enabled
            and not self._is_blackout_or_off_session()
        )

        if not can_trade:
            # Diagnostic logging for why trade was blocked
            block_reasons = []
            if not self.autotrader:
                block_reasons.append("No AutoTrader")
            elif not self.autotrader.enabled:
                block_reasons.append("AutoTrader disabled")
            if not self.trading_enabled:
                block_reasons.append("Trading disabled")
            if spread_block:
                block_reasons.append("Spread too wide")
            if atr_block:
                block_reasons.append("ATR too low")
            if self.event_mode_enabled:
                block_reasons.append("Event mode active")
            if self._is_blackout_or_off_session():
                block_reasons.append("Outside trading session")
            
            reason_str = " | ".join(block_reasons) if block_reasons else "Unknown reason"
            print(f"⛔ [{datetime.now().strftime('%H:%M:%S')}] NYUPIP: Signal generated but blocked | {reason_str}")
            return

        try:
            trade = self.autotrader.place_market_order(
                signal.direction,
                signal.entry_price,
                signal.stop_loss,
                signal.take_profit_primary,
            )
        except Exception as exc:
            print(f"⚠️ NYUPIP auto-trade error: {exc}")
            return

        if not trade:
            return

        ticket = trade.get('ticket', 0)
        self.nyupip_state['auto_last_ticket'] = ticket
        print(f"✅ [NYUPIP-{signal.module}] Auto order sent ticket={ticket} lots={trade.get('volume', 0.0)}")

        if self.persistence:
            try:
                self.persistence.save_trade({
                    'timestamp': signal.timestamp.isoformat(),
                    'symbol': self.symbol,
                    'direction': signal.direction,
                    'entry': signal.entry_price,
                    'sl': signal.stop_loss,
                    'tp': signal.take_profit_primary,
                    'lots': trade.get('volume', 0.0),
                    'ticket': ticket,
                    'status': 'SENT',
                    'alert_level': signal.module,
                    'tier': 'NYUPIP',
                    'engine': f'NYUPIP_{signal.module}'
                })
            except Exception as exc:
                print(f"⚠️ NYUPIP trade persist error: {exc}")

        if self.order_manager:
            try:
                self.order_manager.register_new_order(
                    ticket,
                    signal.direction,
                    signal.entry_price,
                    signal.stop_loss,
                    signal.take_profit_primary,
                    signal.module,
                    tier='NYUPIP'
                )
            except Exception as exc:
                print(f"⚠️ Order manager NYUPIP error: {exc}")

    def _process_ict_swing_signal(self, signal: ICTSwingSignal, spread_block: bool, atr_block: bool):
        payload = signal.to_payload()
        self.ict_swing_state['last_signal'] = payload
        if self.ict_swing_strategy:
            self.ict_swing_state['last_diagnostics'] = self.ict_swing_strategy.get_last_diagnostics()

        direction_txt = 'BUY' if signal.direction == 1 else 'SELL'
        print(
            f"🟠 [ICT Swing {signal.session}] {direction_txt} @ {signal.entry_price:.2f} | "
            f"SL {signal.stop_loss:.2f} | TP {signal.take_profit_primary:.2f} | RR {signal.risk_reward:.2f}"
        )

        if self.persistence:
            try:
                metadata = signal.metadata or {}
                self.persistence.save_signal({
                    'timestamp': payload['timestamp'],
                    'symbol': signal.symbol,
                    'current_price': signal.entry_price,
                    'signal': signal.direction,
                    'signal_type': direction_txt,
                    'confidence': signal.confidence,
                    'rsi': None,
                    'macd': None,
                    'macd_signal': None,
                    'sma_20': None,
                    'sma_50': None,
                    'price_change': None,
                    'price_change_pct': None,
                    'alert_level': signal.session,
                    'alert_color': None,
                    'target_pips': None,
                    'success_rate': None,
                    'entry_price': signal.entry_price,
                    'stop_loss': signal.stop_loss,
                    'take_profit_1': signal.take_profit_primary,
                    'take_profit_2': signal.take_profit_secondary,
                    'take_profit_3': signal.take_profit_tertiary,
                    'risk_reward_ratio': signal.risk_reward,
                    'atr_value': metadata.get('atr_like'),
                    'position_size_percent': None,
                    'risk_amount_dollars': None,
                    'potential_profit_tp1': None,
                    'potential_profit_tp2': None,
                    'potential_profit_tp3': None,
                })
            except Exception as exc:
                print(f"⚠️ ICT Swing persist error: {exc}")

        can_trade = (
            self.autotrader
            and self.autotrader.enabled
            and self.trading_enabled
            and not spread_block
            and not atr_block
            and not self.event_mode_enabled
            and not self._is_blackout_or_off_session()
        )

        engine_mode = getattr(self, 'engine_mode', 'ALL')
        if engine_mode in {'NONE', 'FARMER_ONLY', 'LOW_ONLY', 'MEDIUM_ONLY', 'EVENT_ONLY'}:
            can_trade = False
        if not self.enable_high:
            can_trade = False

        if not can_trade:
            # Diagnostic logging for why trade was blocked
            block_reasons = []
            if not self.autotrader:
                block_reasons.append("No AutoTrader")
            elif not self.autotrader.enabled:
                block_reasons.append("AutoTrader disabled")
            if not self.trading_enabled:
                block_reasons.append("Trading disabled")
            if spread_block:
                block_reasons.append("Spread too wide")
            if atr_block:
                block_reasons.append("ATR too low")
            if self.event_mode_enabled:
                block_reasons.append("Event mode active")
            if self._is_blackout_or_off_session():
                block_reasons.append("Outside trading session")
            if engine_mode in {'NONE', 'FARMER_ONLY', 'LOW_ONLY', 'MEDIUM_ONLY', 'EVENT_ONLY'}:
                block_reasons.append(f"Engine mode: {engine_mode}")
            if not self.enable_high:
                block_reasons.append("HIGH engine disabled")
            
            reason_str = " | ".join(block_reasons) if block_reasons else "Unknown reason"
            print(f"⛔ [{datetime.now().strftime('%H:%M:%S')}] ICT Swing: Signal generated but blocked | {reason_str}")
            return

        if self.order_manager and getattr(self.order_manager, 'halt_new_orders', False):
            print(f"⏸️ [{datetime.now().strftime('%H:%M:%S')}] ICT Swing: Halt new orders (daily loss cap reached)")
            return

        # Use a distinct campaign bucket for ICT Swing so it doesn't compete with ATM
        swing_bucket = 'HIGH_SWING'
        if self.campaign and not self.campaign.allow(self.symbol, signal.direction, swing_bucket):
            current_count = self.campaign.current_count(self.symbol, signal.direction, swing_bucket) if self.campaign else 0
            max_count = self.campaign.max_per_level.get(swing_bucket, self.campaign.max_per_level.get('HIGH', 9)) if self.campaign else 9
            print(f"⛔ [{datetime.now().strftime('%H:%M:%S')}] ICT Swing: Campaign limit reached ({current_count}/{max_count} {swing_bucket} trades in window)")
            return

        try:
            trade = self.autotrader.place_market_order(
                signal.direction,
                signal.entry_price,
                signal.stop_loss,
                signal.take_profit_primary,
            )
        except Exception as exc:
            print(f"⚠️ ICT Swing auto-trade error: {exc}")
            return

        if not trade:
            return

        ticket = trade.get('ticket', 0)
        self.ict_swing_state['auto_last_ticket'] = ticket
        print(f"✅ [ICT Swing {signal.session}] Auto order sent ticket={ticket} lots={trade.get('volume', 0.0)}")

        if self.persistence:
            try:
                self.persistence.save_trade({
                    'timestamp': payload['timestamp'],
                    'symbol': self.symbol,
                    'direction': signal.direction,
                    'entry': signal.entry_price,
                    'sl': signal.stop_loss,
                    'tp': signal.take_profit_primary,
                    'lots': trade.get('volume', 0.0),
                    'ticket': ticket,
                    'status': 'SENT',
                    'alert_level': signal.session,
                    'tier': signal.scenario,
                    'engine': 'ICT_SWING'
                })
            except Exception as exc:
                print(f"⚠️ ICT Swing trade persist error: {exc}")

        if self.order_manager:
            try:
                self.order_manager.register_new_order(
                    ticket,
                    signal.direction,
                    signal.entry_price,
                    signal.stop_loss,
                    signal.take_profit_primary,
                    f"ICT_SWING_{signal.session}",
                    tier=signal.scenario,
                )
            except Exception as exc:
                print(f"⚠️ Order manager ICT Swing error: {exc}")
        if self.campaign:
            self.campaign.record(self.symbol, signal.direction, swing_bucket)

    def _process_ict_atm_signal(self, signal: ICTATMSignal, spread_block: bool, atr_block: bool):
        payload = signal.to_payload()
        self.ict_atm_state['last_signal'] = payload
        if self.ict_atm_strategy:
            self.ict_atm_state['last_diagnostics'] = self.ict_atm_strategy.get_last_diagnostics()

        direction_txt = 'BUY' if signal.direction == 1 else 'SELL'
        print(
            f"🟣 [ICT ATM] {direction_txt} @ {signal.entry_price:.2f} | "
            f"SL {signal.stop_loss:.2f} | TP {signal.take_profit_primary:.2f} | RR {signal.risk_reward:.2f}"
        )

        if self.persistence:
            try:
                metadata = signal.metadata or {}
                self.persistence.save_signal({
                    'timestamp': payload['timestamp'],
                    'symbol': signal.symbol,
                    'current_price': signal.entry_price,
                    'signal': signal.direction,
                    'signal_type': direction_txt,
                    'confidence': signal.confidence,
                    'rsi': None,
                    'macd': None,
                    'macd_signal': None,
                    'sma_20': None,
                    'sma_50': None,
                    'price_change': None,
                    'price_change_pct': None,
                    'alert_level': 'ICT_ATM',
                    'alert_color': None,
                    'target_pips': None,
                    'success_rate': None,
                    'entry_price': signal.entry_price,
                    'stop_loss': signal.stop_loss,
                    'take_profit_1': signal.take_profit_primary,
                    'take_profit_2': signal.take_profit_secondary,
                    'take_profit_3': signal.take_profit_tertiary,
                    'risk_reward_ratio': signal.risk_reward,
                    'atr_value': metadata.get('atr_current'),
                    'position_size_percent': None,
                    'risk_amount_dollars': None,
                    'potential_profit_tp1': None,
                    'potential_profit_tp2': None,
                    'potential_profit_tp3': None,
                })
            except Exception as exc:
                print(f"⚠️ ICT ATM persist error: {exc}")

        can_trade = (
            self.autotrader
            and self.autotrader.enabled
            and self.trading_enabled
            and not spread_block
            and not atr_block
            and not self.event_mode_enabled
            and not self._is_blackout_or_off_session()
        )

        engine_mode = getattr(self, 'engine_mode', 'ALL')
        if engine_mode in {'NONE', 'FARMER_ONLY', 'LOW_ONLY', 'MEDIUM_ONLY', 'EVENT_ONLY'}:
            can_trade = False
        if not self.enable_high:
            can_trade = False

        if not can_trade:
            # Diagnostic logging for why trade was blocked
            block_reasons = []
            if not self.autotrader:
                block_reasons.append("No AutoTrader")
            elif not self.autotrader.enabled:
                block_reasons.append("AutoTrader disabled")
            if not self.trading_enabled:
                block_reasons.append("Trading disabled")
            if spread_block:
                block_reasons.append("Spread too wide")
            if atr_block:
                block_reasons.append("ATR too low")
            if self.event_mode_enabled:
                block_reasons.append("Event mode active")
            if self._is_blackout_or_off_session():
                block_reasons.append("Outside trading session")
            if engine_mode in {'NONE', 'FARMER_ONLY', 'LOW_ONLY', 'MEDIUM_ONLY', 'EVENT_ONLY'}:
                block_reasons.append(f"Engine mode: {engine_mode}")
            if not self.enable_high:
                block_reasons.append("HIGH engine disabled")
            
            reason_str = " | ".join(block_reasons) if block_reasons else "Unknown reason"
            print(f"⛔ [{datetime.now().strftime('%H:%M:%S')}] ICT ATM: Signal generated but blocked | {reason_str}")
            return

        if self.order_manager and getattr(self.order_manager, 'halt_new_orders', False):
            print(f"⏸️ [{datetime.now().strftime('%H:%M:%S')}] ICT ATM: Halt new orders (daily loss cap reached)")
            return

        # Use a distinct campaign bucket for ICT ATM so it doesn't compete with Swing
        atm_bucket = 'HIGH_ATM'
        if self.campaign and not self.campaign.allow(self.symbol, signal.direction, atm_bucket):
            current_count = self.campaign.current_count(self.symbol, signal.direction, atm_bucket) if self.campaign else 0
            max_count = self.campaign.max_per_level.get(atm_bucket, self.campaign.max_per_level.get('HIGH', 9)) if self.campaign else 9
            print(f"⛔ [{datetime.now().strftime('%H:%M:%S')}] ICT ATM: Campaign limit reached ({current_count}/{max_count} {atm_bucket} trades in window)")
            return

        try:
            trade = self.autotrader.place_market_order(
                signal.direction,
                signal.entry_price,
                signal.stop_loss,
                signal.take_profit_primary,
            )
        except Exception as exc:
            print(f"⚠️ ICT ATM auto-trade error: {exc}")
            return

        if not trade:
            return

        ticket = trade.get('ticket', 0)
        self.ict_atm_state['auto_last_ticket'] = ticket
        print(f"✅ [ICT ATM] Auto order sent ticket={ticket} lots={trade.get('volume', 0.0)}")

        if self.persistence:
            try:
                self.persistence.save_trade({
                    'timestamp': payload['timestamp'],
                    'symbol': self.symbol,
                    'direction': signal.direction,
                    'entry': signal.entry_price,
                    'sl': signal.stop_loss,
                    'tp': signal.take_profit_primary,
                    'lots': trade.get('volume', 0.0),
                    'ticket': ticket,
                    'status': 'SENT',
                    'alert_level': 'ICT_ATM',
                    'tier': 'ICT_ATM',
                    'engine': 'ICT_ATM'
                })
            except Exception as exc:
                print(f"⚠️ ICT ATM trade persist error: {exc}")

        if self.order_manager:
            try:
                self.order_manager.register_new_order(
                    ticket,
                    signal.direction,
                    signal.entry_price,
                    signal.stop_loss,
                    signal.take_profit_primary,
                    'ICT_ATM',
                    tier='ICT_ATM',
                )
            except Exception as exc:
                print(f"⚠️ Order manager ICT ATM error: {exc}")
        if self.campaign:
            self.campaign.record(self.symbol, signal.direction, atm_bucket)

# Example usage
if __name__ == "__main__":
    def signal_callback(signal: LiveSignal):
        # Get alert emoji based on level
        alert_emoji = {
            'HIGH': '🔴',
            'MEDIUM': '🟡', 
            'LOW': '🟢',
            'HOLD': '⭕'
        }.get(signal.alert_level, '⭕')
        
        print(f"🎯 NEW SIGNAL: {signal.signal_type} | ${signal.current_price:.2f} | Confidence: {signal.confidence:.1f}%")
        print(f"{alert_emoji} ALERT LEVEL: {signal.alert_level} | Target: {signal.target_pips} pips | Success Rate: {signal.success_rate:.1f}%")
        
        if signal.signal != 0:
            print(f"📊 RSI: {signal.rsi:.1f} | MACD: {signal.macd:.2f} | Price Change: {signal.price_change_pct:+.2f}%")
            print(f"📋 TRADE DETAILS:")
            print(f"   🎯 Entry: ${signal.entry_price:.2f}")
            print(f"   🛑 Stop Loss: ${signal.stop_loss:.2f}")
            print(f"   💰 TP1 ({signal.target_pips}p): ${signal.take_profit_1:.2f} (${signal.potential_profit_tp1:.0f} profit)")
            print(f"   💰 TP2 ({signal.target_pips*1.5:.0f}p): ${signal.take_profit_2:.2f} (${signal.potential_profit_tp2:.0f} profit)")
            print(f"   💰 TP3 ({signal.target_pips*2:.0f}p): ${signal.take_profit_3:.2f} (${signal.potential_profit_tp3:.0f} profit)")
            print(f"   📊 Risk/Reward: 1:{signal.risk_reward_ratio:.1f} | Position Size: {signal.position_size_percent:.1f}%")
            print("-" * 80)
    
    # Create and start live stream
    stream = LiveDataStream(symbol="GC=F", update_interval=30)
    stream.add_signal_callback(signal_callback)
    stream.start_streaming()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stream.stop_streaming()
        print("👋 Live streaming stopped by user")