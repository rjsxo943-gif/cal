# Scientific Calculator Dual Implementation

동일한 공학용 계산기를 Python과 C++로 구현한 프로젝트입니다.

## Implementations

### Python

- Python + PySide6 GUI
- `python_calculator/`
- CALC / STAT / EQN / CMPLX 모드
- 버튼, SHIFT, 계산 기록, 표시 형식 포함

### C++

- 표준 C++17 콘솔 프로그램
- Visual Studio 2026 또는 일반 CMake 환경
- `cpp_calculator/`
- Qt 및 외부 라이브러리 불필요
- Python 버전을 계산 동작의 기준으로 사용

## C++ quick start

```powershell
cd cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
.\build\Debug\scientific_calculator.exe
```

Ninja 같은 단일 구성 생성기를 사용하면 실행 파일은 보통 `build/scientific_calculator.exe`에 생성됩니다.

단일 수식 실행:

```powershell
.\build\Debug\scientific_calculator.exe --eval "2+3*4"
.\build\Debug\scientific_calculator.exe --eval "sin(30)" --angle DEG
```

## C++ features

- 사칙연산, 괄호, 단항 부호, 거듭제곱
- 팩토리얼, 퍼센트
- 삼각·역삼각·로그·제곱근 함수
- 순열·조합, GCD·LCM, 몫·나머지, n제곱근
- `pi`, `e`, `Ans`, 난수
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4 / S⇔D
- 계산 기록
- 1변수 통계
- 이차방정식
- 복소수 직교형·극형 변환
- 재귀 하강 Parser와 공통 오류 처리

## Documentation

- `docs/CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md`
- `docs/CURRENT_STATUS.md`
