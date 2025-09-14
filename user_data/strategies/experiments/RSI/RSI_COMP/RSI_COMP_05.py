"""
RSI 과매수/과매도 전략 구현
RSI-COMP-05
- RSI 전략 실험 - 탈출 조건 조정 
- RSI 탈출조건을 조정하며 진입신호와 Total Profit과 exit_signal을 관찰
- 현재 RSI 탈출조건: RSI > 75
- 진입 방식은 RSI < 40으로 통일
"""

from freqtrade.strategy import IStrategy, CategoricalParameter, IntParameter
from pandas import DataFrame
import talib.abstract as ta


class RSIOverboughtOversoldStrategy(IStrategy):
    timeframe = '15m'
    minimal_roi = {} # ROI 비활성화
    stoploss = -0.99 # stoploss 비활성화

    rsi_threshold = CategoricalParameter([25, 30, 35, 40], default=40, space="buy", optimize=False)
    # RSI 진입조건 RSI < 40으로 통일

    rsi_exit = IntParameter(60, 75, default=75, space="sell", optimize=True)
    # RSI 탈출조건

    def populate_indicators(self, dataframe: DataFrame, metadta: dict) -> DataFrame:
        # 동적 파라미터로 RSI 계산. timeperiod는 14로 설정(기본값)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 진입 조건 설정
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_threshold.value) &
            (dataframe['rsi'].notnull()),
            'enter_long'
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 탈출 조건 설정
        dataframe.loc[
            (dataframe['rsi'] > self.rsi_exit.value) &
            (dataframe['rsi'].notnull()),
            'exit_long'
        ] = 1
        return dataframe
