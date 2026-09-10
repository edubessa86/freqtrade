# pragma pylint: disable=invalid-name, missing-docstring
import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy import IStrategy
import talib.abstract as ta

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
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=200)
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
