"""Ans와 DEG/RAD/GRAD 상태 동작을 검증한다."""

import pytest

from core.calculator_controller import CalculatorController
from core.calculator_state import AngleMode


def test_ans_uses_latest_successful_result() -> None:
    controller = CalculatorController()

    first_result = controller.calculate("2+3")
    second_result = controller.calculate("Ans*4")
    third_result = controller.calculate("ans+1")

    assert first_result.display_text == "5"
    assert second_result.display_text == "20"
    assert third_result.display_text == "21"


def test_error_does_not_overwrite_previous_answer() -> None:
    controller = CalculatorController()

    controller.calculate("10")
    error_result = controller.calculate("5/0")
    answer_result = controller.calculate("Ans+2")

    assert error_result.is_success is False
    assert answer_result.display_text == "12"


def test_initial_answer_is_zero() -> None:
    controller = CalculatorController()

    result = controller.calculate("Ans+5")

    assert result.display_text == "5"


def test_angle_mode_cycles_in_fixed_order() -> None:
    controller = CalculatorController()

    assert controller.state.angle_mode is AngleMode.DEG
    assert controller.cycle_angle_mode() is AngleMode.RAD
    assert controller.cycle_angle_mode() is AngleMode.GRAD
    assert controller.cycle_angle_mode() is AngleMode.DEG


def test_degree_mode_calculation() -> None:
    controller = CalculatorController()

    result = controller.calculate("sin(30)")

    assert result.numeric_value == pytest.approx(0.5)


def test_radian_mode_calculation() -> None:
    controller = CalculatorController()
    controller.set_angle_mode(AngleMode.RAD)

    result = controller.calculate("sin(pi/2)")
    inverse_result = controller.calculate("asin(1)")

    assert result.numeric_value == pytest.approx(1.0)
    assert inverse_result.numeric_value == pytest.approx(1.5707963267948966)


def test_gradian_mode_calculation() -> None:
    controller = CalculatorController()
    controller.set_angle_mode(AngleMode.GRAD)

    result = controller.calculate("sin(100)")
    inverse_result = controller.calculate("asin(1)")

    assert result.numeric_value == pytest.approx(1.0)
    assert inverse_result.numeric_value == pytest.approx(100.0)
