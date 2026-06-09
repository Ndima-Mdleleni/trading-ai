from dataclasses import dataclass, field
from typing import List

@dataclass
class DataConfig:
    ticker: str = "AAPL"
    start_date: str = "2020-01-01"
    end_date: str = "2024-01-01"
    interval: str = "1d"

@dataclass
class IndicatorConfig:
    ma_fast: int = 20
    ma_slow: int = 50
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9

@dataclass
class BacktestConfig:
    initial_capital: float = 100_000.0
    position_size: float = 0.1
    commission: float = 0.001
    slippage: float = 0.0005

@dataclass
class Config:
    data: DataConfig = None
    indicators: IndicatorConfig = None
    backtest: BacktestConfig = None

    def __post_init__(self):
        self.data = self.data or DataConfig()
        self.indicators = self.indicators or IndicatorConfig()
        self.backtest = self.backtest or BacktestConfig()

config = Config()