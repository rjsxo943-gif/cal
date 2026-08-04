"""NORM/FIX/SCI와 S⇔D 결과 표시 동작을 검증한다."""

import math

from core.calculator_controller import CalculatorController
from core.calculator_state import CalculatorState, DisplayMode
from core.result_formatter import ResultFormatter


def test_formatter_supports_norm_fix_and_sci() -> None:
    formatter = ResultFormatter()

    assert formatter.format(1 / 3) == "0.3333333333"
    assert formatter.format(1 / 3, DisplayMode.FIX, 4) == "0.3333"
    assert formatter.format(1234.5, DisplayMode.SCI, 4) == "1.2345E+03"


def test_simple_values_can_be_displayed_as_fractions() -> None:
    formatter = ResultFormatter()

    assert formatter.format(1 / 3, as_fraction=True) == "1/3"
    assert formatter.format(0.5, as_fraction=True) == "1/2"
    assert formatter.format(2.0, as_fraction=True) == "2"


def test_irrational_values_do_not_become_long_approximate_fractions() -> None:
    formatter = ResultFormatter()

    assert formatter.format_fraction(math.pi) is None
    assert formatter.format_fraction(math.sqrt(2)) is None


def test_display_mode_cycles_with_status_labels() -> None:
    state = CalculatorState()

    assert state.display_mode_label == "NORM"
    assert state.cycle_display_mode() is DisplayMode.FIX
    assert state.display_mode_label == "FIX4"
    assert state.cycle_display_mode() is DisplayMode.SCI
    assert state.display_mode_label == "SCI4"
    assert state.cycle_display_mode() is DisplayMode.NORM


def test_controller_redisplays_latest_result_without_recalculating() -> None:
    controller = CalculatorController()

    original = controller.calculate("1/3")
    controller.cycle_display_mode()
    fixed = controller.redisplay_last_result()
    controller.cycle_display_mode()
    scientific = controller.redisplay_last_result()

    assert original.display_text == "0.3333333333"
    assert fixed is not None
    assert fixed.display_text == "0.3333"
    assert scientific is not None
    assert scientific.display_text == "3.3333E-01"
    assert controller.state.answer == original.numeric_value


def test_fraction_toggle_preserves_numeric_answer() -> None:
    controller = CalculatorController()

    original = controller.calculate("1/3")
    fraction = controller.toggle_fraction_display()
    decimal = controller.toggle_fraction_display()

    assert fraction is not None
    assert fraction.display_text == "1/3"
    assert decimal is not None
    assert decimal.display_text == "0.3333333333"
    assert controller.state.answer == original.numeric_value


def test_new_calculation_returns_to_decimal_display() -> None:
    controller = CalculatorController()

    controller.calculate("1/2")
    controller.toggle_fraction_display()
    result = controller.calculate("1/4")

    assert result.display_text == "0.25"
    assert controller.state.fraction_display is False


def test_display_buttons_do_nothing_before_first_result() -> None:
    controller = CalculatorController()

    assert controller.redisplay_last_result() is None
    assert controller.toggle_fraction_display() is None


def test_irrational_result_stays_decimal_when_s_d_is_pressed() -> None:
    controller = CalculatorController()

    controller.calculate("pi")
    result = controller.toggle_fraction_display()

    assert result is not None
    assert result.display_text == "3.141592654"
    assert controller.state.fraction_display is False
