# C++ Win32 Scientific Calculator

순수 **C++17 + Windows Win32 API**로 구현한 버튼형 공학용 계산기입니다.

Qt 같은 외부 GUI 프레임워크 없이 Windows SDK와 MSVC만 사용합니다. 수식 계산은 직접 만든 Tokenizer와 재귀 하강 Parser가 담당하며, GUI와 계산 엔진을 분리해 테스트와 기능 확장이 가능하도록 구성했습니다.

## Current Status

```text
Win32 버튼형 GUI          완료
일반·공학 계산 엔진       완료
STAT 모드                 완료
EQN 모드                  완료
CMPLX 모드                완료
Visual Studio 빌드         확인 완료
Windows GUI 실행           확인 완료
C++ 자동 테스트            최근 확인 기준 94개 통과
```

확인 환경:

```text
Visual Studio 18
Platform Toolset v145
Debug x64
Windows SDK
```

## Quick Start

CMake는 필요하지 않습니다.

```text
C:\Users\user\cal\cpp_calculator\ScientificCalculator.sln
```

1. `ScientificCalculator.sln`을 더블클릭합니다.
2. Visual Studio 상단 구성을 `Debug`로 설정합니다.
3. 플랫폼을 `x64`로 설정합니다.
4. 솔루션 탐색기에서 `ScientificCalculator` 프로젝트를 우클릭합니다.
5. **시작 프로젝트로 설정**을 선택합니다.
6. `Ctrl + F5` 또는 `F5`로 실행합니다.

일반적인 실행 파일 위치:

```text
cpp_calculator\x64\Debug\ScientificCalculator.exe
```

## Requirements

Visual Studio Installer에서 다음 항목이 필요합니다.

```text
C++를 사용한 데스크톱 개발
최신 MSVC x64/x86 빌드 도구
Windows 10 또는 Windows 11 SDK
```

필요하지 않은 항목:

```text
Qt
Qt VS Tools
vcpkg
CMake — Visual Studio 솔루션 실행 기준
```

## Visual Studio Solution

```text
ScientificCalculator.sln
├─ ScientificCalculator   Win32 버튼형 GUI
└─ CalculatorTests        계산 엔진 자동 테스트
```

`ScientificCalculator`은 Windows 하위 시스템 프로그램이므로 실행 시 별도 콘솔 창이 나타나지 않습니다.

## GUI Modes

### CALC

일반 계산과 공학 함수를 처리합니다.

- 숫자와 사칙연산 버튼
- 괄호와 수식 중간 편집
- 삼각함수와 역삼각함수
- 로그, 자연로그, 제곱근
- 거듭제곱, n제곱근
- 팩토리얼, 백분율
- 순열과 조합
- GCD, LCM, 몫, 나머지
- `pi`, `e`, `Ans`
- 난수 함수
- `SHIFT`
- `DEG / RAD / GRAD`
- `NORM / FIX4 / SCI4`
- `S⇔D`
- 계산 기록

### STAT

공백, 쉼표 또는 세미콜론으로 여러 숫자를 입력할 수 있습니다.

지원 결과:

- 데이터 개수
- 합계
- 평균
- 최솟값과 최댓값
- 모집단 분산과 표준편차
- 표본 분산과 표준편차

### EQN

다음 이차방정식을 풉니다.

```text
ax² + bx + c = 0
```

지원 결과:

- 서로 다른 두 실근
- 중근
- 두 복소근

### CMPLX

복소수를 직교형 또는 극형으로 입력합니다.

지원 결과:

- 직교형 복소수
- 켤레복소수
- 크기
- 위상각
- 직교형 ↔ 극형 변환

위상각은 현재 `DEG / RAD / GRAD` 설정을 사용합니다.

## CALC Controls

```text
Enter       계산 실행
Escape      입력과 최근 결과 초기화
Backspace   커서 앞 문자 삭제
← / →       수식 커서 이동
SHIFT       보조 함수 전환
DRG         DEG → RAD → GRAD
FMT         NORM → FIX4 → SCI4
S⇔D         최근 결과의 소수·분수 전환
AC          입력 전체 삭제
DEL         한 글자 삭제
```

계산 기록 항목을 더블클릭하면 해당 수식을 입력창으로 다시 가져옵니다.

## Expression Syntax

### Operators

```text
+  -  *  /  ^
( )  !  %
```

### Constants and State

```text
pi
e
Ans
```

### Functions

```text
sin cos tan
asin acos atan
log ln sqrt abs recip
npr ncr
gcd lcm
quot rem mod
root
random randint
```

### Examples

```text
2+3*4
(2+3)*4
-5+3
2^3^2
sin(30)
log(100)+2^3
root(3,-8)
5!
npr(10,3)
ncr(10,3)
gcd(84,30)
lcm(12,18)
randint(1,6)
Ans*2
```

`^`는 오른쪽 결합으로 처리합니다.

```text
2^3^2 = 2^(3^2) = 512
```

## Internal Architecture

```text
Win32 GUI
    ↓
CalculatorController / Mode Controllers
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

### GUI Layer

- Win32 창과 컨트롤 생성
- 버튼 및 키보드 이벤트 처리
- 입력 문자열 편집
- 계산 결과와 상태 표시
- 모드 전환

### Core Layer

- 수식 토큰화
- 연산자 우선순위 처리
- 함수와 상수 계산
- 각도 모드 변환
- 결과 포맷
- 오류 변환
- 계산 기록 관리

GUI 소스는 계산식을 직접 해석하지 않습니다. 같은 Core 계층을 테스트 프로그램과 선택적 CLI에서도 재사용합니다.

## Source Layout

```text
cpp_calculator/
├─ ScientificCalculator.sln
├─ ScientificCalculator.vcxproj
├─ CalculatorTests.vcxproj
├─ include/
│  └─ ScientificCalculator.h
├─ src/
│  ├─ ScientificCalculator.cpp
│  └─ 계산 엔진 분할 구현 파일
├─ win32/
│  ├─ ScientificCalculatorWin32.cpp
│  └─ parts/
├─ tests/
│  ├─ CalculatorTests.cpp
│  └─ split/
├─ main.cpp                  선택적 CLI 진입점
├─ CMakeLists.txt            선택적 CMake 빌드
└─ README.md
```

큰 단일 구현 파일은 GitHub 커넥터 작업과 관리 편의를 위해 여러 `.inc` 파일로 분할되어 있습니다. 최종적으로는 하나의 번역 단위에서 함께 컴파일됩니다.

## Error Messages

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

오류가 발생해도 계산기 프로그램은 종료되지 않으며, 오류 문구를 표시한 뒤 다음 입력을 받을 수 있습니다.

## Running Tests in Visual Studio

1. 솔루션 탐색기에서 `CalculatorTests`를 우클릭합니다.
2. **시작 프로젝트로 설정**을 선택합니다.
3. `Ctrl + F5`로 실행합니다.
4. 테스트 요약에서 실패 개수를 확인합니다.

테스트가 끝나면 다시 `ScientificCalculator`을 시작 프로젝트로 설정하면 됩니다.

## Optional CMake Build

CMake가 설치된 환경에서만 사용합니다.

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

Windows CMake 대상:

```text
scientific_calculator       Win32 버튼형 GUI
scientific_calculator_cli   선택적 CLI 프로그램
calculator_tests            자동 테스트
```

저장소에 남아 있는 Qt 이름의 CMake preset은 Visual Studio가 생성한 이전 설정 파일이며, 현재 Win32 계산기 빌드에는 사용하지 않습니다. Windows에서는 `ScientificCalculator.sln`을 여는 방법을 권장합니다.

## Troubleshooting

### `v100` 빌드 도구를 찾을 수 없음

프로젝트가 Visual Studio 2010 도구 집합을 가리킬 때 발생합니다. 현재 프로젝트 파일은 `v145`로 저장되어 있지만, 로컬 캐시나 이전 설정 때문에 다시 나타날 수 있습니다.

```text
솔루션 우클릭
→ 솔루션 대상 변경
→ ScientificCalculator과 CalculatorTests 선택
→ 최신 MSVC 도구 집합으로 변경
```

또는 프로젝트 속성에서:

```text
구성 속성
→ 일반
→ 플랫폼 도구 집합
→ v145 또는 현재 설치된 최신 도구 집합
```

Visual Studio 2010이나 `v100`을 별도로 설치할 필요는 없습니다.

### 실행 파일 경로를 찾을 수 없음

먼저 프로그램을 빌드해야 합니다.

```text
빌드
→ 솔루션 다시 빌드
```

성공 후 다음 파일이 생성되는지 확인합니다.

```text
x64\Debug\ScientificCalculator.exe
```

### 시작 프로젝트 오류

솔루션 탐색기에서 `ScientificCalculator`을 우클릭하고 **시작 프로젝트로 설정**을 선택합니다.

## Validation Notes

- 계산 엔진 자동 테스트: 최근 확인 기준 94개 통과
- Visual Studio 솔루션 빌드: 사용자 Windows 환경에서 확인
- Win32 버튼형 GUI 실행: 사용자 Windows 환경에서 확인
- GitHub Actions: 아직 미구성

## Current Limitations

- 일반 수식 Parser는 실수 계산을 기준으로 합니다.
- 복소수의 일반 수식 연산은 아직 별도 복소수 모드로 제한됩니다.
- `30°`, `pi/2 r`, `50 g`처럼 숫자 뒤에 각도 단위를 직접 붙이는 문법은 완전 지원되지 않습니다.
- 계산 기록은 프로그램을 종료하면 사라집니다.
- 실제 수학책 형태의 세로 분수·루트·지수 렌더링은 지원하지 않습니다.
- 그래프, 단위 변환, 고급 통계는 포함하지 않습니다.

## Future Work

- 일반 복소수 수식 Parser
- 개별 각도 단위 문법
- 계산 기록 파일 저장과 복원
- 실제 수학식 렌더링
- 메모리 키와 사용자 변수
- 삼차방정식과 연립방정식
- 고급 통계와 회귀분석
- 그래프와 단위 변환
- GitHub Actions Windows 자동 빌드
