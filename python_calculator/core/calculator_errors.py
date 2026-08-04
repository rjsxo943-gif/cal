"""계산 엔진 전체에서 공통으로 사용하는 오류 형식."""


class CalculatorError(Exception):
    """사용자 화면에 표시할 수 있는 계산기 오류의 부모 클래스."""

    default_message = "Invalid input"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class SyntaxCalculatorError(CalculatorError):
    """수식의 구조가 올바르지 않을 때 발생한다."""

    default_message = "Syntax ERROR"


class InvalidInputError(CalculatorError):
    """지원하지 않는 문자나 비어 있는 입력에 사용한다."""

    default_message = "Invalid input"


class DivisionByZeroCalculatorError(CalculatorError):
    """0으로 나누거나 0의 음수 거듭제곱을 계산할 때 발생한다."""

    default_message = "Division by zero"


class MathCalculatorError(CalculatorError):
    """일반 계산 모드에서 실수 결과를 만들 수 없을 때 발생한다."""

    default_message = "Math ERROR"


class OverflowCalculatorError(CalculatorError):
    """계산 결과가 부동소수점 범위를 벗어날 때 발생한다."""

    default_message = "Overflow"
