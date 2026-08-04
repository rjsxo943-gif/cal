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
1변수 통계 모드            완료
복소수 모드                다음 작업
C++ 병렬 구현              Python 핵심 모드 이후 진행
```

## Latest completed feature

### One-Variable Statistics mode

MODE 메뉴에서 `Statistics`를 선택하면 실수 데이터를 입력하고 다음 통계량을 확인할 수 있다.

- 데이터 개수 `n`
- 합계 `Σx`
- 평균 `x̄`
- 최솟값 / 최댓값
- 모집단 분산 `σ²`
- 모집단 표준편차 `σ`
- 표본 분산 `s²`
- 표본 표준편차 `s`

입력 방식:

```text
10
10, 20, 30
10 20 30
10;20;30
```

지원 동작:

- 데이터 한 개 또는 여러 개 추가
- 목록에서 선택 삭제
- 전체 초기화
- 공통 AC 버튼으로 통계 데이터 초기화
- NORM / FIX / SCI 표시 형식 동기화
- 데이터가 1개일 때 표본 분산·표준편차를 `—`로 표시

관련 구조:

```text
StatisticsPage
↓
StatisticsController
↓
OneVariableStatisticsCalculator
↓
ResultFormatter
```

## Previously completed mode

### Quadratic Equation mode

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

## Next task

복소수 모드를 구현한다.

예정 범위:

- 직교형 `a + bi`
- 복소수 덧셈 / 뺄셈 / 곱셈 / 나눗셈
- 절댓값과 위상각
- 켤레복소수
- 실수부 / 허수부
- 직교형 ↔ 극형 변환
- DEG / RAD / GRAD 연동
- NORM / FIX / SCI 표시 형식 동기화

## Resume instruction

새 대화에서 이 파일을 읽은 AI는 다음 작업을 `복소수 모드 구현`으로 판단한다.
