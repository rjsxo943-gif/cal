"""복소수 직교형·극형 변환과 표시 동작을 검증한다."""

import math

import pytest

from core.calculator_state import AngleMode, CalculatorState, DisplayMode
from core.complex_calculator import ComplexCalculator
from core.complex_controller import ComplexController


def test_rectangular_summary() -> None:
    summary = ComplexCalculator().from_rectangular(3.0, 4.0)

    assert summary.magnitude == pytest.approx(5.0)
    assert summary.phase_radians == pytest.approx(math.atan2(4.0, 3.0))
    assert summary.conjugate == complex(3.0, -4.0)


def test_polar_degree_conversion() -> None:
    summary = ComplexCalculator().from_polar(
        5.0,
        53.13010235415598,
        AngleMode.DEG,
    )

    assert summary.value.real == pytest.approx(3.0)
    assert summary.value.imag == pytest.approx(4.0)


def test_polar_radian_and_gradian_conversion() -> None:
    calculator = ComplexCalculator()

    radian = calculator.from_polar(1.0, math.pi / 2.0, AngleMode.RAD)
    gradian = calculator.from_polar(1.0, 100.0, AngleMode.GRAD)

    assert radian.value == pytest.approx(complex(0.0, 1.0))
    assert gradian.value == pytest.approx(complex(0.0, 1.0))


def test_controller_formats_engineering_j_notation() -> None:
    controller = ComplexController(CalculatorState())

    result = controller.from_rectangular("3", "4")

    assert result.is_success is True
    assert result.rectangular_text == "3 + 4j"
    assert result.conjugate_text == "3 - 4j"
    assert result.magnitude_text == "5"
    assert result.phase_text == "53.13010235°"
    assert result.polar_text == "5 ∠ 53.13010235°"


def test_pure_imaginary_unit_is_shortened() -> None:
    controller = ComplexController(CalculatorState())

    positive = controller.from_rectangular("0", "1")
    negative = controller.from_rectangular("0", "-1")

    assert positive.rectangular_text == "j"
    assert negative.rectangular_text == "-j"


def test_negative_polar_magnitude_is_rejected() -> None:
    controller = ComplexController(CalculatorState())

    result = controller.from_polar("-1", "30")

    assert result.is_success is False
    assert result.error_message == "Magnitude must not be negative"


@pytest.mark.parametrize(
    ("first", "second", "use_polar"),
    [
        ("", "2", False),
        ("abc", "2", False),
        ("nan", "30", True),
        ("1", "inf", True),
    ],
)
def test_invalid_complex_input(
    first: str,
    second: str,
    use_polar: bool,
) -> None:
    controller = ComplexController(CalculatorState())

    if use_polar:
        result = controller.from_polar(first, second)
    else:
        result = controller.from_rectangular(first, second)

    assert result.is_success is False
    assert result.error_message == "Invalid input"


def test_angle_mode_change_redisplays_phase() -> None:
    state = CalculatorState()
    controller = ComplexController(state)
    controller.from_rectangular("0", "1")

    state.angle_mode = AngleMode.RAD
    radian_result = controller.redisplay_last_result()
    state.angle_mode = AngleMode.GRAD
    gradian_result = controller.redisplay_last_result()

    assert radian_result is not None
    assert radian_result.phase_text == "1.570796327 rad"
    assert gradian_result is not None
    assert gradian_result.phase_text == "100 grad"


def test_fmt_change_redisplays_complex_values() -> None:
    state = CalculatorState()
    controller = ComplexController(state)
    controller.from_rectangular("3", "4")

    state.display_mode = DisplayMode.FIX
    result = controller.redisplay_last_result()

    assert result is not None
    assert result.rectangular_text == "3.0000 + 4.0000j"
    assert result.magnitude_text == "5.0000"


def test_zero_complex_number_has_zero_phase() -> None:
    controller = ComplexController(CalculatorState())

    result = controller.from_rectangular("0", "0")

    assert result.rectangular_text == "0"
    assert result.phase_text == "0°"


def test_redisplay_before_first_conversion_returns_none() -> None:
    controller = ComplexController(CalculatorState())

    assert controller.redisplay_last_result() is None
