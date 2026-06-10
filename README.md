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
This was my first bridge into quant level engineering which is my ultimate goal. 
The pieces are intricate but grounded in simple mathematics. The hard part is that 
code can look right, run properly, and print good results — but those results can be 
misleading when current data leaks into the training process, making numbers look 
strong in testing but weak in deployment. I'm building my eye for those kinds of 
issues and learning to identify problems in the process earlier so I spend more time 
building than debugging. This project is intentionally scalable — the goal is to 
refine the signals, add live broker integration, and deploy it as a fully automated 
system.

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