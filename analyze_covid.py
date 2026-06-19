from data.fetcher import fetch_ohlcv
from data.processor import process
from signals.indicators import add_indicators
from signals.generator import generate_signals
from backtest.engine import run_backtest

df = fetch_ohlcv()
df = process(df)
df = add_indicators(df)
df = generate_signals(df)
df, trades = run_backtest(df)

covid = df.loc["2020-02-01":"2020-04-30"]

price_start = covid["Close"].iloc[0]
price_min   = covid["Close"].min()
price_end   = covid["Close"].iloc[-1]
price_drop  = (price_min - price_start) / price_start

portfolio_start = covid["portfolio_value"].iloc[0]
portfolio_min   = covid["portfolio_value"].min()
portfolio_drop  = (portfolio_min - portfolio_start) / portfolio_start

print("--- COVID CRASH STRESS TEST ( Feb-Apr 2020) ---\n")
print(f"AAPL price:      {price_start:.2f}")
print(f"AAPL max drop:   {price_drop:.2%}")
print()
print(f"Portfolio value: {portfolio_start:.2f}")
print(f"Portfolio max drop:  {portfolio_drop:.2%}")

covid_trades = trades[(trades["date"] >= "2020-02-01") & (trades["date"] <= "2020-04-30")]
print(f"\ntrades during this window: {len(covid_trades)}")
if len(covid_trades) > 0:
    print(covid_trades.to_string(index=False))
else:
    print("(no trades - strategy was likely in cash or holding through this period)")