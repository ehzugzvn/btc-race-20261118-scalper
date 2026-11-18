"""Median Scalper: mean reversion against noisy cbBTC pool prints.

Strategy (agent-fun/bars-replay/v1, hello / batch / orders / bar):
- Track recent closes; the median of the last MEDIAN_WINDOW closes is the
  fair-value anchor and an EMA over 240 closes is the trend guard.
- Buy only when flat and the close dips DIP_BPS below the median, unless
  price has collapsed far below the EMA (falling knife: skip).
- Sell when the reversion completes or risk limits trigger.
Deterministic, stdlib only: no clock, no randomness, no network.
"""
import os
import sys
from statistics import median

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"
MAX_SLIPPAGE_BPS = 150

# Tunable parameters (tuned on the frozen dev window).
DIP_BPS = 35
MEDIAN_WINDOW = 30
HISTORY = 45
EMA_SPAN = 240
KNIFE_BPS = 150
TAKE_PROFIT_BPS = 60
STOP_LOSS_BPS = 50
MAX_HOLD_BARS = 90
COOLDOWN_BARS = 5

_closes = []
_ema = None
_ema_warm = []
_entry_seq = None
_last_sell_seq = None
_was_holding = False


def _update_ema(close):
    global _ema
    alpha = 2.0 / (EMA_SPAN + 1)
    if _ema is None:
        _ema_warm.append(close)
        if len(_ema_warm) >= EMA_SPAN:
            _ema = sum(_ema_warm) / len(_ema_warm)
        return
    _ema = _ema + alpha * (close - _ema)


def _current_median():
    if len(_closes) < MEDIAN_WINDOW:
        return None
    return median(_closes[-MEDIAN_WINDOW:])


def on_batch(state, batch):
    global _entry_seq, _was_holding, _last_sell_seq
    fresh = None
    for bar in batch["bars"]:
        if bar["symbol"] == SYMBOL:
            fresh = bar
    if fresh is None:
        return []
    close = int(fresh["c"])
    _closes.append(close)
    if len(_closes) > 300:
        del _closes[: len(_closes) - 300]
    _update_ema(close)
    if state.warming_up:
        return []

    held = state.positions.get(SYMBOL)
    holding = held is not None and held.qty > 0
    if holding and not _was_holding:
        _entry_seq = state.seq
    if not holding:
        _entry_seq = None
    _was_holding = holding

    med = _current_median()
    if med is None or _ema is None:
        return []

    if not holding:
        # Buy the dip: close far enough below the median to cover the
        # ~26 bps round-trip cost, but not in a collapse below the EMA.
        if _last_sell_seq is not None and state.seq - _last_sell_seq < COOLDOWN_BARS:
            return []
        dip_limit = med * (1.0 - DIP_BPS / 10000.0)
        knife_floor = _ema * (1.0 - KNIFE_BPS / 10000.0)
        if close <= dip_limit and close >= knife_floor:
            if state.cash >= 1000000:
                return [{
                    "side": "buy",
                    "symbol": SYMBOL,
                    "notional_quote_units": state.cash,
                    "max_slippage_bps": MAX_SLIPPAGE_BPS,
                }]
        return []

    # Holding: exit on completed reversion, take-profit, hard stop, or timeout.
    value = state.value(SYMBOL, held.qty)
    gain_bps = 0.0
    if held.cost > 0:
        gain_bps = (value - held.cost) * 10000.0 / held.cost
    held_bars = 0
    if _entry_seq is not None:
        held_bars = state.seq - _entry_seq
    should_sell = (
        close >= med
        or gain_bps >= TAKE_PROFIT_BPS
        or gain_bps <= -STOP_LOSS_BPS
        or held_bars >= MAX_HOLD_BARS
    )
    if should_sell:
        _last_sell_seq = state.seq
        return [{
            "side": "sell",
            "symbol": SYMBOL,
            "qty": held.qty,
            "max_slippage_bps": MAX_SLIPPAGE_BPS,
        }]
    return []


if __name__ == "__main__":
    makefun_bars.run(on_batch)
