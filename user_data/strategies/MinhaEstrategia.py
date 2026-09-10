# pragma pylint: disable=invalid-name, missing-docstring
import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy import IStrategy

class MinhaEstrategia(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.05,
        "30": 0.03,
        "60": 0.01
    }

    stoploss = -0.10

    timeframe = '5m'

    startup_candle_count: int = 30

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Cálculo do RSI via Pandas puro (sem dependência C do TA-Lib)
        delta = dataframe['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # Médias móveis exponenciais (EMA) via Pandas
        dataframe['ema_fast'] = dataframe['close'].ewm(span=50, adjust=False).mean()
        dataframe['ema_slow'] = dataframe['close'].ewm(span=200, adjust=False).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 30) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 70) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1
        return dataframe
