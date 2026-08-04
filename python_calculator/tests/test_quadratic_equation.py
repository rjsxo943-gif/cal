"""이차방정식 Solver와 Controller 동작을 검증한다."""

import math

import pytest

from core.calculator_errors import (
    InvalidInputError,
    MathCalculatorError,
    OverflowCalculatorError,
)
from core.calculator_state import CalculatorState, DisplayMode
from core.equation_controller import EquationController
from core.quadratic_equation_solver import (
    QuadraticEquationSolver,
    QuadraticRootType,
)


def test_two_distinct_real_roots() -> None:
    solver = QuadraticEquationSolver()

    solution = solver.solve(1.0, -5.0, 6.0)

    assert solution.root_type is QuadraticRootType.TWO_REAL
    assert solution.discriminant == pytest.approx(1.0)
    assert {solution.root1.real, solution.root2.real} == {2.0, 3.0}


def test_repeated_real_root() -> None:
    solution = QuadraticEquationSolver().solve(1.0, 2.0, 1.0)

    assert solution.root_type is QuadraticRootType.REPEATED_REAL
    assert solution.discriminant == 0.0
    assert solution.root1 == pytest.approx(complex(-1.0, 0.0))
    assert solution.root2 == pytest.approx(complex(-1.0, 0.0))


def test_two_complex_roots() -> None:
    solution = QuadraticEquationSolver().solve(1.0, 0.0, 1.0)

    assert solution.root_type is QuadraticRootType.TWO_COMPLEX
    assert solution.discriminant == pytest.approx(-4.0)
    assert solution.root1 == pytest.approx(complex(0.0, 1.0))
    assert solution.root2 == pytest.approx(complex(0.0, -1.0))


def test_nearly_zero_discriminant_is_treated_as_repeated_root() -> None:
    solver = QuadraticEquationSolver()

    solution = solver.solve(1.0, 2.0, 1.0 + 1e-14)

    assert solution.root_type is QuadraticRootType.REPEATED_REAL


def test_zero_a_is_rejected() -> None:
    solver = QuadraticEquationSolver()

    with pytest.raises(MathCalculatorError, match="Coefficient a"):
        solver.solve(0.0, 2.0, 1.0)


@pytest.mark.parametrize("coefficient", [math.inf, -math.inf, math.nan])
def test_nonfinite_coefficients_are_rejected(coefficient: float) -> None:
    solver = QuadraticEquationSolver()

    with pytest.raises(InvalidInputError):
        solver.solve(coefficient, 1.0, 1.0)


def test_discriminant_overflow_is_reported() -> None:
    solver = QuadraticEquationSolver()

    with pytest.raises(OverflowCalculatorError):
        solver.solve(1.0, 1e308, 1.0)


def test_controller_formats_real_roots() -> None:
    controller = EquationController(CalculatorState())

    result = controller.solve("1", "-5", "6")

    assert result.is_success is True
    assert result.classification == "Two real roots"
    assert result.discriminant_text == "Δ = 1"
    assert result.root_lines == ("x₁ = 3", "x₂ = 2")


def test_controller_formats_complex_roots() -> None:
    controller = EquationController(CalculatorState())

    result = controller.solve("1", "0", "1")

    assert result.is_success is True
    assert result.root_lines == ("x₁ = i", "x₂ = -i")


@pytest.mark.parametrize(
    ("a_text", "b_text", "c_text"),
    [
        ("", "1", "2"),
        ("abc", "1", "2"),
        ("1", "", "2"),
        ("1", "2", "nan"),
    ],
)
def test_controller_rejects_invalid_text(
    a_text: str,
    b_text: str,
    c_text: str,
) -> None:
    controller = EquationController(CalculatorState())

    result = controller.solve(a_text, b_text, c_text)

    assert result.is_success is False
    assert result.error_message == "Invalid input"


def test_controller_redisplays_roots_after_fmt_change() -> None:
    state = CalculatorState()
    controller = EquationController(state)

    controller.solve("1", "-5", "6")
    state.display_mode = DisplayMode.FIX
    result = controller.redisplay_last_solution()

    assert result is not None
    assert result.discriminant_text == "Δ = 1.0000"
    assert result.root_lines == ("x₁ = 3.0000", "x₂ = 2.0000")


def test_redisplay_before_first_solution_returns_none() -> None:
    controller = EquationController(CalculatorState())

    assert controller.redisplay_last_solution() is None
