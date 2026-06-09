# signals/generator.py
# Generates buy/sell signals from technical indicators
# Single responsibility: take indicator data, return signal column

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate trading signals based on indicator combinations.

    Signal logic:
    - BUY  (1)  when fast MA crosses above slow MA AND RSI < 70
    - SELL (-1) when fast MA crosses below slow MA AND RSI > 30
    - HOLD (0)  otherwise

    Returns dataframe with added signal columns.
    """
    df = df.copy()

    # MA crossover — fast crosses above slow
    df["ma_cross_up"]   = (
        (df["ma_fast"] > df["ma_slow"]) &
        (df["ma_fast"].shift(1) <= df["ma_slow"].shift(1))
    )

    # MA crossover — fast crosses below slow
    df["ma_cross_down"] = (
        (df["ma_fast"] < df["ma_slow"]) &
        (df["ma_fast"].shift(1) >= df["ma_slow"].shift(1))
    )

    # raw signal
    df["signal"] = 0
    df.loc[df["ma_cross_up"]   & (df["rsi"] < 70), "signal"] =  1
    df.loc[df["ma_cross_down"] & (df["rsi"] > 30), "signal"] = -1

    # position — carries signal forward until next crossover
    df["position"] = df["signal"].replace(0, np.nan).ffill().fillna(0)

    buy_signals  = (df["signal"] ==  1).sum()
    sell_signals = (df["signal"] == -1).sum()
    logger.info(f"generated {buy_signals} buy signals and {sell_signals} sell signals")

    return df


if __name__ == "__main__":
    from data.fetcher import fetch_ohlcv
    from data.processor import process
    from signals.indicators import add_indicators

    df = fetch_ohlcv()
    df = process(df)
    df = add_indicators(df)
    df = generate_signals(df)

    signals = df[df["signal"] != 0][["Close", "signal", "rsi", "ma_fast", "ma_slow"]]
    print(signals)
    print(f"\ntotal signals: {len(signals)}")