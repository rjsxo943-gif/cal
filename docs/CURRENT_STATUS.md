# Scientific Calculator Current Status

> 이 문서는 `SCIENTIFIC_CALCULATOR_DEVELOPMENT_ROADMAP.md`의 세부 진행 상태를 빠르게 복원하기 위한 최신 체크포인트다.

## Current phase

```text
Python 기본 계산 엔진       완료
공학 함수                  완료
Ans / DEG / RAD / GRAD     완료
NORM / FIX / SCI / S⇔D     완료
SHIFT 버튼 라벨 전환       완료
이차방정식 모드            완료
1변수 통계 모드            다음 작업
복소수 모드                후속 작업
C++ 병렬 구현              Python 핵심 모드 이후 진행
```

## Latest completed feature

### Quadratic Equation mode

MODE 메뉴에서 `Equation`을 선택하면 다음 형태의 방정식을 계산한다.

```text
ax² + bx + c = 0
```

지원 결과:

- 서로 다른 두 실근
- 중근
- 두 복소근
- 판별식 표시
- `a = 0` 오류 처리
- NORM / FIX / SCI 표시 형식 동기화

관련 구조:

```text
EquationPage
↓
EquationController
↓
QuadraticEquationSolver
↓
ResultFormatter
```

## Next task

1변수 통계 모드를 구현한다.

예정 범위:

- 데이터 여러 개 입력
- 데이터 목록 표시 및 삭제
- 개수 `n`
- 합계 `Σx`
- 평균
- 최솟값 / 최댓값
- 모집단 분산 / 표준편차
- 표본 분산 / 표준편차
- FMT 표시 형식 동기화

## Resume instruction

새 대화에서 이 파일을 읽은 AI는 다음 작업을 `1변수 통계 모드 구현`으로 판단한다.
