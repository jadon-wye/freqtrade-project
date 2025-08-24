# FreqAI 전략 실험 프로젝트

FreqAI 알고리즘 최적화를 위한 체계적인 전략 실험 및 연구 프로젝트입니다.

## 프로젝트 목표

- 다양한 전통적 트레이딩 전략들을 직접 구현하며 학습
- 각 전략의 성과를 체계적으로 분석하고 기록
- 최종적으로 FreqAI와 결합하여 최적의 알고리즘 개발

## 실험 계획

### 전통적 전략 구현 순서
1. **이동평균 크로스오버** (SMA/EMA) 
2. **RSI 과매수/과매도** 
3. **볼린저밴드** 
4. **MACD** 
5. **모멘텀** (ROC) 
6. **브레이크아웃** 
7. **이동평균+RSI/볼린저 조합** 
8. **Stochastic Oscillator** 
9. **ADX** 
10. **SuperTrend** 

## 프로젝트 구조

```
ft_userdata/
├── user_data/
│   ├── strategies/
│   │   ├── main/                   # 현재 실험 중인 전략
|   |   |   └── MovingAverageCrossStrategy.py
│   │   ├── experiments/            # 전략 실험 폴더
│   │   │   ├── MA_Cross/           # 이동평균 실험
│   │   │   │   ├── v1.0.py         # 이동평균 버전 1.0 실험 
|   |   |   |   └── v1.1.py         # 이동평균 버전 1.1 실험
│   │   │   ├── 02_rsi/             # RSI 실험
│   │   │   └── ...
│   │   ├── archived/               # 실패한 전략 or 백업
|   |   └── MA_Cross_v1_failed.py
│   ├── config.json                 # 기본 설정 (Git 추적)
│   ├── config.secrets.json         # 민감한 정보 (Git 제외)
│   └── ...
├── docker-compose.yml
└── README.md
```

### 설정 파일 관리
- **config.json**: 기본 실험 설정 (Git으로 추적)
- **config.secrets.json**: API 키, 토큰 등 민감한 정보 (Git 제외)
- **실험별 설정**: 각 전략 폴더에 버전별 설정 파일들

### 버전 관리법
- MA_cCross 실험을 하던 중 버전관리가 안됨을 느껴 버전명을 체계적으로 관리하기 위한 방안을 고안
```
ver-[전략이름]-[실험이름]-[주요조건]
```
해당 체계로 버전명만으로 어떤 실험을 진행하였는지 확인할 수 있음

## 시작하기

### 1. 환경 설정
```bash
# Docker 환경 시작
docker compose up -d

# 시장 데이터 다운로드
docker exec freqtrade freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframes 5m --days 60
```

### 2. 전략 백테스팅
```bash
# 전략 백테스팅 실행
docker exec freqtrade freqtrade backtesting --config user_data/config.json --strategy [전략명] --timerange 20240101-20240301
```

## 실험 기록

각 전략별 실험 결과는 해당 폴더의 `analysis.md` 파일에 기록됩니다.

### 주요 성과 지표
- **총 수익률**: 전체 기간 수익률
- **샤프 비율**: 위험 대비 수익률 (1.0 이상 양호)
- **최대 손실(MDD)**: 최대 낙폭
- **승률**: 수익 거래 비율
- **수익 팩터**: 총 수익 / 총 손실 (1.0 이상 필요)

## 기술 스택

- **Freqtrade**: 암호화폐 거래봇 프레임워크
- **FreqAI**: 머신러닝 확장
- **Docker**: 컨테이너화된 실행 환경
- **Python**: 전략 구현 언어
- **Git**: 버전 관리

## 실험 진행 상황

- [ ] 01. 이동평균 크로스오버
- [ ] 02. RSI 과매수/과매도
- [ ] 03. 볼린저밴드
- [ ] 04. MACD
- [ ] 05. 모멘텀 (ROC)
- [ ] 06. 브레이크아웃
- [ ] 07. 조합 전략
- [ ] 08. Stochastic Oscillator
- [ ] 09. ADX
- [ ] 10. SuperTrend

## 주의사항

- 이 프로젝트는 **연구 및 학습 목적**입니다
- 실제 투자에 사용하기 전에 충분한 검증이 필요합니다
- 모든 실험은 **모의거래(dry run)** 환경에서 진행됩니다

## 라이선스

이 프로젝트는 개인 학습 목적으로 만들어졌습니다.