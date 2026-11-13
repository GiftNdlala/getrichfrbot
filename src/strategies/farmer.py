"""Experimental M1 trend-pullback worker; no promise of a profitable edge."""
import pandas as pd


class FarmerStrategy:
    def __init__(self):
        self.last_bar = None
        self.diagnostics = {'reason': 'waiting_for_completed_bar'}

    def evaluate(self, bars):
        if bars is None or len(bars) < 60:
            self.diagnostics = {'reason': 'insufficient_history'}
            return None
        if self.last_bar == bars.index[-1]:
            self.diagnostics['reason'] = 'waiting_for_completed_bar'
            return None
        self.last_bar = bars.index[-1]
        recent = bars.tail(60)
        if not (recent.index.to_series().diff().dropna() == pd.Timedelta(minutes=1)).all():
            self.diagnostics = {'reason': 'history_gap'}
            return None
        close = bars['Close']
        fast, slow = close.ewm(span=20, adjust=False).mean(), close.ewm(span=50, adjust=False).mean()
        prev, last = bars.iloc[-2], bars.iloc[-1]
        tr = pd.concat([bars.High-bars.Low, (bars.High-close.shift()).abs(), (bars.Low-close.shift()).abs()], axis=1).max(axis=1)
        atr = float(tr.tail(14).mean())
        trend = 'LONG' if fast.iloc[-1] > slow.iloc[-1] and fast.iloc[-1] > fast.iloc[-4] else ('SHORT' if fast.iloc[-1] < slow.iloc[-1] and fast.iloc[-1] < fast.iloc[-4] else 'FLAT')
        self.diagnostics = {'reason':'no_confirmed_pullback','closed_bar':str(self.last_bar),'trend_bias':trend,
            'pullback_touched':bool(prev.Low <= fast.iloc[-2]) if trend=='LONG' else bool(prev.High >= fast.iloc[-2]) if trend=='SHORT' else False,
            'confirmation_closed':bool(last.Close > prev.High) if trend=='LONG' else bool(last.Close < prev.Low) if trend=='SHORT' else False}
        side = 0
        if fast.iloc[-1] > slow.iloc[-1] and fast.iloc[-1] > fast.iloc[-4] and prev.Low <= fast.iloc[-2] and last.Close > prev.High:
            side = 1
        elif fast.iloc[-1] < slow.iloc[-1] and fast.iloc[-1] < fast.iloc[-4] and prev.High >= fast.iloc[-2] and last.Close < prev.Low:
            side = -1
        if side == 0 or atr <= 0:
            return None
        stop = float(bars.Low.tail(5).min() - 0.1*atr) if side == 1 else float(bars.High.tail(5).max() + 0.1*atr)
        self.diagnostics = {'reason': 'candidate', 'bar': str(self.last_bar), 'direction': side}
        return {'direction': side, 'sl': stop, 'setup_id': f'FARMER:{self.last_bar.isoformat()}:{side}'}
