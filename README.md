# Trading AI Pipeline

A full quantitative trading pipeline built in Python — from raw market data to automated 
buy/sell signals, backtesting, and performance reporting.

## What it does
Fetches real market data, calculates technical indicators, generates trading signals, 
simulates trades on historical data, and produces a clean performance report with 
industry standard metrics.

## Pipeline
1. **Data** — fetches OHLCV data from Yahoo Finance via `yfinance`
2. **Processing** — cleans data, adds returns and volatility
3. **Indicators** — Moving Averages, RSI, MACD, Bollinger Bands
4. **Signals** — generates buy/sell signals from indicator combinations
5. **Backtest** — simulates trades with commission, slippage and position sizing
6. **Metrics** — Sharpe ratio, max drawdown, win rate, profit factor
7. **Report** — clean formatted performance report with verdict

## How to run
pip install yfinance pandas numpy ta

python3 main.py

## Configuration
All parameters are in `config.py` — change ticker, dates, capital, 
position size, commission and indicator periods from one place.

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
- Improve signal quality for higher Sharpe ratio
- Add forex data (GBP/USD, USD pairs)
- Live broker integration via OANDA API
- Automatic execution and deployment
- Paper trading validation before live capital

## Built with
- Python
- yfinance
- pandas
- ta (technical analysis)
- numpy