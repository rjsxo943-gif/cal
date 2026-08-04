# Scientific Calculator Dual Implementation
## Development Roadmap / AI Context Refresh

> 이 문서는 Python(PySide6)과 C++(Qt Widgets)로 기능과 결과가 최대한 동일한 공학용 계산기를 병렬 개발하기 위한 진행 기준 문서다.  
> 새 대화나 작업 재개 시 이 문서를 기준으로 현재 상태와 다음 작업을 복원한다.

---

# 1. 프로젝트 목표

Casio fx-991ES PLUS 수준의 주요 기능을 가진 GUI 공학용 계산기를 두 언어로 구현한다.

## Python 버전

- 언어: Python
- GUI: PySide6
- IDE: VS Code
- 프로젝트 경로: `C:\Users\user\cal\python_calculator`

## C++ 버전

- 언어: C++
- GUI: Qt Widgets
- IDE: Visual Studio
- 프로젝트 경로: `C:\Users\user\cal\cpp_calculator`

## GitHub 저장소

- Repository: `rjsxo943-gif/cal`
- 기본 브랜치: `main`

---

# 2. 핵심 개발 원칙

## 2.1 GUI와 계산 엔진 분리

```text
GUI
↓
CalculatorController
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

GUI 코드 안에서 직접 수식을 계산하지 않는다.

## 2.2 Python과 C++ 병렬 개발

한 언어를 전부 완성한 뒤 다른 언어로 번역하지 않는다.

```text
Python에서 기능 구현
→ C++에서 같은 기능 구현
→ 동일 입력으로 결과 비교
```

## 2.3 코드 제공 규칙

- 사용자가 명시적으로 코드를 요청했을 때만 코드를 작성한다.
- 구현 전에는 구조, 선택지, 장단점부터 검토한다.
- 코드를 작성할 때는 주석을 충분히 넣는다.
- 클래스, 함수, 문법이 왜 필요한지 설명한다.
- 한 번에 지나치게 많은 코드를 주지 않고 기능 단위로 나눈다.
- Python과 C++의 클래스명과 책임은 최대한 대응시킨다.

## 2.4 GitHub 작업 방식

```text
설계 및 작업 범위 결정
→ GitHub 코드 반영
→ 사용자가 git pull
→ 로컬 실행 확인
→ 오류 또는 결과 공유
→ 다음 단계 진행
```

가상환경과 빌드 결과는 GitHub에 올리지 않는다.

---

# 3. 현재 진행 상태

## 완료

### Phase 0 — Python 환경

- Python 가상환경 `.venv` 생성
- PySide6 설치
- pytest 설치
- Git 설치
- GitHub 저장소 생성 및 연결
- `.gitignore` 작성
- Python 프로젝트 폴더 구조 생성

### Phase 1 — Python GUI 뼈대

다음 파일에 초기 GUI가 구현되어 있다.

```text
python_calculator/
├─ main.py
└─ gui/
   ├─ main_window.py
   ├─ calculator_widget.py
   ├─ display_panel.py
   ├─ control_panel.py
   ├─ history_panel.py
   └─ styles.py
```

현재 지원되는 GUI 동작:

- 프로그램 창 실행
- 수식 입력창
- 결과 표시창
- 숫자 및 기본 공학 함수 버튼
- 현재 커서 위치에 문자 삽입
- 왼쪽·오른쪽 커서 이동
- DEL
- AC
- SHIFT 활성 표시
- `SHIFT + sin → asin(`
- `SHIFT + cos → acos(`
- `SHIFT + tan → atan(`
- `SHIFT + log → 10^(`
- `SHIFT + ln → e^(`
- MODE 메뉴
- Calculate / Statistics / Equation / Complex 화면 전환
- 계산 기록 패널 열기·닫기
- 기록 항목 더블클릭 시 수식 복원

현재 `=`을 누르면 실제 계산 대신 다음 문구가 표시된다.

```text
ENGINE NOT CONNECTED
```

즉, GUI 뼈대는 동작하지만 계산 엔진은 아직 연결되지 않았다.

---

# 4. 전체 진행률

현재 위치:

```text
Phase 0 환경 설정       완료
Phase 1 GUI 뼈대        약 80% 완료
Phase 2 기본 계산 엔진  다음 작업
```

전체 1차 완성 기준 진행률은 약 15~20%로 본다.

버튼과 화면보다 수식 파서, 상태 관리, 결과 통일, Python/C++ 비교 테스트의 작업량이 더 크다.

---

# 5. 1차 완성까지 남은 8개 큰 단계

## Step 1 — Python 기본 계산 엔진

### 구현 범위

- 숫자
- 소수
- `+`
- `-`
- `*`
- `/`
- `^`
- 괄호
- 중첩 괄호
- 단항 음수
- 연산자 우선순위
- 기본 오류 처리

### 내부 구성

```text
Tokenizer
ExpressionParser
CalculatorEngine
CalculatorController
pytest
```

### 파서 우선순위 구조

```text
expression  → +, -
term        → *, /
power       → ^
unary       → 단항 +, 단항 -
primary     → 숫자, 괄호
```

거듭제곱은 오른쪽 결합으로 처리한다.

```text
2^3^2
→ 2^(3^2)
→ 512
```

### 완료 기준

```text
2+3         → 5
2+3*4       → 14
(2+3)*4     → 20
-5+3        → -2
3*-2        → -6
2^10        → 1024
10/4        → 2.5
5/0         → Division by zero
(2+3        → Syntax ERROR
```

GUI 완료 기준:

```text
2+3*4 입력
→ = 클릭
→ 결과창에 14 표시
→ 기록 패널에 2+3*4 = 14 추가
```

---

## Step 2 — C++ 환경 및 동일 GUI 뼈대

Python GUI 구조를 기준으로 C++ Qt Widgets 프로젝트를 만든다.

```text
MainWindow
CalculatorWidget
DisplayPanel
ControlPanel
HistoryPanel
```

완료 기준:

- Python과 유사한 창 크기와 영역 구조
- 버튼 배치 대응
- SHIFT 동작 대응
- MODE 전환 대응
- 기록 패널 대응
- 실제 계산은 아직 연결하지 않아도 됨

---

## Step 3 — C++ 기본 계산 엔진

Python과 동일한 수식 규격으로 구현한다.

```text
Tokenizer
ExpressionParser
CalculatorEngine
CalculatorController
```

완료 기준:

- Python과 같은 테스트 입력 사용
- 같은 결과 출력
- 같은 오류 메시지 출력
- 거듭제곱 결합 방향 일치
- 단항 음수 처리 일치

---

## Step 4 — 공학 함수

Python과 C++에서 기능 단위로 병렬 구현한다.

### 상수 및 기본 함수

- `π`
- `e`
- 절댓값
- 역수
- 제곱
- 거듭제곱
- 제곱근
- n제곱근

### 삼각함수

- `sin`
- `cos`
- `tan`
- `asin`
- `acos`
- `atan`

### 로그 및 지수

- `log`
- `ln`
- `10^x`
- `e^x`

### 정수·특수 계산

- 팩토리얼
- 순열 `nPr`
- 조합 `nCr`
- 나머지
- GCD
- LCM
- 몫과 나머지
- 난수
- 백분율

---

## Step 5 — 상태와 결과 표시

### CalculatorState

- 현재 계산 모드
- DEG / RAD / GRAD
- SHIFT
- Ans
- 표시 모드
- 분수·소수 표시 상태

### 각도 처리

```text
DEG
RAD
GRAD
```

개별 각도 단위:

```text
30°
pi/2 r
50 g
```

### 결과 표시

- NORM
- FIX
- SCI
- 최대 10자리 수준
- Python과 C++의 동일한 반올림 규칙
- S⇔D
- Ans
- 계산 기록

---

## Step 6 — Statistics 및 Equation 모드

### Statistics

1변수 통계:

- 데이터 개수
- 합계
- 평균
- 최솟값
- 최댓값
- 분산
- 모집단 표준편차
- 표본 표준편차

### Equation

이차방정식:

```text
ax² + bx + c = 0
```

처리 결과:

- 서로 다른 두 실근
- 중근
- 두 복소근

---

## Step 7 — Complex 모드

전자공학 활용을 위해 1차 완성 범위에 포함한다.

### 직교형

```text
a + bi
```

지원 기능:

- 덧셈
- 뺄셈
- 곱셈
- 나눗셈
- 절댓값
- 켤레복소수
- 실수부
- 허수부

### 극형

```text
r∠θ
```

지원 기능:

- 직교형 → 극형
- 극형 → 직교형
- 크기
- 위상각

관련 기능:

```text
i
∠
Abs
Arg
Conj
Re
Im
Pol
Rec
```

---

## Step 8 — 최종 통합 및 비교 테스트

최종 검증 항목:

- 마우스 입력
- 키보드 입력
- 커서 이동
- SHIFT
- MODE
- 계산 기록
- 오류 메시지
- 각도 처리
- 결과 반올림
- Python/C++ 결과 비교
- README 및 실행 방법
- 코드 주석과 클래스 책임 검토

공통 테스트 예시:

```text
2+3*4
(2+3)*4
-5+3
1/3
sqrt(16)
2^10
sin(30°)
sin(pi/2 r)
log(100)
ln(e)
5!
10C3
gcd(12,18)
lcm(12,18)
sqrt(-1)
(2+3i)*(4-i)
2∠30°
```

---

# 6. 1차 완성 이후 확장

다음 기능은 초기 텍스트 기반 계산기 완성 후 진행한다.

## 자연스러운 수학식 표시

- 세로 분수
- 수학식 형태의 루트
- 위첨자 지수
- 분수 내부 커서 이동
- 구조화된 수식 편집

## 추가 Future Work

- M+
- M-
- MR
- MC
- A, B, C, D, X, Y 변수
- 삼차방정식
- 연립방정식
- 단위 변환
- 소인수분해
- 기록 파일 저장
- 프로그램 재실행 후 기록 복원
- 그래프
- 회귀분석

---

# 7. 세부 작업량 예상

## Python 기본 계산기

남은 큰 작업은 약 4~6개다.

## Python과 C++의 1차 완성

남은 큰 단계는 약 8개다.

기능 구현, 테스트, 검토를 세분화하면 약 20~30회의 작업 사이클이 필요하다.

## 자연스러운 수학식 표시까지 포함

1차 완성 이후 약 4~8개의 추가 작업이 필요하다.

---

# 8. 바로 다음 작업

현재 최우선 작업은 **Python 기본 계산 엔진**이다.

진행 순서:

```text
1. 기본 수식 문법 최종 확인
2. Token 및 TokenType 설계
3. Tokenizer 구현
4. ExpressionParser 구현
5. CalculatorEngine 구현
6. 공통 오류 정의
7. CalculatorController 구현
8. GUI 연결
9. pytest 테스트
10. 로컬 GUI 실행 확인
```

이번 Step에서는 삼각함수, 복소수, 통계 기능을 섞지 않는다.

완료 목표:

```text
2+3*4 = 14
```

가 GUI에서 실제로 계산되고 기록 패널에 추가되는 상태.

---

# 9. AI 작업 재개 규칙

이 문서를 제공받은 AI는 다음을 따른다.

1. 이 문서를 현재 개발 로드맵과 진행 상태로 사용한다.
2. 이미 확정된 요구사항을 반복해서 질문하지 않는다.
3. GUI와 계산 엔진을 섞지 않는다.
4. Python과 C++ 양쪽 구현을 항상 고려한다.
5. 사용자가 코드를 명시적으로 요청하기 전에는 코드를 작성하지 않는다.
6. 코드에는 충분한 주석과 구조 설명을 넣는다.
7. 기능 단위로 개발하고 각 단계마다 테스트한다.
8. GitHub 저장소의 실제 코드를 확인한 뒤 다음 작업을 판단한다.
9. 현재 최우선 작업은 Python 기본 계산 엔진이다.
10. 프로젝트 범위를 갑자기 확장하지 않고 현재 Step을 먼저 완료한다.

---

# 10. 한 줄 상태 요약

> Python PySide6 GUI 뼈대는 실행 가능한 상태이며, 다음 작업은 Tokenizer와 재귀 하강 파서를 이용한 Python 기본 계산 엔진 구현 및 GUI 연결이다.
