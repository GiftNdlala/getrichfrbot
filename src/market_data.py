"""Canonical UTC broker candles. MT5 rate timestamps denote bar OPEN times."""
import pandas as pd


def utc_timestamp(value):
    return pd.Timestamp(value).tz_localize('UTC') if pd.Timestamp(value).tzinfo is None else pd.Timestamp(value).tz_convert('UTC')


def broker_frame(rates, now):
    frame = pd.DataFrame(rates)
    if frame.empty:
        raise ValueError('BROKER_HISTORY_UNAVAILABLE')
    frame.index = pd.to_datetime(frame['time'], unit='s', utc=True)
    frame = frame.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'})
    frame = frame[['Open', 'High', 'Low', 'Close', 'Volume']].sort_index()
    frame = frame[~frame.index.duplicated(keep='last')]
    frame = frame.loc[frame.index + pd.Timedelta(minutes=1) <= utc_timestamp(now)]
    if frame.empty or utc_timestamp(now) - (frame.index[-1] + pd.Timedelta(minutes=1)) > pd.Timedelta(minutes=2):
        raise ValueError('BROKER_HISTORY_STALE')
    if frame.isna().any().any() or (frame[['Open', 'High', 'Low', 'Close']] <= 0).any().any():
        raise ValueError('BROKER_HISTORY_INVALID')
    return frame


def closed_bars(data, rule, now):
    """Aggregate open-labelled M1 bars; return only fully elapsed HTF bars."""
    frame = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    frame.index = pd.to_datetime(frame.index, utc=True)
    frame = frame.loc[frame.index + pd.Timedelta(minutes=1) <= utc_timestamp(now)]
    bars = frame.resample(rule, label='left', closed='left').agg(
        {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
    # M1 input is required: gaps must not masquerade as complete candles.
    counts = frame['Close'].resample(rule, label='left', closed='left').count()
    duration = pd.Timedelta(rule)
    return bars.loc[(bars.index + duration <= utc_timestamp(now)) & (counts == duration / pd.Timedelta(minutes=1))].dropna()


def confirmed_retest(data, now, level, direction, tolerance, after=None):
    """A completed M1 reaction after a zone touch; a hypothesis, not proof of edge."""
    frame = data.copy()
    frame.index = pd.to_datetime(frame.index, utc=True)
    frame = frame.loc[frame.index + pd.Timedelta(minutes=1) <= utc_timestamp(now)].tail(5)
    if len(frame) < 5 or not (frame.index.to_series().diff().dropna() == pd.Timedelta(minutes=1)).all():
        return False
    if after is not None and frame.index[0] < utc_timestamp(after):
        return False
    touched = ((frame.Low <= level + tolerance) & (frame.High >= level - tolerance)).any()
    last, previous = frame.iloc[-1], frame.iloc[-2]
    if direction == 1:
        return bool(touched and last.Close > last.Open and last.Close > previous.High and last.Close > level)
    return bool(touched and last.Close < last.Open and last.Close < previous.Low and last.Close < level)
