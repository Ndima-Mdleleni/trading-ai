# backtest/engine.py
# Simulates trading based on generated signals
# Single responsibility: execute signals, track portfolio, return results

import pandas as pd
import numpy as np
import logging
from config import config

logger = logging.getLogger(__name__)


def run_backtest(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate trading on historical data using generated signals.
    Accounts for position sizing, commission, slippage and trailing ATR stop.
    Returns dataframe with portfolio value tracked over time.
    """
    df    = df.copy()
    cfg   = config.backtest

    capital       = cfg.initial_capital
    position      = 0.0
    cash          = capital
    portfolio_val = capital
    entry_price   = 0.0
    trailing_stop = 0.0

    portfolio_values = []
    trade_log        = []

    for date, row in df.iterrows():
        price    = row["Close"]
        signal   = row["signal"]
        atr      = row["atr"]
        cost     = price * (1 + cfg.commission + cfg.slippage)
        proceeds = price * (1 - cfg.commission - cfg.slippage)

        # BUY signal — enter long position
        if signal == 1 and position == 0:
            shares_to_buy  = (cash * cfg.position_size) / cost
            cash          -= shares_to_buy * cost
            position      += shares_to_buy
            entry_price    = price
            trailing_stop  = price - (3 * atr)
            trade_log.append({
                "date":   date,
                "action": "BUY",
                "price":  price,
                "shares": shares_to_buy,
                "cash":   cash
            })
            logger.debug(f"BUY  {shares_to_buy:.2f} shares at {price:.2f}")

        # TRAILING STOP — update and check
        elif position > 0 and entry_price > 0:
            new_stop = price - (3 * atr)
            if new_stop > trailing_stop:
                trailing_stop = new_stop

            if price < trailing_stop:
                cash += position * proceeds
                trade_log.append({
                    "date":   date,
                    "action": "TRAIL STOP",
                    "price":  price,
                    "shares": position,
                    "cash":   cash
                })
                logger.debug(f"TRAIL STOP {position:.2f} shares at {price:.2f}")
                position      = 0.0
                entry_price   = 0.0
                trailing_stop = 0.0

        # SELL signal — exit position
        elif signal == -1 and position > 0:
            cash += position * proceeds
            trade_log.append({
                "date":   date,
                "action": "SELL",
                "price":  price,
                "shares": position,
                "cash":   cash
            })
            logger.debug(f"SELL {position:.2f} shares at {price:.2f}")
            position      = 0.0
            entry_price   = 0.0
            trailing_stop = 0.0

        # track portfolio value
        portfolio_val = cash + (position * price)
        portfolio_values.append(portfolio_val)

    df["portfolio_value"] = portfolio_values
    df["cash"]            = cash
    df["drawdown"]        = (
        df["portfolio_value"] / df["portfolio_value"].cummax() - 1
    )

    trades = pd.DataFrame(trade_log)
    logger.info(f"backtest complete — {len(trades)} trades executed")

    return df, trades


if __name__ == "__main__":
    from data.fetcher import fetch_ohlcv
    from data.processor import process
    from signals.indicators import add_indicators
    from signals.generator import generate_signals

    df         = fetch_ohlcv()
    df         = process(df)
    df         = add_indicators(df)
    df         = generate_signals(df)
    df, trades = run_backtest(df)

    print("\n--- trades ---")
    print(trades.to_string(index=False))
    print(f"\nfinal portfolio value: ${df['portfolio_value'].iloc[-1]:,.2f}")
    print(f"starting capital:      ${config.backtest.initial_capital:,.2f}")