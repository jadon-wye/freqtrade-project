"""
이동평균 크로스오버 전략 구현 V1.1
V1.1 
- V1.x 버전에서는 short, long 기간만 바꾸며 실험 예정
- 실험에 용이하도록 각 파라미터별 변수화
- ema short = 5
- ema long = 50(고정)
"""

from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce

class MovingAverageCrossStrategy(IStrategy):
    # 파라미터 선언
    ema_short_period = IntParameter(5, 20, default=5, space="buy", optimize=False)
    ema_long_period = IntParameter(25, 100, default=50, space="buy", optimize=False)

    timeframe = '15m'
    # set the initial stoploss to -10%
    stoploss = -0.10
    # exit profitable positions at any time when the profit is greater than 1%
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