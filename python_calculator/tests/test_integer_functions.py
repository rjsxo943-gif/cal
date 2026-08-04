"""절댓값, 역수, 팩토리얼, 조합 및 정수 함수를 검증한다."""

import pytest

from core.calculator_engine import CalculatorEngine
from core.calculator_errors import (
    DivisionByZeroCalculatorError,
    MathCalculatorError,
    OverflowCalculatorError,
    SyntaxCalculatorError,
)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("abs(-12.5)", 12.5),
        ("recip(4)", 0.25),
        ("5!", 120.0),
        ("0!", 1.0),
        ("3!!", 720.0),
        ("2^3!", 64.0),
        ("-3!", -6.0),
        ("(3+2)!", 120.0),
        ("npr(5,2)", 20.0),
        ("ncr(5,2)", 10.0),
        ("mod(10,3)", 1.0),
        ("mod(-10,3)", -1.0),
        ("gcd(48,18)", 6.0),
        ("gcd(-48,18)", 6.0),
        ("lcm(12,18)", 36.0),
        ("lcm(0,18)", 0.0),
        ("ncr(5,2)+gcd(12,18)", 16.0),
    ],
)
def test_integer_and_combinatorics_operations(
    expression: str,
    expected: float,
) -> None:
    engine = CalculatorEngine()
    assert engine.evaluate(expression) == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["recip(0)", "mod(10,0)"])
def test_zero_division_operations(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(DivisionByZeroCalculatorError):
        engine.evaluate(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "(-1)!",
        "3.5!",
        "npr(4,5)",
        "ncr(5,-1)",
        "gcd(4.5,2)",
        "lcm(2.5,3)",
    ],
)
def test_integer_function_domain_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(MathCalculatorError):
        engine.evaluate(expression)


def test_factorial_overflow() -> None:
    engine = CalculatorEngine()

    with pytest.raises(OverflowCalculatorError):
        engine.evaluate("171!")


@pytest.mark.parametrize(
    "expression",
    [
        "abs(1,2)",
        "gcd(1)",
        "npr()",
        "mod(1,2,3)",
    ],
)
def test_function_argument_count_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(SyntaxCalculatorError):
        engine.evaluate(expression)
