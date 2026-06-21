# Trading AI Pipeline

A full quantitative trading pipeline built in Python — from raw market data to automated 
buy/sell signals, backtesting, and performance reporting.

## How it works

**Step 1 — Data Fetching**
Pulls real historical OHLCV data (Open, High, Low, Close, Volume) from Yahoo Finance 
using yfinance for any ticker and date range.

**Step 2 — Processing**
Cleans raw price data and adds daily returns, log returns, and rolling volatility — 
turning raw prices into meaningful statistical information.

**Step 3 — Indicators**
Calculates four technical indicators on the processed data:
- Moving Averages (20 and 50 day) — trend direction
- RSI — momentum, overbought or oversold conditions
- MACD — momentum turning bullish or bearish
- Bollinger Bands — price position relative to its normal volatility range

**Step 4 — Signal Generation**
Two buy signals and one sell signal:
- Buy 1: MACD crosses above signal line, price in lower 65% of BB range, RSI below 75
- Buy 2: Price bounces off lower Bollinger Band with RSI below 40 (oversold bounce)
- Sell: MACD crosses below signal line, price in upper 50% of BB range, RSI above 30

**Step 5 — Backtesting**
Simulates trades on historical data accounting for position sizing (10% per trade), 
commission (0.1%) and slippage (0.05%). Tracks portfolio value daily.

**Step 6 — Metrics**
Reports industry standard quant performance metrics:
- Total and annualised return
- Sharpe ratio (risk adjusted returns)
- Maximum drawdown
- Win rate and profit factor

**Step 7 — Report**
Clean formatted report with honest verdict:
- Sharpe above 1.5 → STRONG
- Sharpe above 1.0 → MODERATE  
- Sharpe below 1.0 → WEAK

## Current performance

period           →  2018-01-01 to 2022-01-01 (AAPL)

strategy         →  MACD crossover + BB bounce, dual signal entry

exit             →  trailing ATR stop (3x) + MACD cross-down

regime filter    →  ADX > 15 (trending markets only)

parameters       →  BB threshold 0.70, RSI 65, ATR 3.0x, ADX 15
total return     →  17.63%

annual return    →  4.46%

sharpe ratio     →  1.58

sortino ratio    →  1.64

calmar ratio     →  1.42

max drawdown     →  -3.14%

win rate         →  70.00%

profit factor    →  6.99

total trades     →  21
verdict          →  ✅ STRONG — deploy with caution

## COVID crash stress test (Feb–Apr 2020)

To test the strategy under real crisis conditions, performance was isolated to the 
2020 COVID crash window — one of the fastest, sharpest drawdowns in modern market history.
AAPL price          →  -27.14% peak-to-trough during this window

portfolio value      →  -0.85% peak-to-trough during this window

trades during window →  1 (BUY on 2020-03-19, days before the actual market bottom)


## Train/test split — checking for overfitting

The original v8 result (Sharpe 1.58, STRONG) was found by running an ~80-combination 
parameter grid search across the full 2018-2022 dataset, then reporting performance on 
that same dataset. This is a known methodological problem: with enough parameter 
combinations tested, some will look strong by chance alone, regardless of whether the 
underlying edge is real.

To check this honestly, the dataset was split chronologically:


**Results:**

| Period | Sharpe | Return | Trades | Notes |
|--------|--------|--------|--------|-------|
| Train (optimized) | 0.51 | 1.73% | 12 | Best combination found on this window only |
| Full range (original, biased) | 1.58 | 17.63% | 21 | Optimized and reported on the same data |
| Test (out-of-sample, honest) | 1.15 | 2.80% | 3 | Parameters fixed from train, never re-tuned |

**Honest interpretation:** the original 1.58 Sharpe was partly inflated by searching 80 
parameter combinations on the data it was then reported against — a form of overfitting. 
The genuinely out-of-sample result is Sharpe 1.15, still a real, respectable MODERATE 
result, not noise. The strategy shows real (if more modest) edge on data it never saw 
during optimization, but the corrected, defensible claim is "Sharpe in the 1.0-1.2 
range, MODERATE" — not the original STRONG verdict. The test sample is also very small 
(3 trades), which limits how much confidence to place in this single result; a longer 
or rolling test window would give a more reliable estimate.

This is the difference between a backtest result and a validated strategy. The first is 
easy to produce. The second requires checking your own work this way before trusting it 
with real capital.


## Performance progression

| Version | Strategy | Trades | Sharpe | Return | Win Rate | Verdict |
|---------|----------|--------|--------|--------|----------|---------|
| v1 | MA crossover | 17 | 0.63 | 6.05% | 62.5% | WEAK |
| v2 | MACD + BB confluence | 8 | 0.86 | 4.82% | 100% | WEAK |
| v3 | MACD + BB, relaxed threshold | 12 | 1.13 | 7.44% | 100% | MODERATE |
| v4 | Dual signal: MACD + BB bounce | 14 | 1.06 | 7.87% | 100% | MODERATE |
| v5 | + Fixed stop loss (5%) | 26 | 0.92 | 6.86% | 61.5% | WEAK |
| v6 | + Trailing ATR stop (3x) | 22 | 1.00 | 8.01% | 54.5% | MODERATE |
| v7 | + Parameter optimisation (BB 0.70, RSI 65) | 25 | 1.14 | 9.61% | 58.3% | MODERATE |
| v8 | + ADX regime filter, tested on 2018-2022 | 21 | 1.58 | 17.63% | 70.0% | **STRONG** |

**Key insight from v8:** 

the same strategy logic produced very different results across 
different market periods. On 2020-2024 (dominated by a strong AAPL bull run), the strategy 
underperformed buy-and-hold significantly. On 2018-2022 (a more mixed period including the 
COVID crash), the strategy hit a STRONG verdict with excellent risk-adjusted metrics. This is 
an honest and important finding: the strategy's edge appears strongest in genuinely volatile, 
non-trending-forever markets — not in extended one-way bull runs where buy-and-hold simply 
wins by default.

## Limitations and known failure modes

- **Single asset, single timeframe** — only tested on AAPL daily candles. Not yet validated 
  across multiple assets or timeframes.

- **No leverage, financing, or capacity modelling** — backtest assumes unlimited liquidity 
  and fixed commission/slippage regardless of position size.

- **No correlation analysis** — unknown how this strategy's returns correlate with broader 
  market indices or other strategies during stress periods.

- **Small sample of trades** — 21 trades over 4 years is a limited sample; results should be 
  treated as a strong signal, not statistical certainty.

- **Regime dependent** — performs best in markets with sufficient trend strength (ADX > 15). 
  In prolonged low-volatility, sideways markets, the strategy generates few or no signals.



## How to run
```bash
pip install yfinance pandas numpy ta
python3 main.py
```

## Configuration
All parameters in `config.py` — change ticker, dates, capital, position size, 
commission and indicator periods from one place.

## What I learned
Building this trading AI was my first real step into quantitative engineering — 
and it taught me more about what I don't know than what I do. The pipeline itself 
is solid: data fetching, processing, indicators, signal generation, backtesting, 
metrics and reporting all connected and working. But running it humbled me. The 
first strategy — MA crossover — looked clean in code and returned results, but 
only 6% over 4 years while the market made 50%. The problem wasn't the code, it 
was the thinking. Moving averages are lagging — by the time they signal a move 
the move has already happened. Switching to MACD and Bollinger Bands improved the 
quality immediately — 100% win rate, better drawdown, higher Sharpe — but now the 
strategy is too conservative, missing most of the market's moves by sitting in cash. 
The deeper lesson was about data leakage: code can run perfectly, print good numbers, 
and still be lying to you because future information is bleeding into past decisions. 
Learning to see those problems before they cost real money is the actual skill. 
This is version one. The signals get better, the parameters get optimised, 
live broker integration comes next — and so does the real test.

## Next steps
- Add stop losses for better risk management
- Optimise parameters using walk-forward validation
- Add forex data (GBP/USD, USD pairs)
- Live broker integration via OANDA API
- Automatic execution and deployment

## Built with
- Python
- yfinance
- pandas
- ta (technical analysis)
- numpy