import contextlib
import threading
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch
import pandas as pd
from src.live_data_stream import LiveDataStream


class FarmerIntegrationTests(unittest.TestCase):
    def test_trade_gate_continue_still_reconciles_and_waits(self):
        stream = LiveDataStream.__new__(LiveDataStream)
        stream.symbol,stream.update_interval='XAUUSDm',0
        stream._stream_lock=threading.RLock()
        stream.stream_thread=None
        stream._stream_generation=0
        stream._stop_event=NS(set=Mock())
        stream.is_running=False
        stream._log_status=stream._log_trade=Mock()
        stream.config={'filters':{'min_atr_pips':0}}
        stream.historical_data=pd.DataFrame(columns=['Open','High','Low','Close','Volume'])
        stream.spread_analyzer=None
        stream.autotrader=NS(enabled=True,market_context={})
        stream.trading_enabled=True
        stream.order_manager=NS(halt_new_orders=True,reconcile=Mock())
        stream.persistence=None
        stream.event_mode_enabled=False
        stream.event_engine=None
        stream._is_blackout_or_off_session=lambda:False
        stream._process_farmer=Mock()
        quote={'price':100,'spread_points':2,'timestamp':datetime.now(timezone.utc),'source':'MT5'}
        stream._fetch_current_quote=Mock(side_effect=[quote,None])
        stream._update_historical_data=Mock()
        stream._generate_live_signal=Mock(return_value=NS(signal=1,alert_level='HIGH',timestamp='now',symbol='XAUUSDm',current_price=100,signal_type='BUY',confidence=90))
        stream._notify_callbacks=Mock()
        stream.nyupip_enabled=True
        stream.nyupip_state={}
        stream.nyupip_strategy=NS(evaluate=Mock(return_value=[]),get_last_diagnostics=lambda:{'status':'hold','reason':'no_module_triggered'})
        stream.ict_swing_enabled=stream.ict_atm_enabled=False
        waits=[]
        class Event:
            def __init__(self): self.flag=False
            def is_set(self): return self.flag
            def set(self): self.flag=True
            def wait(self,timeout):
                waits.append(timeout)
                self.flag=True
        class Thread:
            def __init__(self,target,**kw): self.target=target
            def start(self): self.target()
            def is_alive(self): return False
        with patch('src.live_data_stream.threading.Event',Event),patch('src.live_data_stream.threading.Thread',Thread):
            stream.start_streaming()
        self.assertEqual(stream._fetch_current_quote.call_count,1)
        stream.order_manager.reconcile.assert_called_once()
        self.assertEqual(waits,[0])
        stream.nyupip_strategy.evaluate.assert_called_once()

    def test_all_mode_enables_the_separate_gold_switches_without_arming(self):
        stream=LiveDataStream.__new__(LiveDataStream)
        stream.symbol='XAUUSDm'
        stream._farmer_default_enabled=True
        stream.trading_enabled=False
        stream.set_nyupip_enabled=Mock()
        stream.set_ict_swing_enabled=Mock()
        stream.set_ict_atm_enabled=Mock()
        stream.set_engine_mode('ALL')
        stream.set_nyupip_enabled.assert_called_once_with(True)
        stream.set_ict_swing_enabled.assert_called_once_with(True)
        stream.set_ict_atm_enabled.assert_called_once_with(True)
        self.assertFalse(stream.trading_enabled)

    def test_farmer_wait_reason_is_visible_without_forcing_an_order(self):
        stream=LiveDataStream.__new__(LiveDataStream)
        stream.config={}
        stream.symbol='XAUUSDm'
        stream._log_trade=Mock()
        stream.farmer_enabled=stream.trading_enabled=True
        stream.event_mode_enabled=False
        stream.engine_mode='ALL'
        stream._is_blackout_or_off_session=lambda:False
        stream.autotrader=NS(enabled=True,place_market_order=Mock())
        stream.persistence=object()
        stream._get_nyupip_history=lambda:pd.DataFrame()
        stream.farmer_strategy=NS(evaluate=lambda bars:None,diagnostics={'reason':'no_confirmed_pullback'})
        stream._process_farmer({},False,False)
        self.assertEqual(stream.strategy_decisions['FARMER']['reason'],'no_confirmed_pullback')
        stream.autotrader.place_market_order.assert_not_called()

    def test_dashboard_risk_scenario_uses_actual_equity_and_configured_budget(self):
        stream=LiveDataStream.__new__(LiveDataStream)
        stream.config={'risk':{'risk_percent_per_trade':.25}}
        stream.mt5=NS(get_equity=lambda:1000.)
        stream._log_status=Mock()
        result=stream._calculate_risk_management(100,1,pd.Series({'ATR_14':1.}),{'alert_level':'HIGH','target_pips':4})
        self.assertEqual(result['risk_amount_dollars'],2.5)
        self.assertEqual(result['position_size_percent'],.25)

    def test_farmer_can_trade_with_high_engine_disabled_and_no_ensemble_signal(self):
        stream = LiveDataStream.__new__(LiveDataStream)
        stream.symbol='XAUUSDm'
        stream.farmer_enabled=stream.trading_enabled=True
        stream.enable_high=False
        stream.event_mode_enabled=False
        stream.engine_mode='FARMER_ONLY'
        stream._is_blackout_or_off_session=lambda:False
        stream._get_nyupip_history=lambda:pd.DataFrame()
        stream._log_trade=Mock()
        stream.farmer_strategy=NS(evaluate=Mock(return_value={'direction':1,'sl':99,'setup_id':'FARMER:BAR:1'}),diagnostics={})
        stream.autotrader=NS(enabled=True,place_market_order=Mock(return_value={'ticket':1,'price':100.02,'volume':.01,'sl':99,'tp':102.17}))
        stream.config={'broker':{'login':1}}
        stream.persistence=NS(save_signal=Mock(),save_trade=Mock(),setup_was_traded=Mock(return_value=False))
        stream.order_manager=NS(register_new_order=Mock())
        quote={'bid':100.,'ask':100.02,'timestamp':datetime.now(timezone.utc),'source':'MT5'}
        stream._process_farmer(quote,False,False)
        stream.autotrader.place_market_order.assert_called_once()
        self.assertEqual(stream.persistence.save_trade.call_args.args[0]['engine'],'FARMER')
        self.assertEqual(stream.persistence.save_trade.call_args.args[0]['tp'],102.17)
        self.assertEqual(stream.order_manager.register_new_order.call_args.args[5],'FARMER')

    def test_refresh_replaces_quote_candles_with_completed_broker_bars(self):
        stream=LiveDataStream.__new__(LiveDataStream)
        stream._nyupip_history_limit=4800
        stream._history_limit_default=400
        stream.autotrader=NS(market_context={})
        stream.ignore_session_filter=False
        stream.spread_analyzer=None
        stream.indicators=NS(calculate_all_indicators=lambda x:x)
        stream._quiet_status_stdout=contextlib.nullcontext
        idx=pd.date_range('2026-10-27T08:00Z',periods=120,freq='min')
        rates=[{'time':t.timestamp(),'open':100,'high':105,'low':95,'close':101,'tick_volume':7} for t in idx]
        stream.mt5=NS(get_rates=lambda *args:rates)
        quote={'source':'MT5','timestamp':pd.Timestamp('2026-10-27T09:59:30Z'),'price':999}
        with patch.dict('sys.modules',{'MetaTrader5':NS(TIMEFRAME_M1=1)}):
            stream._update_historical_data(quote)
            stream._update_historical_data(quote)
        self.assertEqual(len(stream.historical_data),119)
        self.assertEqual(stream.historical_data.iloc[-1].High,105)
        self.assertTrue(stream.autotrader.market_context['history_ready'])


if __name__ == '__main__': unittest.main()
