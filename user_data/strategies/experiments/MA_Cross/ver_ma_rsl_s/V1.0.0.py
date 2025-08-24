"""
이동평균 크로스오버 전략 구현 V1
V1: 가장 기본적인 구조임. 실제 사용하기는 힘들며 앞으로의 실험에 base가 될 파일.
"""

from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce

class MovingAverageCrossStrategy(IStrategy):

    timeframe = '15m'

    # set the initial stoploss to -10%
    stoploss = -0.10

    # exit profitable positions at any time when the profit is greater than 1%
    minimal_roi = {"0": 0.01}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 10기간(캔들) 이동평균선과 50기간(캔들) 이동평균선 생성
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10) # dataframe의 close컬럼(종가)으로 10기간(캔들)의 지수이동평균을 계산하는 코드
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)

        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 골든크로스일 경우 매수 신호 생성
        conditions = [] # 조건을 저장할 빈 리스트 생성
        conditions.append(dataframe['ema10'] > dataframe['ema50']) # 단기 이동평균선 > 장기 이동평균선(골든크로스)일 경우 True
        conditions.append(dataframe['ema10'].shift(1) <= dataframe['ema50'].shift(1)) # 바로 이전 캔들에서는 ema10이 ema50보다 작거나 같았을 경우
        conditions.append(dataframe['ema10'].notnull()) # ema10 값이 NaN이 아닌 경우만 신호 생성

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
                # 모든 조건이 True인 행의 'enter_long' 컬럼에 1(매수 신호) 할당

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 데드크로스일 경우 매도 신호 생성
        conditions = [] # 조건을 저장할 빈 리스트 생성
        conditions.append(dataframe['ema10'] < dataframe['ema50']) # 데드크로스일 경우 True
        conditions.append(dataframe['ema10'].shift(1) >= dataframe['ema50'].shift(1)) # 교차순간일 경우 True
        conditions.append(dataframe['ema10'].notnull()) # 결측치 제거

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions), 'exit_long'] = 1
                # 모든 조건이 True인 행의 'enter_exit' 컬럼에 1(매도 신호) 할당
        
        return dataframe