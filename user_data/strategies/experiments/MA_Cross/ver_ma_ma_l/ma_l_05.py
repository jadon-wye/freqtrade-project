"""
이동평균 크로스오버 전략 구현 ver_ma_ma_l_05
ver_ma_ma_l_05
- MA 파라미터 최적화 실험
- 진입 조건을 판단하는 골든크로스 실험이므로 exit_signal을 의도적으로 제거
- 매도 신호는 오직 이전 실험에서의 최적값인 ROI/SL에 의해서만 결정
- 목표: 단기 EMA / 장기 EMA 비율이 수익에 어떤 영향을 미치는가
- 이번 실험에서의 값: (Short EMA, Long EMA) = (15, 80) => 상당히 보수적
- ROI = 0.015(고정)
- loss = -0.10(고정)
"""

"""
┌───────────────────────────┐
│        진입 조건           │
│   EMA(short) > EMA(long)  │ ← 실험에서 이 기간 조합을 튜닝
└───────────────────────────┘
             │
             ▼
  포지션 오픈 (LONG 진입)
             │
 ┌──────────────┬──────────────┐
 │   ROI 도달   │  Stoploss 도달 │
 │   → 익절     │   → 손절       │
 └──────────────┴──────────────┘
             │
         포지션 종료
"""

from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce

class MovingAverageCrossStrategy(IStrategy):
    # 파라미터 선언
    ema_short_period = IntParameter(5, 20, default=15, space="buy", optimize=False)
    ema_long_period = IntParameter(25, 100, default=80, space="buy", optimize=False)

    timeframe = '15m' 
    stoploss = -0.10
    minimal_roi = {"0": 0.015}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 동적 파라미터로 이동평균 계산
        short_period = self.ema_short_period.value
        long_period = self.ema_long_period.value

        # Short(캔들) 이동평균선과 Long(캔들) 이동평균선 생성
        dataframe[f'ema{short_period}'] = ta.EMA(dataframe, timeperiod=short_period) # dataframe의 close컬럼(종가)으로 캔들의 지수이동평균을 계산하는 코드
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
        # 골든크로스로 인한 진입 영향만 보는 실험이므로
        # ROI/SL로 탈출 전략을 일정하게 가져가기 위해
        # exit_signal을 의도적으로 제거
        return dataframe