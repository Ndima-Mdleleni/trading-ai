import pandas as pd
import numpy as np 
import logging

logger = logging.getLogger(__name__)


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate trading signals using MACD + Bollinger Band confluence.

    BUY  (1)  when:
        - MACD line crosses above signal line (momentum turning bullish)
        - price is at or below BB midline (good entry, not overextended)
        - RSI is not overbought (below 70)

    SELL (-1) when:
        - MACD line crosses below signal line (momentum turning bearish)
        - price is at or above BB midline (good exit, not oversold)
        - RSI is not oversold (above 30)
    """
    df = df.copy()

    df["macd_cross_up"] = (
        (df["macd"] > df["macd_signal"]) &
        (df["macd"].shift(1) <= df["macd_signal"].shift(1))
    )

    df["macd_cross_down"] = (
        (df["macd"] < df["macd_signal"]) &
        (df["macd"].shift(1) >= df["macd_signal"].shift(1))
    )


    df["bb_position"] = (df["Close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

    df["bb_bounce"] = (
        (df["bb_position"] > 0.1) &
        (df["bb_position"].shift(1) <= 0.1)
    )

    df["regime"] = "ranging"
    df.loc[df["adx"] > 15, "regime"] = "trending"

    df["signal"] = 0

    df.loc[
        df["macd_cross_up"] &
        (df["bb_position"] <= 0.70) &
        (df["rsi"] < 65) &
        (df["regime"] == "trending"),
        "signal"
    ] = 1

    df.loc[
        df["bb_bounce"] &
        (df["rsi"] < 40) &
        (df["regime"] == "trending"),
        "signal"
    ] = 1

    df.loc[
    df["macd_cross_down"] &
    (df["bb_position"] >= 0.5) &
    (df["rsi"] > 30),
    "signal"
] = -1

    df["position"] = df["signal"].replace(0, np.nan).ffill().fillna(0)
    
    buy_signals = (df["signal"] == 1).sum()
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

    signals = df[df["signal"] != 0][["Close", "signal", "rsi", "bb_position", "macd_signal"]]
    print(signals)
    print(f"\ntotal signals: {len(signals)}")
    print(df["regime"]. value_counts())

    buy_and_hold = (df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]
    print(f"\nbuy and hold return: {buy_and_hold:.2%}")
    print(f"first price: {df['Close'].iloc[0]:.2f}")
    print(f"last price:  {df['Close'].iloc[-1]:.2f}")