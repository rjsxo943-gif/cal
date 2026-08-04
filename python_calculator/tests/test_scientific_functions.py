"""상수, 제곱근, 삼각함수, 로그 함수 동작을 검증한다."""

import math

import pytest

from core.calculator_controller import CalculatorController
from core.calculator_engine import CalculatorEngine
from core.calculator_errors import MathCalculatorError, SyntaxCalculatorError
from core.calculator_state import AngleMode, CalculatorState


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("pi", math.pi),
        ("π", math.pi),
        ("e", math.e),
        ("sqrt(16)", 4.0),
        ("√(81)", 9.0),
        ("sin(30)", 0.5),
        ("cos(60)", 0.5),
        ("tan(45)", 1.0),
        ("asin(0.5)", 30.0),
        ("acos(0.5)", 60.0),
        ("atan(1)", 45.0),
        ("log(1000)", 3.0),
        ("ln(e)", 1.0),
        ("sqrt(16)+sin(30)", 4.5),
        ("2^sqrt(4)", 4.0),
    ],
)
def test_scientific_expressions(expression: str, expected: float) -> None:
    engine = CalculatorEngine()
    assert engine.evaluate(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    "expression",
    [
        "sqrt(-1)",
        "log(0)",
        "ln(-1)",
        "asin(2)",
        "acos(-2)",
        "tan(90)",
    ],
)
def test_function_domain_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(MathCalculatorError):
        engine.evaluate(expression)


@pytest.mark.parametrize("expression", ["sin30", "sqrt()", "log(1"])
def test_function_syntax_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(SyntaxCalculatorError):
        engine.evaluate(expression)


def test_radian_mode() -> None:
    state = CalculatorState(angle_mode=AngleMode.RAD)
    engine = CalculatorEngine(state)

    assert engine.evaluate("sin(pi/2)") == pytest.approx(1.0)
    assert engine.evaluate("asin(1)") == pytest.approx(math.pi / 2)


def test_gradian_mode() -> None:
    state = CalculatorState(angle_mode=AngleMode.GRAD)
    engine = CalculatorEngine(state)

    assert engine.evaluate("sin(100)") == pytest.approx(1.0)
    assert engine.evaluate("asin(1)") == pytest.approx(100.0)


def test_controller_stores_latest_successful_answer() -> None:
    controller = CalculatorController()

    result = controller.calculate("sqrt(81)")

    assert result.is_success is True
    assert controller.state.answer == pytest.approx(9.0)
