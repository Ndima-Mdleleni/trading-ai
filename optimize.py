# optimize.py
# Multi-parameter optimisation — finds best combination for maximum Sharpe
# Tests all combinations of BB threshold, RSI level and ATR multiplier

import itertools
from data.fetcher import fetch_ohlcv
from data.processor import process
from signals.indicators import add_indicators
from signals.generator import generate_signals
from backtest.engine import run_backtest
from backtest.metrics import calculate_metrics
from config import config

# fetch data once — reuse for all combinations
print("fetching data...\n")
df_raw = fetch_ohlcv()
df_raw = process(df_raw)
df_raw = add_indicators(df_raw)

# parameter ranges to scan
bb_thresholds  = [0.55, 0.60, 0.65, 0.70, 0.75]
rsi_levels     = [65, 70, 75, 80]
atr_multipliers = [2.5, 3.0, 3.5, 4.0]

results = []
total   = len(bb_thresholds) * len(rsi_levels) * len(atr_multipliers)
count   = 0

print(f"scanning {total} combinations...\n")

for bb, rsi, atr in itertools.product(bb_thresholds, rsi_levels, atr_multipliers):
    count += 1

    # update config
    config.backtest.atr_multiplier = atr

    # run pipeline with current parameters
    import signals.generator as sg
    df = df_raw.copy()

    # temporarily patch thresholds
    df["signal"] = 0
    df["bb_position"] = (df["Close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])
    df["bb_bounce"] = (
        (df["bb_position"] > 0.1) &
        (df["bb_position"].shift(1) <= 0.1)
    )
    df["macd_cross_up"] = (
        (df["macd"] > df["macd_signal"]) &
        (df["macd"].shift(1) <= df["macd_signal"].shift(1))
    )
    df["macd_cross_down"] = (
        (df["macd"] < df["macd_signal"]) &
        (df["macd"].shift(1) >= df["macd_signal"].shift(1))
    )

    df.loc[df["macd_cross_up"] & (df["bb_position"] <= bb) & (df["rsi"] < rsi), "signal"] = 1
    df.loc[df["bb_bounce"] & (df["rsi"] < 40), "signal"] = 1
    df.loc[df["macd_cross_down"] & (df["bb_position"] >= 0.5) & (df["rsi"] > 30), "signal"] = -1
    df["position"] = df["signal"].replace(0, None).ffill().fillna(0)

    df, trades = run_backtest(df)
    metrics    = calculate_metrics(df, trades)

    sharpe = float(metrics["sharpe_ratio"])
    results.append({
        "bb":     bb,
        "rsi":    rsi,
        "atr":    atr,
        "sharpe": sharpe,
        "return": metrics["total_return"],
        "trades": metrics["total_trades"],
        "winrate": metrics["win_rate"]
    })

    if count % 10 == 0:
        print(f"progress: {count}/{total}")

# sort by sharpe
results.sort(key=lambda x: x["sharpe"], reverse=True)

print("\n--- TOP 5 COMBINATIONS ---\n")
for r in results[:5]:
    print(f"BB {r['bb']}  RSI {r['rsi']}  ATR {r['atr']}x  →  Sharpe {r['sharpe']:.2f}  Return {r['return']}  Trades {r['trades']}  WinRate {r['winrate']}")

best = results[0]
print(f"\nbest combination:")
print(f"  bb_threshold:    {best['bb']}")
print(f"  rsi_level:       {best['rsi']}")
print(f"  atr_multiplier:  {best['atr']}")
print(f"  sharpe:          {best['sharpe']:.2f}")
print(f"  return:          {best['return']}")
