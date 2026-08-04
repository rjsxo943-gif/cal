"""정수 몫, 나머지, 백분율, 난수, n제곱근을 검증한다."""

import random

import pytest

from core.calculator_engine import CalculatorEngine
from core.calculator_errors import (
    DivisionByZeroCalculatorError,
    MathCalculatorError,
    SyntaxCalculatorError,
)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("quot(10,3)", 3.0),
        ("quot(-10,3)", -3.0),
        ("quot(10,-3)", -3.0),
        ("rem(10,3)", 1.0),
        ("rem(-10,3)", -1.0),
        ("rem(10,-3)", 1.0),
        ("50%", 0.5),
        ("200*10%", 20.0),
        ("25%%", 0.0025),
        ("root(2,9)", 3.0),
        ("root(3,-8)", -2.0),
        ("root(4,16)", 2.0),
        ("root(1,-5)", -5.0),
        ("root(3,27)+50%", 3.5),
    ],
)
def test_quotient_percent_and_root(
    expression: str,
    expected: float,
) -> None:
    engine = CalculatorEngine()
    assert engine.evaluate(expression) == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["quot(1,0)", "rem(1,0)"])
def test_quotient_and_remainder_zero_division(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(DivisionByZeroCalculatorError):
        engine.evaluate(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "root(2,-4)",
        "root(0,4)",
        "root(2.5,4)",
        "randint(5,1)",
        "randint(1.5,2)",
    ],
)
def test_root_and_random_domain_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(MathCalculatorError):
        engine.evaluate(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "random(1)",
        "quot(1)",
        "root(2,3,4)",
        "randint()",
    ],
)
def test_new_function_argument_count_errors(expression: str) -> None:
    engine = CalculatorEngine()

    with pytest.raises(SyntaxCalculatorError):
        engine.evaluate(expression)


def test_random_result_is_between_zero_and_one() -> None:
    engine = CalculatorEngine()

    result = engine.evaluate("random()")

    assert 0.0 <= result < 1.0


def test_seeded_random_sequence_is_reproducible() -> None:
    actual_generator = random.Random(1234)
    expected_generator = random.Random(1234)
    engine = CalculatorEngine(random_generator=actual_generator)

    random_result = engine.evaluate("random()")
    integer_result = engine.evaluate("randint(1,10)")

    assert random_result == pytest.approx(expected_generator.random())
    assert integer_result == expected_generator.randint(1, 10)
