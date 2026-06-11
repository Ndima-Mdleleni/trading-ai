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

## Performance progression

| Version | Strategy | Trades | Sharpe | Return | Win Rate | Verdict |
|---------|----------|--------|--------|--------|----------|---------|
| v1 | MA crossover | 17 | 0.63 | 6.05% | 62.5% | WEAK |
| v2 | MACD + BB confluence | 8 | 0.86 | 4.82% | 100% | WEAK |
| v3 | MACD + BB, relaxed threshold | 12 | 1.13 | 7.44% | 100% | MODERATE |
| v4 | Dual signal: MACD + BB bounce | 14 | 1.06 | 7.87% | 100% | MODERATE |
| v5 | + Fixed stop loss (5%) | 26 | 0.92 | 6.86% | 61.5% | WEAK |
| v6 | + Trailing ATR stop (3x) | 22 | 1.00 | 8.01% | 54.5% | MODERATE |

**Key improvements from v1 to v6:**
- Sharpe ratio improved from 0.63 to 1.00
- Returns improved from 6.05% to 8.01%
- Max drawdown reduced from -3.45% to -2.31%
- Profit factor improved from 3.32 to 5.01
- Added intelligent trailing stop loss that locks in profits
- Strategy consistently holds MODERATE verdict


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