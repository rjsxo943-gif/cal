# C++ Console Scientific Calculator

외부 GUI 라이브러리 없이 **Visual Studio와 표준 C++17만으로 빌드되는 콘솔 공학용 계산기**입니다. 완성된 `python_calculator/`를 계산 동작의 기준으로 사용합니다.

## Features

- 재귀 하강 파서: `+ - * / ^`, 괄호, 단항 부호
- 후위 연산: 팩토리얼 `!`, 백분율 `%`
- 상수와 상태: `pi`, `π`, `e`, `Ans`
- 공학 함수: 삼각·역삼각·로그·제곱근·절댓값·역수
- 정수 함수: `npr`, `ncr`, `gcd`, `lcm`, `quot`, `rem`, `mod`, `root`
- 난수: `random()`, `randint(a,b)`
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4
- S⇔D 단순 분수 표시
- 계산 기록
- 1변수 통계
- 이차방정식
- 복소수 직교형·극형 변환
- 대화형 메뉴와 `--eval` 자동 실행 모드
- 외부 테스트 프레임워크가 필요 없는 CTest 테스트

## Requirements

- Visual Studio 2026의 **C++를 사용한 데스크톱 개발** 워크로드
- CMake 3.21 이상
- C++17 컴파일러

Qt, Qt VS Tools, vcpkg 및 별도 수학 라이브러리는 필요하지 않습니다.

## Build in PowerShell

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
.\build\Debug\scientific_calculator.exe
```

Ninja 같은 단일 구성 생성기를 사용하면 실행 파일은 보통 다음 위치에 생성됩니다.

```powershell
.\build\scientific_calculator.exe
```

## Open in Visual Studio

1. Visual Studio 실행
2. **파일 → 열기 → 폴더**
3. `C:\Users\user\cal\cpp_calculator` 선택
4. CMake 구성이 끝나면 시작 항목에서 `scientific_calculator.exe` 선택
5. `Ctrl+F5` 또는 `F5`

새 콘솔 프로젝트를 별도로 만들 필요가 없습니다. 이 폴더의 `CMakeLists.txt`가 Visual Studio 프로젝트 역할을 합니다.

## Command-line mode

```powershell
.\build\Debug\scientific_calculator.exe --eval "2+3*4"
.\build\Debug\scientific_calculator.exe --eval "sin(30)" --angle DEG
.\build\Debug\scientific_calculator.exe --eval "1/3" --format FIX4
.\build\Debug\scientific_calculator.exe --help
.\build\Debug\scientific_calculator.exe --version
```

종료 코드:

- `0`: 성공
- `1`: 계산 또는 수식 오류
- `2`: 잘못된 명령줄 옵션

## Interactive commands

일반 계산 화면에서 사용할 수 있습니다.

```text
:back       메인 메뉴
:history    계산 기록
:help       지원 문법
:drg        DEG → RAD → GRAD
:fmt        NORM → FIX4 → SCI4
:sd         최근 결과의 소수/분수 전환
:clear      최근 표시만 초기화(Ans 유지)
```

## Error messages

```text
Syntax ERROR
Math ERROR
Division by zero
Overflow
Invalid input
Coefficient a must not be zero
Magnitude must not be negative
Select a data row
```

## Tests

```powershell
ctest --test-dir build -C Debug --output-on-failure
```

Linux/Ninja 환경:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
ctest --test-dir build --output-on-failure
```

Python과 대표 수식 결과를 비교하려면 Python 가상환경을 활성화한 뒤 실행합니다.

```powershell
python tools\compare_with_python.py build\Debug\scientific_calculator.exe
```

## Architecture

```text
ConsoleApplication
        ↓
CalculatorController / mode controllers
        ↓
CalculatorState
        ↓
Tokenizer → ExpressionParser → CalculatorEngine
        ↓
ResultFormatter / CalculationHistory
```

`core/`와 `modes/`는 콘솔 입출력에 의존하지 않으므로 나중에 GUI를 다시 붙여도 계산 엔진을 재사용할 수 있습니다.

## Known limitations

- C++ 1.0은 콘솔 버전이며 GUI를 포함하지 않습니다.
- 복소수 모드는 변환·크기·위상·켤레를 지원하지만 일반 복소수 수식 파서는 지원하지 않습니다.
- 삼차방정식, 연립방정식, 회귀분석, 그래프, 단위 변환, 파일 기반 기록은 Future Work입니다.
