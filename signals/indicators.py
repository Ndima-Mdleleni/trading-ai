# signals/indicators.py
# Technical indicators calculated on processed OHLCV data
# Single responsibility: compute indicators, nothing else

import pandas as pd
import ta
import logging
from config import config

logger = logging.getLogger(__name__)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators to processed dataframe.
    - Moving averages (trend)
    - RSI (momentum)
    - MACD (trend + momentum)
    - Bollinger Bands (volatility)
    """
    df = df.copy()
    cfg = config.indicators

    # moving averages
    df["ma_fast"] = ta.trend.sma_indicator(df["Close"], window=cfg.ma_fast)
    df["ma_slow"] = ta.trend.sma_indicator(df["Close"], window=cfg.ma_slow)

    # RSI — momentum oscillator 0 to 100
    df["rsi"] = ta.momentum.rsi(df["Close"], window=cfg.rsi_period)

    # MACD — trend following momentum
    macd = ta.trend.MACD(
        df["Close"],
        window_fast=cfg.macd_fast,
        window_slow=cfg.macd_slow,
        window_sign=cfg.macd_signal
    )
    df["macd"]        = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"]   = macd.macd_diff()

    # Bollinger Bands — volatility bands around price
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_mid"]   = bb.bollinger_mavg()

    df["atr"] = ta.volatility.average_true_range(
        df["High"], df["Low"], df["Close"], window=14
    )

    # drop rows with NaN from indicator warmup period
    df.dropna(inplace=True)

    logger.info(f"added indicators, {len(df)} rows remaining")
    return df


if __name__ == "__main__":
    from data.fetcher import fetch_ohlcv
    from data.processor import process

    df = fetch_ohlcv()
    df = process(df)
    df = add_indicators(df)

    print(df[["Close", "ma_fast", "ma_slow", "rsi", "macd"]].tail())
    print(f"\nshape: {df.shape}")
    print(f"columns: {list(df.columns)}")