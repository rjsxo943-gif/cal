"""기본 계산 엔진의 공통 동작을 검증한다."""

import pytest

from core.calculator_controller import CalculatorController
from core.calculator_engine import CalculatorEngine
from core.calculator_errors import (
    DivisionByZeroCalculatorError,
    InvalidInputError,
    SyntaxCalculatorError,
)
from core.result_formatter import ResultFormatter


@pytest.fixture
def engine() -> CalculatorEngine:
    return CalculatorEngine()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2+3", 5.0),
        ("2+3*4", 14.0),
        ("(2+3)*4", 20.0),
        ("-5+3", -2.0),
        ("3*-2", -6.0),
        ("-2^2", -4.0),
        ("(-2)^2", 4.0),
        ("2^3^2", 512.0),
        ("2^-2", 0.25),
        ("10/4", 2.5),
        (" 12.5 + 3 * (4 - 1) ", 21.5),
        ("1E3", 1000.0),
        ("2.5e-3", 0.0025),
    ],
)
def test_basic_expressions(
    engine: CalculatorEngine,
    expression: str,
    expected: float,
) -> None:
    assert engine.evaluate(expression) == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["(2+3", "1.2.3", "2++*3", ".", "2 3"])
def test_syntax_errors(engine: CalculatorEngine, expression: str) -> None:
    with pytest.raises(SyntaxCalculatorError):
        engine.evaluate(expression)


@pytest.mark.parametrize("expression", ["2+a", "unknown(3)", ""])
def test_invalid_inputs(engine: CalculatorEngine, expression: str) -> None:
    with pytest.raises(InvalidInputError):
        engine.evaluate(expression)


def test_division_by_zero(engine: CalculatorEngine) -> None:
    with pytest.raises(DivisionByZeroCalculatorError):
        engine.evaluate("5/0")


def test_formatter_removes_unnecessary_decimal_part() -> None:
    formatter = ResultFormatter()
    assert formatter.format(14.0) == "14"
    assert formatter.format(2.5) == "2.5"
    assert formatter.format(1 / 3) == "0.3333333333"


@pytest.mark.parametrize(
    ("expression", "expected_text", "is_success"),
    [
        ("2+3*4", "14", True),
        ("5/0", "Division by zero", False),
        ("(2+3", "Syntax ERROR", False),
        ("2+a", "Invalid input", False),
    ],
)
def test_controller_returns_gui_ready_result(
    expression: str,
    expected_text: str,
    is_success: bool,
) -> None:
    controller = CalculatorController()
    result = controller.calculate(expression)

    assert result.display_text == expected_text
    assert result.is_success is is_success
