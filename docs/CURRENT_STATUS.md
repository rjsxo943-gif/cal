# Scientific Calculator Current Status

## Current phase

```text
Python PySide6 계산기          완료
C++ 계산 엔진                 완료
C++ CLI 1.0                   완료
C++ Win32 버튼형 GUI          구현 완료
Visual Studio 솔루션          추가 완료
C++ 계산 엔진 테스트         94개 통과
Windows/MSVC GUI 실기동       사용자 환경 확인 대기
```

## C++ 최신 방향

C++ 기본 실행 화면은 콘솔이 아니라 **순수 Win32 API 버튼형 GUI**다.

```text
cpp_calculator\ScientificCalculator.sln
```

CMake를 설치하지 않아도 위 솔루션을 Visual Studio에서 직접 열 수 있다.

솔루션 프로젝트:

```text
ScientificCalculator   C++17 Win32 버튼형 공학용 계산기
CalculatorTests        계산 엔진 자동 테스트
```

기존 CLI는 삭제하지 않고 선택 실행 대상으로 유지했다.

## GUI 완료 기능

### CALC

- 수식 입력창과 결과 표시창
- 48개 계산·상태·편집 버튼
- 숫자, 사칙연산, 괄호, 거듭제곱
- 삼각함수, 역삼각함수, 로그, 제곱근
- 순열·조합, GCD·LCM, 몫·나머지
- 팩토리얼, 퍼센트, 절댓값, 역수
- `pi`, `e`, `Ans`, 난수
- SHIFT 라벨·입력 전환
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4
- S⇔D
- 왼쪽·오른쪽 커서, DEL, AC
- Enter 계산, Esc 초기화
- 계산 기록과 더블클릭 수식 복원

### STAT

- 여러 데이터 입력
- 추가, 선택 삭제, 전체 삭제
- 개수, 합, 평균, 최솟값, 최댓값
- 모집단·표본 분산과 표준편차

### EQN

- 이차방정식 `ax² + bx + c = 0`
- 서로 다른 실근, 중근, 복소근

### CMPLX

- 직교형·극형 입력
- 복소수, 켤레복소수, 크기, 위상
- DEG / RAD / GRAD 상태 연동

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

GUI는 기존 계산 엔진을 재사용하며 수식을 직접 해석하지 않는다.

## Build without CMake

```text
1. cpp_calculator\ScientificCalculator.sln 열기
2. Debug / x64 선택
3. ScientificCalculator를 시작 프로젝트로 설정
4. Ctrl+F5 또는 F5
```

필요한 Visual Studio 구성:

```text
C++를 사용한 데스크톱 개발
Windows 10 또는 Windows 11 SDK
MSVC x64/x86 빌드 도구
```

Qt와 CMake는 Visual Studio 솔루션 빌드에 필요하지 않다.

## Validation

기존 계산 엔진은 이전 개발 환경에서 다음 검증을 통과했다.

```text
Passed: 94
Failed: 0
```

Win32 GUI 코드는 Windows 전용 헤더와 MSVC가 없는 현재 작업 환경에서 작성했기 때문에 실제 Windows 컴파일·실행 여부는 사용자의 Visual Studio에서 최종 확인해야 한다. 오류가 발견되면 해당 MSVC 오류 메시지를 기준으로 수정한다.

## Resume instruction

다음 작업은 사용자가 `ScientificCalculator.sln`을 빌드한 결과를 확인하고 Windows/MSVC 호환 오류 또는 GUI 배치 문제를 수정하는 것이다.
