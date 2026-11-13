"""Fail-closed execution policy. Called under the process-wide MT5 lock."""
from datetime import datetime, timezone
import json
import math
from pathlib import Path


MAGIC = 20250923
# A DONE response may precede position visibility. Never free this slot on time alone.
ACKNOWLEDGED_ORDERS = {}


def epoch(value):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if isinstance(value, datetime):
        return value.replace(tzinfo=timezone.utc).timestamp() if value.tzinfo is None else value.timestamp()
    return float(value)


def news_reason(config, now):
    if not config.get('enabled', True):
        return None
    try:
        path = Path(config.get('calendar_file', 'data/news_calendar.json'))
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[1] / path
        payload = json.loads(path.read_text(encoding='utf-8'))
        if not epoch(payload['valid_from']) <= now <= epoch(payload['valid_until']):
            return 'NEWS_CALENDAR_STALE'
        for event in payload['events']:
            if event.get('currency') != 'USD' or event.get('impact') != 'HIGH':
                continue
            delta = (now - epoch(event['timestamp'])) / 60
            if -float(config.get('pre_blackout_minutes', 30)) <= delta <= float(config.get('post_blackout_minutes', 15)):
                return 'NEWS_BLACKOUT:' + event['name']
    except (OSError, ValueError, KeyError, TypeError):
        return 'NEWS_CALENDAR_UNAVAILABLE'
    return None


def money_at_stop(api, symbol, side, volume, entry, stop):
    value = api.order_calc_profit(side, symbol, volume, entry, stop)
    if value is None or not math.isfinite(value):
        raise ValueError('RISK_CALCULATION_UNAVAILABLE')
    return max(0.0, -float(value))


def floor_volume(raw, info):
    step, minimum = float(info.volume_step), float(info.volume_min)
    if not math.isfinite(raw) or raw + 1e-10 < minimum or step <= 0:
        return 0.0
    return round(minimum + math.floor((min(raw, float(info.volume_max)) - minimum + 1e-10) / step) * step, 8)


def usd_account_rate(api, account, now=None):
    """Account currency per USD, using a fresh broker conversion pair."""
    currency = str(account.currency).upper()
    if currency == 'USD':
        return 1.0
    now = now if now is not None else datetime.now(timezone.utc).timestamp()
    candidates = api.symbols_get() if hasattr(api, 'symbols_get') else None
    for info in candidates or ():
        base, quote = getattr(info, 'currency_base', ''), getattr(info, 'currency_profit', '')
        direct = base == 'USD' and quote == currency
        inverse = base == currency and quote == 'USD'
        if not (direct or inverse):
            continue
        if not api.symbol_select(info.name, True):
            continue
        tick = api.symbol_info_tick(info.name)
        if not tick:
            continue
        bid, ask = float(tick.bid), float(tick.ask)
        if not all(math.isfinite(v) and v > 0 for v in (bid, ask)) or ask < bid:
            continue
        if not -2 <= now-float(tick.time) <= 60 or ask/bid > 1.05:
            continue
        # Conservative liquidation value of USD; never use a hard-coded FX rate.
        return bid if direct else 1.0/ask
    raise ValueError('USD_CONVERSION_UNAVAILABLE:' + currency)


def execution_snapshot(api, cfg, symbol, context, tick, account, strategy, now=None, usd_rate=None):
    """Validate all broker/account reads and return budgets for this proposal."""
    now = now if now is not None else datetime.now(timezone.utc).timestamp()
    ex, risk = cfg.get('execution', {}), cfg.get('risk', {})
    if account is None or not math.isfinite(float(account.equity)) or account.equity <= 0:
        raise ValueError('ACCOUNT_UNAVAILABLE')
    if ex.get('demo_only', True) and account.trade_mode != api.ACCOUNT_TRADE_MODE_DEMO:
        raise ValueError('DEMO_ACCOUNT_REQUIRED')
    if cfg.get('broker', {}).get('login') and int(account.login) != int(cfg['broker']['login']):
        raise ValueError('ACCOUNT_MISMATCH')
    if context.get('source') != 'MT5' or not context.get('history_ready'):
        raise ValueError('BROKER_DATA_REQUIRED')
    if cfg.get('sessions') and not context.get('ignore_session_filter', False):
        import pytz
        from datetime import timedelta
        sessions = cfg['sessions']
        local = datetime.fromtimestamp(now, pytz.timezone(sessions['timezone']))
        start_h, start_m = map(int, sessions['trade_start'].split(':'))
        end_h, end_m = map(int, sessions['trade_end'].split(':'))
        clock, start_clock, end_clock = local.hour*60+local.minute, start_h*60+start_m, end_h*60+end_m
        days = sessions['days']
        if end_clock >= start_clock:
            allowed = local.strftime('%a') in days and start_clock <= clock <= end_clock
        else:
            allowed = (clock >= start_clock and local.strftime('%a') in days) or (clock <= end_clock and (local-timedelta(days=1)).strftime('%a') in days)
        if not allowed:
            raise ValueError('OUTSIDE_SESSION')
    if not context.get('audit_ready'):
        raise ValueError('AUDIT_STORAGE_REQUIRED')
    age_limit = float(ex.get('max_quote_age_seconds', 15))
    for ts in (epoch(context['timestamp']), float(tick.time)):
        if not -2 <= now - ts <= age_limit:
            raise ValueError('QUOTE_STALE')
    info = api.symbol_info(symbol)
    if not info or not all(math.isfinite(float(v)) and float(v) > 0 for v in (info.point, tick.bid, tick.ask)) or tick.ask < tick.bid:
        raise ValueError('QUOTE_INVALID')
    spread = (tick.ask - tick.bid) / info.point
    if spread > float(cfg.get('filters', {}).get('max_spread_points', 40)):
        raise ValueError('SPREAD_CAP')
    normal = context.get('normal_spread_points')
    if normal and spread > float(normal) * float(cfg.get('filters', {}).get('spread_spike_multiplier', 2)):
        raise ValueError('SPREAD_SPIKE')
    reason = news_reason(cfg.get('news', {}), now)
    if reason:
        raise ValueError(reason)
    positions, orders = api.positions_get(), api.orders_get()
    if positions is None or orders is None:
        raise ValueError('EXPOSURE_UNAVAILABLE')
    if orders:
        raise ValueError('POSITION_CAP:PENDING_ORDER')
    # Account-wide UTC-day loss, including floating losses and all booked costs.
    end = datetime.fromtimestamp(now, timezone.utc)
    start = end.replace(hour=0, minute=0, second=0, microsecond=0)
    deals = api.history_deals_get(start, end)
    if deals is None:
        raise ValueError('DAILY_HISTORY_UNAVAILABLE')
    visible = {getattr(p, 'identifier', p.ticket) for p in positions} | {p.ticket for p in positions}
    reserved_risk = 0.0
    reserved_symbol_risk = 0.0
    reserved_count = 0
    for (login, ticket), reserved in list(ACKNOWLEDGED_ORDERS.items()):
        if login != account.login:
            continue
        pid = reserved.get('position_id', ticket)
        # An order ticket is not necessarily the broker's position identifier.
        opening = next((d for d in deals if getattr(d, 'order', None) == ticket or (reserved.get('deal') and getattr(d, 'ticket', None) == reserved['deal'])), None)
        if opening is None and reserved.get('deal'):
            opening = next(iter(api.history_deals_get(ticket=reserved['deal']) or ()), None)
        if opening is not None:
            pid = getattr(opening, 'position_id', None) or pid
            reserved['position_id'] = pid
        if pid in visible or ticket in visible:
            continue  # Broker position accounts for risk exactly once.
        history = api.history_deals_get(position=pid)
        exits = [d for d in (history or []) if getattr(d, 'position_id', None) == pid and getattr(d, 'entry', None) in (1, 3)]
        if exits and sum(float(d.volume) for d in exits) >= reserved['volume'] - 1e-8:
            del ACKNOWLEDGED_ORDERS[(login, ticket)]
        else:
            reserved_count += 1
            reserved_risk += reserved['risk']
            if reserved.get('symbol', symbol) == symbol:
                reserved_symbol_risk += reserved['risk']
    if len(positions) + reserved_count >= int(risk.get('max_concurrent_trades', 1)):
        raise ValueError('POSITION_CAP')
    farmer = strategy.startswith('FARMER')
    farmer_reserve = risk.get('farmer_reserve', {})
    farmer_active = any('FARMER' in getattr(p, 'comment', '') for p in positions) or any('FARMER' in r.get('strategy', '') for (login, _), r in ACKNOWLEDGED_ORDERS.items() if login == account.login)
    if not farmer and not farmer_active and len(positions)+reserved_count >= int(risk.get('max_concurrent_trades', 1))-int(farmer_reserve.get('slots', 0)):
        raise ValueError('POSITION_CAP:FARMER_RESERVED')
    if getattr(account, 'margin_mode', None) in (0, 1) and (any(p.symbol == symbol for p in positions) or reserved_symbol_risk > 0):
        raise ValueError('NETTING_POSITION_EXISTS')
    # Funding, credit, corrections and bonuses are capital flows, not trading P&L.
    # This also permits a freshly funded demo account on its first day.
    net = sum(sum(float(getattr(d, k, 0.0) or 0.0) for k in ('profit', 'commission', 'swap', 'fee')) for d in deals if getattr(d, 'type', 0) not in (2, 3, 5, 6))
    baseline = float(account.balance) - net
    if not math.isfinite(baseline) or baseline <= 0:
        raise ValueError('DAILY_BASELINE_INVALID')
    loss_pct = max(0.0, (baseline - float(account.equity)) / baseline * 100)
    if loss_pct >= float(risk.get('daily_loss_limit_pct', 2.0)):
        raise ValueError('DAILY_LOSS_CAP')
    mult = 1.0
    defense = risk.get('progressive_defense', {})
    if defense.get('enabled', True):
        for tier in sorted(defense.get('loss_tiers', []), key=lambda t: t['realized_loss_pct']):
            if loss_pct >= float(tier['realized_loss_pct']):
                mult = min(mult, float(tier['position_size_mult']))
    fc = ex.get('farmer', {})
    if farmer:
        usd_rate = usd_account_rate(api, account, now) if usd_rate is None else usd_rate
        history = [d for d in deals if getattr(d, 'magic', None) == MAGIC and 'FARMER' in getattr(d, 'comment', '')]
        if history and now - max(float(d.time) for d in history) < float(fc.get('cooldown_seconds', 120)):
            raise ValueError('FARMER_COOLDOWN')
        # Resolve exit legs by position_id; broker-generated exit comments omit FARMER.
        ids = {getattr(d, 'position_id', None) for d in history} - {None}
        # Include Farmer positions opened before today's history window.
        for d in deals:
            pid = getattr(d, 'position_id', None)
            if pid and getattr(d, 'entry', None) in (1, 3) and pid not in ids:
                legs = api.history_deals_get(position=pid)
                if legs is None:
                    raise ValueError('FARMER_HISTORY_UNAVAILABLE')
                if any(getattr(leg, 'magic', None) == MAGIC and 'FARMER' in getattr(leg, 'comment', '') for leg in legs):
                    ids.add(pid)
        farmer_legs = [d for d in deals if getattr(d, 'position_id', None) in ids]
        if farmer_legs and now - max(float(d.time) for d in farmer_legs) < float(fc.get('cooldown_seconds', 120)):
            raise ValueError('FARMER_COOLDOWN')
        farmer_net = sum(sum(float(getattr(d, k, 0.0) or 0.0) for k in ('profit', 'commission', 'swap', 'fee')) for d in deals if getattr(d, 'position_id', None) in ids)
        if farmer_net <= -float(fc.get('daily_loss_dollars', 5)) * usd_rate:
            raise ValueError('FARMER_DAILY_LOSS_CAP')
    risk_pct = min(float(risk.get('risk_percent_per_trade', 0.25)), float(fc.get('risk_percent_per_trade', 0.1))) if farmer else float(risk.get('risk_percent_per_trade', 0.25))
    budget = account.equity * risk_pct / 100 * mult
    if farmer:
        budget = min(budget, float(fc.get('max_loss_dollars', 2)) * usd_rate)
    # Stop risk for every existing account position, irrespective of engine/magic.
    open_risk = reserved_risk
    symbol_risk = reserved_symbol_risk
    for p in positions:
        if not p.sl:
            raise ValueError('UNPROTECTED_POSITION')
        position_risk = money_at_stop(api, p.symbol, p.type, p.volume, p.price_open, p.sl)
        # Preserve estimated costs after the acknowledged fill becomes visible.
        reservation = next((r for (login, ticket), r in ACKNOWLEDGED_ORDERS.items() if login == account.login and (ticket == p.ticket or r.get('position_id') == getattr(p, 'identifier', p.ticket))), None)
        if reservation is not None:
            position_risk += float(reservation.get('cost_buffer', 0))
        else:
            cost_usd = float(fc.get('estimated_round_trip_cost_dollars', .15)) if 'FARMER' in getattr(p, 'comment', '') else float(risk.get('cost_buffer_dollars', 0))
            if cost_usd:
                position_risk += cost_usd * (usd_rate if usd_rate is not None else usd_account_rate(api, account, now))
        open_risk += position_risk
        if p.symbol == symbol:
            symbol_risk += position_risk
    symbol_cap = risk.get('symbol_caps', {}).get(symbol, {}).get('max_open_risk_pct', risk.get('max_open_risk_pct', 0.5))
    max_risk = account.equity * float(risk.get('max_open_risk_pct', 0.5)) / 100
    reserve_cash = account.equity * float(farmer_reserve.get('risk_pct', 0)) / 100 if not farmer and not farmer_active else 0.0
    remaining_daily = max(0.0, baseline * float(risk.get('daily_loss_limit_pct', 2)) / 100 - max(0.0, baseline - account.equity))
    budget = min(budget, max_risk - open_risk - reserve_cash, account.equity*float(symbol_cap)/100-symbol_risk, remaining_daily)
    if budget <= 0:
        raise ValueError('RISK_BUDGET_EXHAUSTED')
    return budget, farmer
