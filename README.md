# Scientific Calculator

Python과 C++로 동일한 계산 동작을 구현한 **버튼형 공학용 계산기 프로젝트**입니다.

Python 버전은 `PySide6`, C++ 버전은 별도 GUI 프레임워크 없이 `Win32 API`를 사용합니다. 두 프로그램은 화면 구현 방식은 다르지만, 같은 수식 문법·계산 결과·표시 모드·오류 메시지를 제공하도록 설계했습니다.

## Project Status

| 구현 | 기술 | 상태 |
|---|---|---|
| Python | Python 3, PySide6 | GUI 및 핵심 기능 완료 |
| C++ | C++17, Win32 API, Visual Studio | GUI 및 핵심 기능 완료 |
| Python tests | pytest | 최근 확인 기준 174개 통과 |
| C++ tests | 자체 테스트 러너, CTest/Visual Studio | 최근 확인 기준 94개 통과 |

C++ 버튼형 계산기는 Visual Studio 18, 플랫폼 도구 집합 `v145`, `Debug x64` 환경에서 실제 빌드와 실행을 확인했습니다.

## Main Features

### CALC — 일반·공학 계산

- 사칙연산과 괄호
- 연산자 우선순위와 중첩 수식
- 단항 `+`, `-`
- 거듭제곱, 제곱근, n제곱근
- 팩토리얼과 백분율
- 삼각함수와 역삼각함수
- 상용로그와 자연로그
- 순열 `nPr`, 조합 `nCr`
- `GCD`, `LCM`, 몫, 나머지
- 상수 `pi`, `e`
- 이전 결과 `Ans`
- 난수 `random()`, `randint(a,b)`

### Calculator State

- `DEG / RAD / GRAD`
- `NORM / FIX4 / SCI4`
- `S⇔D` 소수·분수 전환
- `SHIFT` 보조 기능
- 실행 중 계산 기록
- 기록 더블클릭 복원

### Additional Modes

- `STAT`: 1변수 통계
- `EQN`: 이차방정식
- `CMPLX`: 복소수 직교형·극형 변환

## Quick Start

### C++ 버튼형 계산기

CMake나 Qt 설치 없이 Visual Studio 솔루션을 바로 열 수 있습니다.

```text
cpp_calculator\ScientificCalculator.sln
```

1. 솔루션을 Visual Studio에서 엽니다.
2. 구성을 `Debug`, 플랫폼을 `x64`로 설정합니다.
3. `ScientificCalculator` 프로젝트를 시작 프로젝트로 설정합니다.
4. `Ctrl + F5` 또는 `F5`로 실행합니다.

필요한 Visual Studio 구성 요소:

```text
C++를 사용한 데스크톱 개발
최신 MSVC x64/x86 빌드 도구
Windows 10 또는 Windows 11 SDK
```

일반적인 Debug 실행 파일 경로:

```text
cpp_calculator\x64\Debug\ScientificCalculator.exe
```

### Python 버튼형 계산기

```powershell
cd python_calculator
python main.py
```

Python 환경에는 `PySide6`가 필요합니다.

## Expression Examples

```text
2+3*4
(2+3)*4
sin(30)
sqrt(16)+2^3
root(3,-8)
ncr(10,3)
gcd(84,30)
Ans*2
```

지원 함수:

```text
sin cos tan asin acos atan
log ln sqrt abs recip
npr ncr gcd lcm quot rem mod root
random randint
```

## Architecture

```text
Python GUI / Win32 GUI
          ↓
CalculatorController
          ↓
CalculatorState
          ↓
Tokenizer
          ↓
ExpressionParser
          ↓
CalculatorEngine
          ↓
ResultFormatter / CalculationHistory
```

GUI는 수식을 직접 계산하지 않습니다. 입력과 화면 갱신만 담당하며, 실제 계산은 독립된 엔진 계층에서 처리합니다. 이 구조 덕분에 Python과 C++의 동작을 같은 테스트 입력으로 비교할 수 있고, GUI를 변경해도 계산 엔진을 재사용할 수 있습니다.

## Parser Design

수식을 왼쪽부터 단순 계산하지 않고, 직접 만든 Tokenizer와 재귀 하강 Parser가 전체 수식을 해석합니다.

```text
expression → addition / subtraction
term       → multiplication / division
unary      → unary + / unary -
power      → right-associative exponentiation
postfix    → factorial / percent
primary    → number / constant / function / parentheses
```

따라서 다음 결과를 올바르게 구분합니다.

```text
2+3*4     → 14
(2+3)*4   → 20
2^3^2     → 512
```

## Error Handling

두 구현에서 가능한 한 같은 오류 문구를 사용합니다.

```text
Syntax ERROR
Math ERROR
Division by zero
Overflow
Invalid input
Coefficient a must not be zero
Magnitude must not be negative
```

오류가 발생해도 프로그램이 종료되지 않고 다음 입력을 계속 받을 수 있도록 구성했습니다.

## Project Structure

```text
cal/
├─ python_calculator/        Python + PySide6 GUI
├─ cpp_calculator/           C++17 + Win32 API GUI
│  ├─ include/               공통 인터페이스
│  ├─ src/                   계산 엔진 구현
│  ├─ win32/                 버튼형 Windows GUI
│  ├─ tests/                 C++ 자동 테스트
│  └─ ScientificCalculator.sln
├─ docs/                     설계·진행 문서
└─ README.md
```

## Validation

### C++

Visual Studio에서 `CalculatorTests` 프로젝트를 빌드·실행하거나, CMake가 설치된 환경에서는 다음 명령을 사용할 수 있습니다.

```powershell
cd cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

Windows에서 프로그램 실행은 Visual Studio 솔루션 방식이 기본이며, CMake는 선택 사항입니다.

### Python

```powershell
cd python_calculator
pytest
```

GitHub Actions는 아직 구성하지 않았으므로 테스트 개수는 로컬에서 마지막으로 확인한 결과입니다.

## Key Engineering Points

- `eval`을 사용하지 않고 수식 파서를 직접 구현
- GUI와 계산 로직의 의존성 분리
- Python과 C++ 간 동일 입력·결과 비교
- 각도 및 표시 모드를 공통 상태 객체로 관리
- 부동소수점 결과를 공통 규칙으로 포맷
- 실근·중근·복소근을 구분하는 이차방정식 처리
- 복소수의 직교형·극형·크기·위상·켤레 계산
- 잘못된 입력과 수학적 정의역 오류를 구분

## Current Limitations

- 일반 수식 Parser는 실수 계산을 기준으로 하며, 복소수 일반 수식은 별도 모드에서 처리합니다.
- 개별 숫자 뒤에 붙이는 `°`, `r`, `g` 각도 표기는 아직 완전 지원 대상이 아닙니다.
- 세로 분수, 루트, 지수 형태의 수학식 렌더링은 지원하지 않습니다.
- 계산 기록은 프로그램 실행 중에만 유지됩니다.
- 그래프와 단위 변환은 포함하지 않습니다.

## Future Work

- 일반 복소수 수식 Parser
- 계산 기록 저장과 복원
- 세로 분수·루트·지수 렌더링
- 메모리 키 `M+ / M- / MR / MC`
- 변수 저장 `A / B / C / X / Y`
- 연립방정식과 삼차방정식
- 고급 통계와 회귀분석
- 단위 변환과 그래프 기능
- GitHub Actions 기반 Windows/Python 자동 테스트

## Documentation

- [`cpp_calculator/README.md`](cpp_calculator/README.md): C++ 실행 및 사용 설명
- [`docs/CURRENT_STATUS.md`](docs/CURRENT_STATUS.md): 현재 진행 상태
- [`docs/CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md`](docs/CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md): C++ 계산 엔진 구현 계획 기록
