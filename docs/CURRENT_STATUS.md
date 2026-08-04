# Scientific Calculator Current Status

> 이 문서는 `SCIENTIFIC_CALCULATOR_DEVELOPMENT_ROADMAP.md`의 세부 진행 상태를 빠르게 복원하기 위한 최신 체크포인트다.

## Current phase

```text
Python 기본 계산 엔진       완료
공학 함수                  완료
Ans / DEG / RAD / GRAD     완료
NORM / FIX / SCI / S⇔D     완료
SHIFT 버튼 라벨 전환       완료
이차방정식 모드            완료
1변수 통계 모드            완료
복소수 모드                완료
C++ Qt 병렬 구현           다음 작업
```

## Latest completed feature

### Complex mode

MODE 메뉴에서 `Complex`를 선택하면 다음 두 입력 방식을 지원한다.

```text
Rectangular: a + bj
Polar:       r ∠ θ
```

전자공학 표기 관례에 따라 허수 단위는 `j`로 표시한다.

지원 결과:

- 직교형 `a + bj`
- 극형 `r ∠ θ`
- 크기 `|z|`
- 위상각 `arg(z)`
- 켤레복소수
- 직교형 → 극형 변환
- 극형 → 직교형 변환
- DEG / RAD / GRAD 동기화
- NORM / FIX / SCI 동기화
- 음수 크기 및 잘못된 입력 오류 처리

관련 구조:

```text
ComplexPage
↓
ComplexController
↓
ComplexCalculator
↓
AngleConverter + ResultFormatter
```

## Python implementation status

Python 버전의 핵심 모드가 모두 실제 화면과 연결되었다.

```text
CALC  기본·공학 계산
STAT  1변수 통계
EQN   이차방정식
CMPLX 복소수 직교형·극형 변환
```

## Next task

C++ Qt Widgets 병렬 구현을 시작한다.

우선순위:

1. `cpp_calculator` Qt 프로젝트와 빌드 구조 확인
2. Python GUI와 대응되는 메인 창·디스플레이·버튼 구조 작성
3. C++ Tokenizer / Parser / Engine 구현
4. Python 테스트 식과 동일한 기준으로 기능 패리티 검증
5. STAT / EQN / CMPLX 순서로 모드 이식

## Resume instruction

새 대화에서 이 파일을 읽은 AI는 다음 작업을 `C++ Qt 프로젝트 구조 확인 및 기본 GUI 구현`으로 판단한다.
