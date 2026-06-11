# backtest/metrics.py
# Calculates performance metrics from backtest results
# Single responsibility: take backtest dataframe, return metrics dict

import pandas as pd
import numpy as np
import logging
from config import config

logger = logging.getLogger(__name__)


def calculate_metrics(df: pd.DataFrame, trades: pd.DataFrame) -> dict:
    """
    Calculate standard quantitative performance metrics.
    - Total return
    - Annualised return
    - Sharpe ratio
    - Max drawdown
    - Win rate
    - Profit factor
    """
    initial  = config.backtest.initial_capital
    final    = df["portfolio_value"].iloc[-1]

    # total return
    total_return = (final - initial) / initial

    # annualised return
    days   = (df.index[-1] - df.index[0]).days
    years  = days / 365.25
    ann_return = (1 + total_return) ** (1 / years) - 1

    # daily returns of portfolio
    port_returns = df["portfolio_value"].pct_change().dropna()

    # sharpe ratio — annualised, assumes 0% risk free rate
    sharpe = (port_returns.mean() / port_returns.std()) * np.sqrt(252)

    # max drawdown
    max_drawdown = df["drawdown"].min()

    # trade level metrics
    if len(trades) >= 2:
        buys  = trades[trades["action"] == "BUY"].reset_index(drop=True)
        exits = trades[trades["action"].isin(["SELL", "TRAIL STOP"])].reset_index(drop=True)
        n     = min(len(buys), len(exits))

        pnl   = (exits["price"].values[:n] - buys["price"].values[:n]) * buys["shares"].values[:n]
        wins  = (pnl > 0).sum()
        win_rate     = wins / n if n > 0 else 0
        gross_profit = pnl[pnl > 0].sum()
        gross_loss   = abs(pnl[pnl < 0].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    else:
        win_rate = profit_factor = 0

    metrics = {
        "total_return":    f"{total_return:.2%}",
        "annual_return":   f"{ann_return:.2%}",
        "sharpe_ratio":    f"{sharpe:.2f}",
        "max_drawdown":    f"{max_drawdown:.2%}",
        "win_rate":        f"{win_rate:.2%}",
        "profit_factor":   f"{profit_factor:.2f}",
        "total_trades":    len(trades),
        "final_value":     f"${final:,.2f}"
    }

    return metrics


if __name__ == "__main__":
    from data.fetcher import fetch_ohlcv
    from data.processor import process
    from signals.indicators import add_indicators
    from signals.generator import generate_signals
    from backtest.engine import run_backtest

    df         = fetch_ohlcv()
    df         = process(df)
    df         = add_indicators(df)
    df         = generate_signals(df)
    df, trades = run_backtest(df)
    metrics    = calculate_metrics(df, trades)

    print("\n--- performance metrics ---")
    for key, val in metrics.items():
        print(f"{key:<20} {val}")