# Scientific Calculator Dual Implementation

동일한 공학용 계산기를 Python과 C++로 구현한 프로젝트입니다.

## Implementations

### Python

- Python + PySide6 버튼형 GUI
- `python_calculator/`
- CALC / STAT / EQN / CMPLX 모드
- SHIFT, 계산 기록, 표시 형식 포함

### C++

- C++17 + Windows Win32 API 버튼형 GUI
- `cpp_calculator/`
- Qt 및 외부 GUI 라이브러리 불필요
- Visual Studio 솔루션을 직접 열어 빌드 가능
- 기존 CLI 버전도 선택적으로 유지
- Python 버전을 계산 동작의 기준으로 사용

## C++ quick start — CMake 불필요

```text
cpp_calculator\ScientificCalculator.sln
```

위 파일을 Visual Studio에서 열고:

```text
구성: Debug
플랫폼: x64
시작 프로젝트: ScientificCalculator
실행: Ctrl+F5 또는 F5
```

솔루션 구성:

```text
ScientificCalculator   Win32 버튼형 GUI
CalculatorTests        계산 엔진 테스트
```

## C++ GUI modes

```text
CALC   일반·공학 계산
STAT   1변수 통계
EQN    이차방정식
CMPLX  복소수 직교형·극형 변환
```

## C++ features

- 사칙연산, 괄호, 단항 부호, 거듭제곱
- 팩토리얼, 퍼센트
- 삼각·역삼각·로그·제곱근 함수
- 순열·조합, GCD·LCM, 몫·나머지, n제곱근
- `pi`, `e`, `Ans`, 난수
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4 / S⇔D
- SHIFT 버튼 라벨·입력 전환
- 커서 이동, DEL, AC
- 계산 기록과 더블클릭 복원
- 1변수 통계
- 이차방정식
- 복소수 직교형·극형 변환
- 재귀 하강 Parser와 공통 오류 처리

## Optional CMake build

CMake가 설치된 환경에서는 다음 방식도 사용할 수 있습니다.

```powershell
cd cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

Windows CMake 대상:

```text
scientific_calculator       버튼형 GUI
scientific_calculator_cli   CLI 버전
calculator_tests            자동 테스트
```

## Documentation

- `cpp_calculator/README.md`
- `docs/CURRENT_STATUS.md`
- `docs/CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md` — 계산 엔진 구현 당시 기준 문서
