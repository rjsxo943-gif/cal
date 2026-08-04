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
C++ Qt GUI 뼈대            완료
C++ 기본 계산 엔진         다음 작업
```

## Latest completed feature

### C++ Qt Widgets GUI skeleton

`cpp_calculator`에 Visual Studio에서 열 수 있는 CMake 기반 Qt Widgets 프로젝트를 추가했다.

지원 구조:

```text
MainWindow
├─ CalculatorWidget
│  ├─ DisplayPanel
│  ├─ ControlPanel
│  └─ Calculate / Statistics / Equation / Complex mode stack
├─ HistoryPanel
└─ CalculatorState
```

현재 동작:

- `QMainWindow`와 좌우 `QSplitter`
- 수식 입력창과 결과 표시창
- Python 버전과 대응되는 계산 버튼 그리드
- 마우스 버튼 입력과 현재 커서 위치 삽입
- 왼쪽/오른쪽 커서 이동
- DEL / AC
- SHIFT 상태 표시와 버튼 라벨 변경
- MODE 메뉴와 네 개 모드 페이지
- 기록 패널 열기/닫기와 수식 복원 구조
- DEG → RAD → GRAD 상태 순환
- NORM → FIX4 → SCI4 상태 순환
- Qt 5 / Qt 6 자동 탐지 CMake 구성
- MSVC UTF-8 컴파일 옵션

아직 C++ 계산 엔진은 연결하지 않았으므로 `=` 실행 시 `ENGINE NOT CONNECTED`를 표시한다.

C++ 상태 클래스 테스트:

```text
CalculatorStateTests
- DEG / RAD / GRAD 순환
- NORM / FIX4 / SCI4 순환
- SHIFT 상태
```

관련 구조:

```text
CalculatorWidget signal
↓
MainWindow
↓
CalculatorState
```

## Python implementation status

Python 버전의 핵심 모드는 모두 실제 화면과 연결되었다.

```text
CALC  기본·공학 계산
STAT  1변수 통계
EQN   이차방정식
CMPLX 복소수 직교형·극형 변환
```

## Next task

C++ 기본 계산 엔진을 구현하고 GUI의 `=`에 연결한다.

우선순위:

1. C++ CalculatorError 오류 계층
2. C++ Tokenizer
3. C++ 재귀 하강 ExpressionParser
4. CalculatorEngine / ResultFormatter / CalculatorController
5. 사칙연산·괄호·단항 부호·거듭제곱 테스트
6. Python과 동일한 테스트 식으로 결과 비교
7. `ENGINE NOT CONNECTED` 제거 및 HistoryPanel 연결

## Resume instruction

새 대화에서 이 파일을 읽은 AI는 다음 작업을 `C++ 기본 계산 엔진 구현 및 GUI 연결`로 판단한다.
