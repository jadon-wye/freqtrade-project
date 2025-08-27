"""
이동평균 크로스오버 전략 구현
EX_COMP_02
- exit_signal 복원 여부에 따른 전략 수익률 비교
- 고정 파라미터: short_ema(10), long_ema(50), ROI(0.015), stoploss(-0.10), timeframe(15m)
- EX_COMP_01: ROI + SL + exit_signal
"""

from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce

class MovingAverageCrossStrategy(IStrategy):
    # 파라미터 선언
    ema_short_period = IntParameter(5, 20, default=10, space="buy", optimize=False)
    ema_long_period = IntParameter(25, 100, default=50, space="buy", optimize=False)

    timeframe = '15m'
    stoploss = -0.10
    minimal_roi = {"0": 0.015}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 동적 파라미터로 이동평균 계산
        short_period = self.ema_short_period.value
        long_period = self.ema_long_period.value

        dataframe[f'ema{short_period}'] = ta.EMA(dataframe, timeperiod=short_period) 
        dataframe[f'ema{long_period}'] = ta.EMA(dataframe, timeperiod=long_period)

        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        short = self.ema_short_period.value
        long = self.ema_long_period.value
        
        # 골든크로스일 경우 매수 신호 생성
        conditions = [] # 조건을 저장할 빈 리스트 생성
        conditions.append(dataframe[f'ema{short}'] > dataframe[f'ema{long}']) # 단기 이동평균선 > 장기 이동평균선(골든크로스)일 경우 True
        conditions.append(dataframe[f'ema{short}'].shift(1) <= dataframe[f'ema{long}'].shift(1)) # 바로 이전 캔들에서는 ema10이 ema50보다 작거나 같았을 경우
        conditions.append(dataframe[f'ema{short}'].notnull()) # ema10 값이 NaN이 아닌 경우만 신호 생성

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
                # 모든 조건이 True인 행의 'enter_long' 컬럼에 1(매수 신호) 할당

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        short = self.ema_short_period.value
        long = self.ema_long_period.value
        
        # 데드크로스일 경우 매도 신호 생성
        conditions = [] # 조건을 저장할 빈 리스트 생성
        conditions.append(dataframe[f'ema{short}'] < dataframe[f'ema{long}']) # 데드크로스일 경우 True
        conditions.append(dataframe[f'ema{short}'].shift(1) >= dataframe[f'ema{long}'].shift(1)) # 교차순간일 경우 True
        conditions.append(dataframe[f'ema{short}'].notnull()) # 결측치 제거

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions), 'exit_long'] = 1
                # 모든 조건이 True인 행의 'enter_exit' 컬럼에 1(매도 신호) 할당
        
        return dataframe