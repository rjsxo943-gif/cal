# Scientific Calculator Current Status

## Current phase

```text
Python PySide6 계산기          완료
C++ 콘솔 계산기 1.0           완료
C++ Qt 시제품                  제거
C++ 자동 테스트               94개 통과
Python/C++ 비교 도구           추가
```

## C++ 1.0

`cpp_calculator/`는 Qt 없이 Visual Studio와 CMake로 빌드되는 C++17 콘솔 공학용 계산기다.

완료 기능:

- 사용자 정의 Tokenizer 및 재귀 하강 Parser
- 사칙연산, 괄호, 단항 부호, 오른쪽 결합 거듭제곱
- 팩토리얼, 퍼센트, 과학적 표기 숫자
- 삼각함수·역삼각함수·로그·제곱근
- 순열·조합·정수 함수·n제곱근·난수
- pi, e, Ans
- DEG / RAD / GRAD
- NORM / FIX4 / SCI4 / S⇔D
- 계산 기록
- 1변수 통계
- 이차방정식
- 복소수 직교형·극형 변환
- 대화형 메뉴와 `--eval` 실행 모드
- 공통 오류 메시지

## Validation

개발 환경에서 다음을 확인했다.

```text
CMake configure 성공
C++17 strict warning build 성공
CTest 100% 통과
Passed: 94, Failed: 0
대화형 메뉴 수동 입력 확인
--eval 수식 실행 확인
```

GitHub Actions 워크플로는 아직 없으므로 위 결과는 개발 환경에서 수행한 로컬 검증 결과다.

## Build

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
.\build\Debug\scientific_calculator.exe
```

단일 구성 생성기에서는 실행 파일 경로가 `build/scientific_calculator.exe`일 수 있다.

## Resume instruction

C++ 콘솔 1.0은 완료 상태다. 다음 작업은 사용자의 Visual Studio 빌드 결과를 확인하고 발견되는 Windows/MSVC 호환 문제를 수정하는 것이다.
