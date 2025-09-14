"""
RSI 과매수/과매도 전략 구현
RSI-B-03
- RSI 전략 실험 
- RSI 진입조건을 조정(RSI < 30, RSI < 35, RSI < 40)하며 진입신호와 WinRate 관찰
- 현재 RSI 진입조건: RSI < 40
- Exit 방식은 ROI와 SL로 통일

"""

from freqtrade.strategy import IStrategy, CategoricalParameter
from pandas import DataFrame
import talib.abstract as ta

class RSIOverboughtOversoldStrategy(IStrategy):
    timeframe = '15m'
    # ROI와 SL은 0.015, -0.10으로 통일한다.
    minimal_roi = {
        "0":0.015
    }
    stoploss = -0.10

    rsi_threshold = CategoricalParameter([25, 30, 35, 40], default=40, space="buy", optimize=False)
    # RSI 진입조건 변경값. => 30, 35, 40으로 비교 실험

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
        # 현재는 Exit_Signal을 ROI와 SL로만 수행중이므로 비워둠.
        return dataframe
