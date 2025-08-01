# 전략 실험 관리 시스템

## 실험 진행 순서
1. 이동평균 크로스오버 (SMA/EMA) ★★★
2. RSI 과매수/과매도 ★★★  
3. 볼린저밴드 ★★★
4. MACD ★★☆
5. 모멘텀 (ROC) ★★☆
6. 브레이크아웃 ★★☆
7. 이동평균+RSI/볼린저 조합 ★★☆
8. Stochastic Oscillator ★☆☆
9. ADX ★☆☆
10. SuperTrend ★☆☆

## 각 전략별 폴더 구조
```
experiments/
├── 01_moving_average/
│   ├── strategy_v1.py
│   ├── config_v1.json
│   ├── results/
│   └── analysis.md
├── 02_rsi/
└── ...
```

## 실험 기록 템플릿
각 전략마다 analysis.md 파일에 다음 내용 기록:
- 전략 개념 및 구현 방법
- 파라미터 실험 결과
- 백테스팅 성과 지표
- 개선점 및 다음 단계