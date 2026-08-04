# Scientific Calculator Dual Implementation

Python과 C++로 기능과 출력 결과가 최대한 동일한 공학용 계산기를 구현하는 프로젝트입니다.

## Project Goal

Casio fx-991ES PLUS 수준의 기능을 가진 GUI 공학용 계산기를 두 언어로 병렬 구현합니다.

두 버전은 내부 구현 언어만 다르고 다음 요소는 최대한 동일하게 맞춥니다.

- GUI 구조
- 버튼 배치
- 수식 입력 방식
- 계산 기능
- 계산 결과
- 표시 형식
- 오류 메시지
- 키보드 조작

## Python Version

- Language: Python
- GUI: PySide6
- IDE: VS Code

## C++ Version

- Language: C++
- GUI: Qt Widgets
- IDE: Visual Studio

## Project Structure

- `python_calculator/`: Python 및 PySide6 버전
- `cpp_calculator/`: C++ 및 Qt Widgets 버전
- `shared_tests/`: Python과 C++ 공통 비교 테스트
- `docs/`: 설계 문서와 프로젝트 요구사항

## Architecture

GUI  
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

GUI와 계산 엔진을 분리하고, 두 언어 버전을 기능 단위로 병렬 개발합니다.

## Development Method

한 언어의 프로그램을 모두 완성한 뒤 다른 언어로 번역하지 않습니다.

기능 단위로 다음 순서를 반복합니다.

1. Python 버전 구현
2. C++ 버전 구현
3. 동일한 입력으로 결과 비교
4. 출력 형식과 오류 메시지 확인

## Initial Features

- 기본 사칙연산
- 괄호와 연산자 우선순위
- 삼각함수와 로그
- DEG, RAD, GRAD
- Ans
- 분수 및 소수 표시
- 계산 기록
- 통계 모드
- 이차방정식 모드
- 복소수 모드

## Current Status

- Python 가상환경 생성 완료
- PySide6 설치 완료
- pytest 설치 완료
- Python 프로젝트 폴더 구조 생성 완료
- Phase 1 GUI 구조 설계 진행 중
