# Scientific Calculator Current Status

> 이 문서는 프로젝트의 최신 진행 상태를 빠르게 복원하기 위한 체크포인트다.

## Current phase

```text
Python 기본 계산 엔진       완료
Python 공학 함수            완료
Python 상태·표시 기능       완료
Python 이차방정식 모드      완료
Python 1변수 통계 모드      완료
Python 복소수 모드          완료
Python GUI                  완료
C++ Qt GUI 시제품           폐기 예정
C++ 콘솔 완성 계획서       완료
C++ 콘솔 Phase 0           다음 작업
```

## 최신 방향 변경

기존에는 C++ 버전을 Qt Widgets GUI로 구현할 계획이었지만, 최신 사용자 결정에 따라 C++ 버전은 Visual Studio 콘솔 프로그램으로 변경한다.

```text
Python → PySide6 GUI 기준 구현
C++    → Qt 없는 Visual Studio 콘솔 구현
```

Qt 설치와 Qt 의존성은 더 이상 필요하지 않다.

현재 저장소의 C++ Qt 코드는 초기 시제품이며 다음 Phase에서 활성 빌드와 작업 트리에서 제거한다. 필요한 상태 로직만 콘솔 프로젝트로 옮긴다.

## 기준 문서

C++ 구현의 전체 범위, 구조, 테스트, 커밋 순서, 완료 조건은 다음 문서에 고정했다.

```text
docs/CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md
```

이 문서는 다음을 포함한다.

- Python 완성본과 맞출 기능 범위
- C++ 1.0 제외 범위
- 재귀 하강 Parser 문법
- 콘솔 메뉴와 명령
- 최종 폴더 구조
- 단위·통합·Python/C++ 동등성 테스트
- Phase 0~9 구현 순서
- 최종 완료 체크리스트

## Python implementation status

Python 버전은 C++의 계산 동작 기준으로 사용한다.

```text
CALC  기본·공학 계산
STAT  1변수 통계
EQN   이차방정식
CMPLX 복소수 직교형·극형 변환
```

현재 확인된 Python 전체 테스트 기준은 `174 passed`다.

## Next task — C++ Phase 0

Qt 프로젝트를 외부 의존성 없는 콘솔 프로젝트로 전환한다.

작업 순서:

1. CMake에서 Qt 탐색·링크 제거
2. `main.cpp`를 콘솔 진입점으로 교체
3. `CalculatorState` 재사용·정리
4. 메인 콘솔 메뉴 뼈대 구현
5. Qt GUI 파일 삭제
6. Visual Studio/MSVC 빌드 확인
7. CTest 상태 테스트 확인
8. C++ README를 콘솔 기준으로 수정

완료 조건:

```text
Qt가 없는 환경에서 configure 성공
C++ 프로그램 빌드 성공
메인 메뉴 출력
정상 종료
CalculatorState 테스트 통과
```

## Resume instruction

새 대화에서 이 파일을 읽은 AI는 다음 작업을 `CPP_CONSOLE_CALCULATOR_MASTER_PLAN.md의 Phase 0 구현`으로 판단한다.
