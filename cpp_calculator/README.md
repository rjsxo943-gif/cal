# C++ Win32 Scientific Calculator

외부 GUI 프레임워크 없이 **순수 C++17 + Windows Win32 API**로 만든 버튼형 공학용 계산기입니다. 계산 엔진은 사용자 정의 Tokenizer와 재귀 하강 Parser를 사용하며, 완성된 `python_calculator/`의 계산 동작을 기준으로 구현했습니다.

## 가장 쉬운 실행 방법

CMake는 필요하지 않습니다.

1. `C:\Users\user\cal\cpp_calculator\ScientificCalculator.sln`을 더블클릭합니다.
2. Visual Studio 상단 구성을 `Debug`, 플랫폼을 `x64`로 둡니다.
3. 솔루션 탐색기에서 `ScientificCalculator`을 우클릭합니다.
4. **시작 프로젝트로 설정**을 누릅니다.
5. `Ctrl + F5` 또는 `F5`로 실행합니다.

Visual Studio Installer에는 다음 워크로드가 필요합니다.

```text
C++를 사용한 데스크톱 개발
Windows 10 또는 Windows 11 SDK
최신 MSVC x64/x86 빌드 도구
```

Qt, Qt VS Tools, CMake, vcpkg는 버튼형 프로그램을 실행하는 데 필요하지 않습니다.

## GUI 구성

```text
CALC   일반·공학 계산
STAT   1변수 통계
EQN    이차방정식
CMPLX  복소수 직교형·극형 변환
```

CALC 화면:

- 숫자·연산자·괄호 버튼
- 삼각함수, 로그, 제곱근
- 순열·조합, GCD·LCM, 몫·나머지
- 팩토리얼과 퍼센트
- `pi`, `e`, `Ans`, 난수
- SHIFT 라벨·입력 전환
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4
- S⇔D 분수·소수 전환
- 왼쪽·오른쪽 커서, DEL, AC
- 계산 기록과 더블클릭 복원
- 수식창에서 Enter 계산, Esc 초기화

STAT 화면:

- 공백·쉼표·세미콜론으로 여러 값 입력
- 값 추가·선택 삭제·전체 삭제
- 개수, 합계, 평균, 최솟값, 최댓값
- 모집단·표본 분산과 표준편차

EQN 화면:

- `a`, `b`, `c` 입력
- `ax² + bx + c = 0` 계산
- 서로 다른 실근, 중근, 복소근 표시

CMPLX 화면:

- 직교형 또는 극형 입력
- 복소수, 켤레복소수, 크기, 위상 표시
- 현재 DEG / RAD / GRAD 상태 사용

## Visual Studio 프로젝트

```text
ScientificCalculator.sln
├─ ScientificCalculator   버튼형 Win32 GUI
└─ CalculatorTests        계산 엔진 테스트
```

일반적으로 Debug 실행 파일은 다음 경로에 생성됩니다.

```text
cpp_calculator\x64\Debug\ScientificCalculator.exe
```

## 계산 문법

```text
+  -  *  /  ^
( )  !  %
pi  e  Ans
sin cos tan asin acos atan
log ln sqrt abs recip
npr ncr gcd lcm quot rem mod root
random() randint(a,b)
```

예시:

```text
2+3*4
sin(30)
root(3,-8)
ncr(10,3)
gcd(84,30)
Ans*2
```

## 선택 사항: CMake

CMake가 설치된 환경에서는 다음 방식도 사용할 수 있습니다.

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

Windows CMake 빌드 대상:

```text
scientific_calculator       Win32 버튼형 GUI
scientific_calculator_cli   기존 CLI 버전
calculator_tests            자동 테스트
```

## Architecture

```text
Win32 GUI / optional CLI
          ↓
CalculatorController / mode controllers
          ↓
CalculatorState
          ↓
Tokenizer → ExpressionParser → CalculatorEngine
          ↓
ResultFormatter / CalculationHistory
```

GUI는 계산식을 직접 해석하지 않습니다. 계산·상태·표시 형식은 기존 독립 엔진에서 처리하므로 CLI와 GUI가 같은 계산 결과를 사용합니다.

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

## Validation status

계산 엔진의 기존 자동 테스트 94개는 통과한 상태입니다. Win32 GUI는 Windows SDK와 MSVC가 없는 개발 환경에서 작성되어, 실제 Windows 빌드·실행 확인은 사용자의 Visual Studio에서 최종 확인해야 합니다. 빌드 오류가 나오면 오류 메시지를 기준으로 바로 수정합니다.
