# C++ 콘솔 공학용 계산기 완성 계획서

> 저장소: `rjsxo943-gif/cal`  
> 대상 폴더: `cpp_calculator/`  
> 개발 환경: Visual Studio 2026, MSVC, Windows 콘솔  
> 언어 표준: C++17  
> 외부 라이브러리: 사용하지 않음  
> 기능 기준: 완성된 `python_calculator/`

---

## 1. 문서 목적

이 문서는 C++ 공학용 계산기를 처음부터 최종 완성까지 구현하기 위한 기준 문서다.

앞으로 구현 중 대화가 길어지거나 새 대화로 넘어가더라도 이 문서를 읽으면 다음 내용을 바로 복원할 수 있어야 한다.

- 최종 목표
- 구현 범위
- 제외 범위
- 내부 구조
- 수식 문법
- 콘솔 사용 흐름
- 테스트 기준
- 커밋 순서
- 완료 판정 조건

사용자가 이후에 새로운 변경을 요청하지 않는 한 이 문서를 C++ 구현의 기준으로 사용한다.

---

## 2. 최신 확정 방향

기존 프로젝트 기준 문서에서는 C++ 버전에 Qt Widgets GUI를 사용하기로 했지만, 최신 사용자 결정에 따라 C++ 버전은 **Visual Studio 콘솔 프로그램**으로 변경한다.

```text
Python 버전 → PySide6 GUI 계산기, 핵심 기능 완료
C++ 버전    → Visual Studio 콘솔 계산기, 앞으로 완성
```

따라서 C++ 구현은 다음 원칙을 따른다.

- Qt를 설치하지 않는다.
- Qt에 링크하지 않는다.
- Visual Studio의 C++ 데스크톱 개발 도구만 사용한다.
- 현재 저장소에 있는 Qt GUI 시제품은 활성 빌드에서 제거한다.
- 재사용할 수 있는 상태 로직은 옮긴 뒤 Qt GUI 파일은 삭제한다.
- 삭제된 Qt 코드는 Git 기록으로 보존되므로 별도 보관 폴더를 만들지 않는다.
- 콘솔 입력·출력과 계산 엔진은 반드시 분리한다.
- 나중에 GUI를 다시 붙이더라도 계산 엔진을 재작성하지 않아야 한다.

---

## 3. C++ 1.0 완료 목표

C++ 버전은 현재 Python 버전에서 동작하는 계산 기능과 상태 규칙을 콘솔 환경에서 최대한 동일하게 제공한다.

기본 메뉴는 다음과 같이 구성한다.

```text
1. 일반 계산
2. 1변수 통계
3. 이차방정식
4. 복소수
5. 설정
6. 계산 기록
0. 종료
```

공통 상태:

- `Ans`
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4
- S⇔D 소수·분수 전환
- 프로그램 실행 중 계산 기록
- 동일한 오류 문구
- 잘못된 입력 후에도 프로그램 계속 실행

---

## 4. 구현 범위

## 4.1 일반 수식 입력

다음과 같은 한 줄 수식을 입력한다.

```text
2+3*4
(2+3)*4
-5+3
2^10
sqrt(16)
sin(30)+4
```

지원 요소:

- 덧셈 `+`
- 뺄셈 `-`
- 곱셈 `*`
- 나눗셈 `/`
- 거듭제곱 `^`
- 팩토리얼 `!`
- 백분율 `%`
- 괄호
- 중첩 괄호
- 단항 `+`, `-`
- 정수와 소수
- 과학적 숫자 표기 `1E3`, `2.5e-4`
- 함수 호출
- 함수 인자 구분용 쉼표

가능한 경우 다음 유니코드 별칭도 지원한다.

```text
× → *
÷ → /
√ → sqrt
π → pi
```

---

## 4.2 연산 우선순위

연산은 입력 순서대로 단순 계산하지 않고 전체 수식을 파싱한다.

우선순위:

```text
1. 숫자, 상수, 함수, 괄호
2. 후위 연산자 !, %
3. 거듭제곱 ^
4. 단항 +, -
5. 곱셈, 나눗셈
6. 덧셈, 뺄셈
```

거듭제곱은 오른쪽 결합으로 처리한다.

```text
2^3^2   = 512
-2^2    = -4
(-2)^2  = 4
```

---

## 4.3 상수와 Ans

지원 상수:

```text
pi
π
e
Ans
```

`Ans` 규칙:

- 초기값은 `0`이다.
- 일반 계산 모드에서 성공한 계산만 `Ans`를 갱신한다.
- 오류가 발생하면 기존 `Ans`를 유지한다.
- FMT 또는 S⇔D로 표시만 바꿀 때 `Ans`는 변하지 않는다.
- 통계·방정식·복소수 모드 결과는 우선 `Ans`에 저장하지 않는다.

---

## 4.4 공학 함수

### 인자 1개

```text
sqrt(x)
sin(x)
cos(x)
tan(x)
asin(x)
acos(x)
atan(x)
log(x)
ln(x)
abs(x)
recip(x)
```

### 인자 2개

```text
npr(n,r)
ncr(n,r)
mod(a,b)
gcd(a,b)
lcm(a,b)
quot(a,b)
rem(a,b)
root(n,x)
randint(a,b)
```

### 인자 없음

```text
random()
```

세부 규칙:

- 팩토리얼은 0 이상의 정수만 허용한다.
- `170!`까지 허용하고 `171!`은 `Overflow`다.
- 순열·조합은 0 이상의 정수이며 `r <= n`이어야 한다.
- `quot`는 0 방향으로 절삭한다.
- `quot(-10,3) = -3`이다.
- `rem`, `mod`는 Python 구현과 맞추기 위해 `fmod` 방식으로 처리한다.
- `rem(-10,3) = -1`이다.
- `root(3,-8) = -2`이다.
- 음수의 짝수 제곱근은 일반 계산 모드에서 `Math ERROR`다.
- `random()`은 `[0,1)` 범위다.
- `randint(a,b)`는 양 끝값을 포함한다.
- `randint`에서 `a > b`이면 `Math ERROR`다.

---

## 4.5 각도 모드

전역 각도 모드:

```text
DEG → RAD → GRAD → DEG
```

영향을 받는 기능:

- `sin`, `cos`, `tan` 입력
- `asin`, `acos`, `atan` 결과
- 복소수 극형식의 위상각 입력과 출력

현재 Python 파서는 `30°`, `pi/2 r`, `50 g` 같은 개별 각도 접미사를 아직 처리하지 않는다.

따라서 C++ 1.0에서는 Python과 동일하게 전역 각도 모드만 지원한다. 개별 접미사는 Python과 C++에 동시에 추가할 Future Work로 남긴다.

---

## 4.6 결과 표시 모드

### NORM

- 최대 10자리 유효숫자
- 불필요한 뒤쪽 0 제거
- `-0`을 `0`으로 정규화

### FIX4

- 소수점 아래 정확히 4자리

### SCI4

- 과학적 표기법
- 소수점 아래 4자리
- 대문자 `E`

예시:

```text
NORM : 1/3 → 0.3333333333
FIX4 : 1/3 → 0.3333
SCI4 : 1/3 → 3.3333E-01
```

---

## 4.7 S⇔D 소수·분수 전환

최근 성공한 실수 결과를 소수와 단순 분수 사이에서 전환한다.

기준:

- 최대 분모 `10000`
- 허용 오차 `1e-12`
- 연분수 알고리즘 사용
- 모든 분모를 순회하는 무차별 탐색은 사용하지 않음
- `1/3`은 `0.3333333333 ⇔ 1/3`
- `pi`, `sqrt(2)` 같은 무리수는 억지로 분수로 바꾸지 않음
- 전환은 표시만 바꾸며 재계산하거나 `Ans`를 수정하지 않음

---

## 4.8 오류 문구

다음 오류 문구를 정확히 사용한다.

```text
Syntax ERROR
Math ERROR
Division by zero
Overflow
Invalid input
```

모드 전용 오류:

```text
Coefficient a must not be zero
Magnitude must not be negative
Select a data row
```

규칙:

- C++ 내부 예외 메시지를 그대로 화면에 노출하지 않는다.
- 입력 오류가 발생해도 메인 루프는 계속 동작한다.
- `nan`, `inf`, 무한 결과를 허용하지 않는다.
- Python과 같은 상황에서는 같은 오류 문구를 출력한다.

---

## 4.9 1변수 통계 모드

데이터 입력 예시:

```text
1
1, 2, 3, 4
1 2 3 4
1;2;3;4
```

기능:

- 데이터 한 개 또는 여러 개 추가
- 저장된 데이터 목록 표시
- 행 번호로 선택 삭제
- 전체 삭제
- 데이터 변경 시 통계값 즉시 재계산

통계 항목:

```text
n      데이터 개수
Σx     합계
x̄      평균
min    최솟값
max    최댓값
σ²     모집단 분산
σ      모집단 표준편차
s²     표본 분산
s      표본 표준편차
```

규칙:

- 데이터가 없으면 계산 불가 항목은 `—`로 표시한다.
- 데이터가 하나면 모집단 분산·표준편차는 `0`이다.
- 데이터가 하나면 표본 분산·표준편차는 `—`다.
- 잘못된 값이 하나라도 있으면 전체 입력을 거부하고 기존 데이터를 유지한다.
- Welford 알고리즘처럼 수치적으로 안정적인 방법을 사용한다.
- 통계값도 NORM/FIX4/SCI4를 따른다.

---

## 4.10 이차방정식 모드

식:

```text
ax² + bx + c = 0
```

입력:

```text
a
b
c
```

결과 종류:

- 서로 다른 두 실근
- 중근
- 서로 다른 두 복소근
- 판별식

규칙:

- `a = 0`은 허용하지 않는다.
- 부동소수점 오차를 고려해 거의 0인 판별식은 중근으로 처리한다.
- 서로 다른 실근은 상쇄 오차를 줄이는 안정적인 공식을 사용한다.
- 복소근은 Equation 모드에서 `i`로 표시한다.
- FMT 변경 시 최근 해를 재계산하지 않고 다시 포맷한다.

---

## 4.11 복소수 모드

전자공학 표기이므로 허수 단위는 `j`를 사용한다.

### 직교형 입력

```text
a + bj
```

콘솔에서는 실수부 `a`와 허수부 `b`를 따로 입력받는다.

### 극형 입력

```text
r ∠ θ
```

콘솔에서는 크기 `r`과 위상각 `θ`를 따로 입력받는다.

출력:

- 직교형
- 극형
- 크기
- 위상각
- 켤레복소수
- 직교형 → 극형
- 극형 → 직교형

규칙:

- 음수 크기는 허용하지 않는다.
- 허수부가 `1`이면 `1j`가 아니라 `j`로 표시한다.
- 허수부가 `-1`이면 `-j`로 표시한다.
- 매우 작은 계산 잔차는 `0`으로 정규화한다.
- 위상각은 DEG/RAD/GRAD를 따른다.
- 출력 숫자는 NORM/FIX4/SCI4를 따른다.

현재 Python Complex 모드는 복소수 사칙연산 수식까지는 지원하지 않는다. 따라서 C++ 1.0도 변환·크기·위상·켤레까지를 동등성 목표로 한다. 복소수 일반 수식 파서는 Future Work다.

---

## 4.12 계산 기록

프로그램 실행 중 성공한 일반 계산을 저장한다.

```text
2+3 = 5
sin(30) = 0.5
5! = 120
```

기능:

- 번호가 붙은 기록 목록 출력
- 번호를 선택해 이전 수식 다시 사용
- 기록 전체 삭제
- 메인 메뉴로 돌아가기

프로그램을 종료한 뒤 기록을 복원하는 기능은 Future Work다.

---

## 5. C++ 1.0 제외 범위

다음 기능은 이번 완성 작업에서 제외한다.

- Qt 또는 다른 GUI 프레임워크
- 그래프 기능
- 파일 기반 계산 기록
- M+, M-, MR, MC
- A, B, C, D, X, Y 변수
- 삼차방정식
- 연립방정식
- 회귀분석과 고급 통계
- 단위 변환
- 소인수분해
- 세로 분수·수학책 형태 렌더링
- 일반 복소수 수식 파서
- Python에 없는 개별 각도 접미사

제외 범위는 C++ 1.0 완성을 방해하지 않으며 후속 기능으로 관리한다.

---

## 6. 내부 아키텍처

콘솔 화면 코드에 계산 규칙을 넣지 않는다.

```text
ConsoleApplication
        ↓
CalculatorController / Mode Controller
        ↓
CalculatorState
        ↓
Tokenizer
        ↓
ExpressionParser
        ↓
CalculatorEngine
        ↓
ResultFormatter
```

모드별 계산 클래스:

```text
StatisticsCalculator
QuadraticEquationSolver
ComplexCalculator
AngleConverter
CalculationHistory
```

의존 방향:

- `app/`은 `core/`, `modes/`를 사용할 수 있다.
- `modes/`는 필요한 `core/` 유틸리티를 사용할 수 있다.
- `core/`는 콘솔 입출력에 의존하지 않는다.
- 테스트는 가능한 한 콘솔을 거치지 않고 계산 클래스를 직접 호출한다.

---

## 7. 최종 폴더 구조

```text
cpp_calculator/
├─ CMakeLists.txt
├─ README.md
├─ main.cpp
├─ app/
│  ├─ ConsoleApplication.h
│  ├─ ConsoleApplication.cpp
│  ├─ ConsoleInput.h
│  └─ ConsoleInput.cpp
├─ core/
│  ├─ CalculatorError.h
│  ├─ CalculatorState.h
│  ├─ CalculatorState.cpp
│  ├─ Token.h
│  ├─ Tokenizer.h
│  ├─ Tokenizer.cpp
│  ├─ ExpressionParser.h
│  ├─ ExpressionParser.cpp
│  ├─ CalculatorEngine.h
│  ├─ CalculatorEngine.cpp
│  ├─ CalculatorController.h
│  ├─ CalculatorController.cpp
│  ├─ ResultFormatter.h
│  ├─ ResultFormatter.cpp
│  ├─ AngleConverter.h
│  ├─ AngleConverter.cpp
│  ├─ CalculationHistory.h
│  └─ CalculationHistory.cpp
├─ modes/
│  ├─ StatisticsCalculator.h
│  ├─ StatisticsCalculator.cpp
│  ├─ StatisticsController.h
│  ├─ StatisticsController.cpp
│  ├─ QuadraticEquationSolver.h
│  ├─ QuadraticEquationSolver.cpp
│  ├─ EquationController.h
│  ├─ EquationController.cpp
│  ├─ ComplexCalculator.h
│  ├─ ComplexCalculator.cpp
│  ├─ ComplexController.h
│  └─ ComplexController.cpp
├─ tests/
│  ├─ TestHarness.h
│  ├─ CalculatorStateTests.cpp
│  ├─ TokenizerTests.cpp
│  ├─ ExpressionParserTests.cpp
│  ├─ ScientificFunctionTests.cpp
│  ├─ ResultFormatterTests.cpp
│  ├─ StatisticsTests.cpp
│  ├─ EquationTests.cpp
│  ├─ ComplexTests.cpp
│  └─ IntegrationTests.cpp
└─ tools/
   └─ compare_with_python.py
```

기존 `gui/` 폴더는 상태 로직 이식 후 삭제한다.

---

## 8. 파서 설계

외부 수식 라이브러리나 `eval` 계열 기능을 사용하지 않고 재귀 하강 파서를 직접 만든다.

문법:

```text
expression  → term ((PLUS | MINUS) term)*
term        → unary ((MULTIPLY | DIVIDE) unary)*
unary       → (PLUS | MINUS) unary | power
power       → postfix (POWER unary)?
postfix     → primary (FACTORIAL | PERCENT)*
primary     → NUMBER
            | CONSTANT
            | ANS
            | function_call
            | LEFT_PAREN expression RIGHT_PAREN

function_call → IDENTIFIER LEFT_PAREN arguments? RIGHT_PAREN
arguments     → expression (COMMA expression)*
```

토큰 종류:

```text
NUMBER
IDENTIFIER
PLUS
MINUS
MULTIPLY
DIVIDE
POWER
FACTORIAL
PERCENT
COMMA
LEFT_PAREN
RIGHT_PAREN
END
```

Tokenizer 단계에서 유니코드 연산 기호를 표준 토큰으로 정규화한다.

---

## 9. 콘솔 UI 설계

## 9.1 메인 메뉴

```text
==================================================
          Scientific Calculator C++
==================================================
Angle: DEG    Format: NORM    Ans: 0

1. Calculate
2. Statistics
3. Quadratic Equation
4. Complex Number
5. Settings
6. History
0. Exit

Select:
```

## 9.2 일반 계산 화면

```text
[Calculate | DEG | NORM]
Expression (:back, :history, :help): 2+3*4
Result: 14
```

명령:

```text
:back       메인 메뉴
:history    계산 기록
:help       지원 문법
:drg        DEG/RAD/GRAD 순환
:fmt        NORM/FIX4/SCI4 순환
:sd         최근 결과 소수·분수 전환
:clear      현재 표시 상태 초기화
```

## 9.3 입력 안정성

- 모든 입력은 `getline`으로 한 줄 전체를 읽는다.
- 숫자는 엄격하게 변환하고 뒤에 쓰레기 문자가 남으면 거부한다.
- `cin` 실패 상태로 무한 루프에 빠지지 않도록 한다.
- EOF 입력은 정상 종료로 처리한다.
- Windows 콘솔은 UTF-8 출력 설정을 시도한다.
- 유니코드가 깨지는 환경을 위해 모든 핵심 기능에 ASCII 입력 별칭을 둔다.

---

## 10. 자동 실행용 명령줄 인터페이스

Python과 자동 비교하기 위해 대화형 메뉴 외에 단일 계산 모드를 제공한다.

```powershell
scientific_calculator.exe --eval "2+3*4"
scientific_calculator.exe --eval "sin(30)" --angle DEG
scientific_calculator.exe --eval "1/3" --format FIX
scientific_calculator.exe --help
scientific_calculator.exe --version
```

종료 코드:

```text
0  성공
1  계산 또는 입력 오류
2  잘못된 명령줄 옵션
```

대화형 모드와 `--eval` 모드는 반드시 같은 계산 엔진과 포매터를 사용한다.

---

## 11. 테스트 전략

외부 GoogleTest 설치를 요구하지 않는다. 프로젝트 내부에 간단한 테스트 하네스를 둔다.

필요 기능:

```text
EXPECT_EQ
EXPECT_NEAR
EXPECT_TRUE
EXPECT_THROWS_MESSAGE
테스트별 성공·실패 출력
실패 시 0이 아닌 종료 코드
```

CTest에 각 테스트 실행 파일을 등록한다.

### 단위 테스트

- CalculatorState 상태 순환
- Tokenizer 토큰과 위치
- Parser 우선순위와 결합 방향
- 함수 인자 개수
- 함수 정의역
- Overflow 경계
- 결과 포맷
- 분수 근사
- 통계 계산
- 이차방정식
- 복소수 변환

### 통합 테스트

- 성공한 일반 계산만 `Ans` 갱신
- 오류 시 `Ans` 유지
- 성공한 일반 계산만 기록에 추가
- FMT와 S⇔D가 재계산하지 않음
- DRG가 삼각함수와 복소수 위상각에 함께 적용
- 오류 문구가 Python과 정확히 일치

### Python/C++ 동등성 테스트

`tools/compare_with_python.py`가 다음을 수행한다.

1. 공통 테스트 식을 Python 계산기로 실행한다.
2. 같은 식과 상태를 C++ `--eval`로 실행한다.
3. 결과 또는 오류 문자열을 정규화해 비교한다.
4. 불일치한 식을 한 줄씩 출력한다.
5. 하나라도 다르면 실패 종료 코드를 반환한다.

---

## 12. 최소 동등성 테스트 목록

### 기본 수식

```text
2+3*4
(2+3)*4
-5+3
2^3^2
-2^2
(-2)^2
1/3
50%
5!
```

### 공학 함수

```text
sqrt(16)
sqrt(-1)
sin(30)
cos(60)
tan(45)
asin(0.5)
log(100)
ln(e)
recip(4)
root(3,-8)
```

### 정수형 함수

```text
npr(10,3)
ncr(10,3)
gcd(12,18)
lcm(12,18)
quot(-10,3)
rem(-10,3)
mod(-10,3)
```

### 상태와 오류

```text
Ans*4
1/0
sin(
171!
randint(5,2)
unknown(1)
```

### 별도 모드

```text
통계: [1,2,3,4]
통계: 데이터 1개
방정식: (1,-5,6)
방정식: (1,2,1)
방정식: (1,0,1)
복소수 직교형: (3,4)
복소수 극형 DEG: (5,53.13010235415598)
복소수 순허수: (0,1)
```

---

## 13. 구현 단계와 커밋 계획

## Phase 0 — Qt 제거 및 콘솔 전환

작업:

- CMake의 Qt 탐색과 링크 제거
- Qt용 `main.cpp`를 콘솔 진입점으로 교체
- 기존 CalculatorState 재사용 여부 검토 및 수정
- 콘솔 메뉴 뼈대 생성
- Qt GUI 파일 제거
- C++ README의 빌드 방법 변경

완료 조건:

- Qt가 설치되지 않은 Visual Studio에서 빌드됨
- 메뉴가 표시되고 정상 종료됨
- 상태 테스트가 통과함

커밋 예시:

```text
refactor(cpp): replace Qt prototype with console application skeleton
```

---

## Phase 1 — 오류 계층, Tokenizer, Parser

작업:

- CalculatorError
- Token 구조
- Tokenizer
- 재귀 하강 Parser
- 사칙연산
- 괄호
- 단항 부호
- 거듭제곱
- 기본 오류 처리

완료 조건:

- 우선순위·결합 방향 테스트 통과
- `--eval "2+3*4"`가 `14` 출력
- 잘못된 괄호와 0 나눗셈 처리

커밋 예시:

```text
feat(cpp): implement tokenizer and recursive-descent parser
```

---

## Phase 2 — 공학 함수와 상수

작업:

- 모든 실수 공학 함수
- `pi`, `π`, `e`, `Ans`
- 팩토리얼·순열·조합
- 정수 검사와 Overflow 검사
- 난수 생성기 주입 구조

완료 조건:

- Python과 함수 결과·오류 문구 일치
- 고정 seed 난수 테스트 가능
- 170!/171! 경계 통과

커밋 예시:

```text
feat(cpp): add scientific functions constants and Ans
```

---

## Phase 3 — 상태, 포매터, S⇔D, 기록

작업:

- DEG/RAD/GRAD
- NORM/FIX4/SCI4
- ResultFormatter
- 연분수 기반 S⇔D
- CalculatorController
- CalculationHistory
- 설정·기록 콘솔 메뉴

완료 조건:

- Python 포맷 테스트와 일치
- 오류 계산 후 Ans 유지
- FMT/S⇔D가 재계산하지 않음

커밋 예시:

```text
feat(cpp): add result formatting fraction toggle and history
```

---

## Phase 4 — 통계 모드

작업:

- 데이터 파서
- 데이터 저장·추가·삭제·초기화
- Welford 기반 요약 통계
- 통계 콘솔 메뉴

완료 조건:

- 빈 데이터·1개 데이터·일반 데이터 테스트 통과
- 잘못된 입력 시 기존 데이터 보존
- Python 통계값과 일치

커밋 예시:

```text
feat(cpp): implement one-variable statistics mode
```

---

## Phase 5 — 이차방정식 모드

작업:

- 안정적인 이차방정식 Solver
- 실근·중근·복소근 분류
- 판별식
- 방정식 콘솔 메뉴

완료 조건:

- Python의 모든 방정식 테스트와 일치
- 거의 0인 판별식 처리
- 큰 계수 Overflow 처리

커밋 예시:

```text
feat(cpp): implement quadratic equation mode
```

---

## Phase 6 — 복소수 모드

작업:

- 직교형 입력
- 극형 입력
- 크기·위상각·켤레
- DEG/RAD/GRAD 연동
- `j` 포맷
- 복소수 콘솔 메뉴

완료 조건:

- Python Complex 테스트와 일치
- 미세한 실수·허수 잔차 제거
- 음수 크기 오류 처리

커밋 예시:

```text
feat(cpp): implement complex conversion mode
```

---

## Phase 7 — 전체 콘솔 통합

작업:

- 메인 메뉴와 모든 하위 메뉴 완성
- 도움말
- 입력 오류 복구
- Windows UTF-8 초기화
- `--eval`, `--help`, `--version`

완료 조건:

- 모든 메뉴에서 안전하게 메인으로 돌아감
- EOF와 잘못된 입력으로 프로그램이 비정상 종료되지 않음
- 대화형과 비대화형 모드가 같은 엔진 사용

커밋 예시:

```text
feat(cpp): complete interactive console workflow
```

---

## Phase 8 — 동등성 검증과 안정화

작업:

- 공통 테스트 케이스
- Python/C++ 비교 스크립트
- 경계값 테스트
- MSVC 경고 정리
- 코드 중복 제거

완료 조건:

- 모든 C++ 테스트 통과
- 지원 범위의 Python/C++ 동등성 테스트 통과
- 프로젝트 코드에서 새로 발생한 `/W4` 경고 없음
- Qt 의존성 완전 제거

커밋 예시:

```text
test(cpp): add cross-language parity and boundary coverage
```

---

## Phase 9 — 문서와 최종 릴리스 정리

작업:

- 루트 README를 Python GUI + C++ 콘솔 구조로 수정
- `cpp_calculator/README.md` 완성
- `docs/CURRENT_STATUS.md` 갱신
- 빌드·실행·테스트 예시 작성
- 기능표와 제한사항 작성

완료 조건:

- 처음 보는 사용자가 문서만 보고 빌드·실행·테스트 가능
- Qt 설치나 Qt 확장이 필요하지 않음

커밋 예시:

```text
docs: finalize C++ console calculator release guide
```

---

## 14. 최종 빌드·테스트 명령

Visual Studio 개발자 PowerShell 또는 일반 PowerShell에서:

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
.\build\Debug\scientific_calculator.exe
```

Visual Studio가 Ninja를 사용하는 경우 실행 파일 위치가 달라질 수 있으므로 README에 두 방식 모두 기록한다.

---

## 15. 코드 품질 규칙

- 헤더에서 `using namespace std;` 금지
- RAII와 값 타입 우선
- 소유권을 가진 raw pointer 금지
- 전역 가변 상태 금지
- 콘솔과 테스트에서 계산 로직 중복 금지
- 난수 생성기를 주입해 테스트 가능하게 설계
- 모든 결과에 `std::isfinite` 검사
- 오류 문구를 중앙에서 관리
- 헤더는 작고 책임이 분명해야 함
- 함수 하나는 한 가지 역할만 수행
- 주석은 문법 설명보다 설계 이유와 경계 조건을 설명
- 소스 파일은 UTF-8로 컴파일
- MSVC `/W4` 기준으로 정리

---

## 16. 최종 완료 체크리스트

### 빌드

- [ ] Qt 없이 Visual Studio 2026에서 빌드
- [ ] CMake 명령으로 빌드
- [ ] CTest 전체 통과
- [ ] 활성 CMake와 소스에 Qt 참조 없음

### 일반 계산

- [ ] 사칙연산과 우선순위
- [ ] 괄호와 단항 부호
- [ ] 거듭제곱·팩토리얼·백분율
- [ ] 공학 함수
- [ ] 상수와 Ans
- [ ] 난수 함수
- [ ] 오류 문구

### 상태와 출력

- [ ] DEG/RAD/GRAD
- [ ] NORM/FIX4/SCI4
- [ ] S⇔D
- [ ] 음수 0 정규화
- [ ] 계산 기록

### 별도 모드

- [ ] 1변수 통계
- [ ] 이차방정식
- [ ] 복소수 직교형·극형 변환

### 검증

- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] Python/C++ 동등성 테스트 통과
- [ ] 경계값·Overflow 테스트 통과
- [ ] 대화형 수동 점검 통과

### 문서

- [ ] 루트 README 수정
- [ ] C++ README 완성
- [ ] CURRENT_STATUS 수정
- [ ] 알려진 제한사항 기록

---

## 17. 최종 사용자 사용 흐름

모든 구현이 끝난 뒤 사용자는 다음만 실행하면 된다.

```powershell
cd C:\Users\user\cal
git pull origin main
cd cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
.\build\Debug\scientific_calculator.exe
```

최종 저장소 구조:

```text
python_calculator/  → 완성된 PySide6 GUI 기준 구현
cpp_calculator/     → 완성된 Visual Studio C++ 콘솔 계산기
docs/               → 요구사항·계획·진행 상태
shared_tests/        → 필요한 공통 비교 입력
```

---

## 18. 다음 대화 복원 규칙

향후 AI가 이 문서를 읽으면 다음처럼 행동한다.

1. C++ 콘솔 결정이 기존 Qt 요구사항보다 최신임을 인정한다.
2. Python 완성본을 계산 동작의 기준으로 사용한다.
3. GitHub에서 가장 먼저 완료되지 않은 Phase를 확인한다.
4. 사용자가 변경을 요구하지 않으면 구조를 다시 논의하지 않는다.
5. 작업 단위를 구현하고 테스트한 뒤 `rjsxo943-gif/cal`의 `main`에 커밋한다.
6. 테스트와 완료 조건을 통과하기 전에는 해당 Phase가 완료됐다고 말하지 않는다.
7. 최종 완료 전까지 `docs/CURRENT_STATUS.md`를 매 단계 갱신한다.

---

## 한 줄 프로젝트 정의

> 완성된 Python/PySide6 공학용 계산기를 기준 구현으로 유지하고, 동일한 계산 기능·모드·표시·상태·오류를 제공하는 외부 의존성 없는 Visual Studio C++17 콘솔 계산기를 완성한다.
