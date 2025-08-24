"""
이동평균 크로스오버 전략 구현 rsl_l_04
rsl_l_04
- ROI = 0.005(빠른 익절), 0.01(기준 익절), 0.015(더 큰 수익추구)
- stoploss = -0.03(빠른 손절), -0.05(중간 손절), -0.10(느린 손절)
- 목표: EXIT => ROI & Stoploss only
- 이번 실험에서의 값: ROI = 0.01, stoploss = -0.03
- ema short = 10(고정)
- ema long = 50(고정)
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
 
    stoploss = -0.03

    minimal_roi = {"0": 0.01}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 동적 파라미터로 이동평균 계산
        short_period = self.ema_short_period.value
        long_period = self.ema_long_period.value

        # 7기간(캔들) 이동평균선과 20기간(캔들) 이동평균선 생성
        dataframe[f'ema{short_period}'] = ta.EMA(dataframe, timeperiod=short_period) # dataframe의 close컬럼(종가)으로 10기간(캔들)의 지수이동평균을 계산하는 코드
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
        # exit_signal이 전략 로직에서의 조건으로 항상 실행되어 ROI나 SL이 도달하기 전에 손절이 발생함
        # 과감히 전략 로직의 exit_signal을 없앰
        return dataframe