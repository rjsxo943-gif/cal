"""1변수 통계 계산과 데이터 관리 동작을 검증한다."""

import math

import pytest

from core.calculator_errors import OverflowCalculatorError
from core.calculator_state import CalculatorState, DisplayMode
from core.statistics_calculator import OneVariableStatisticsCalculator
from core.statistics_controller import StatisticsController


def test_summary_for_basic_dataset() -> None:
    summary = OneVariableStatisticsCalculator().summarize([1, 2, 3, 4])

    assert summary.count == 4
    assert summary.total == 10
    assert summary.mean == 2.5
    assert summary.minimum == 1
    assert summary.maximum == 4
    assert summary.population_variance == pytest.approx(1.25)
    assert summary.population_standard_deviation == pytest.approx(
        math.sqrt(1.25)
    )
    assert summary.sample_variance == pytest.approx(5 / 3)
    assert summary.sample_standard_deviation == pytest.approx(
        math.sqrt(5 / 3)
    )


def test_empty_summary() -> None:
    summary = OneVariableStatisticsCalculator().summarize([])

    assert summary.count == 0
    assert summary.total == 0
    assert summary.mean is None
    assert summary.sample_variance is None


def test_single_value_has_population_but_not_sample_variance() -> None:
    summary = OneVariableStatisticsCalculator().summarize([7])

    assert summary.population_variance == 0
    assert summary.population_standard_deviation == 0
    assert summary.sample_variance is None
    assert summary.sample_standard_deviation is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1", (1.0,)),
        ("1, 2, 3", (1.0, 2.0, 3.0)),
        ("1 2;3", (1.0, 2.0, 3.0)),
    ],
)
def test_controller_adds_one_or_multiple_values(
    text: str,
    expected: tuple[float, ...],
) -> None:
    controller = StatisticsController(CalculatorState())

    result = controller.add_values(text)

    assert result.is_success is True
    assert controller.values == expected


@pytest.mark.parametrize(
    "text",
    ["", "abc", "1, inf", "1, nan", "1,,x"],
)
def test_invalid_input_does_not_mutate_existing_data(text: str) -> None:
    controller = StatisticsController(CalculatorState())
    controller.add_values("5")

    result = controller.add_values(text)

    assert result.is_success is False
    assert result.error_message == "Invalid input"
    assert controller.values == (5.0,)


def test_remove_and_clear_data() -> None:
    controller = StatisticsController(CalculatorState())
    controller.add_values("1 2 3")

    removed = controller.remove_value(1)
    cleared = controller.clear()

    assert removed.is_success is True
    assert controller.values == ()
    assert dict(cleared.summary_items)["n"] == "0"


def test_remove_without_selection_returns_error() -> None:
    controller = StatisticsController(CalculatorState())

    result = controller.remove_value(-1)

    assert result.is_success is False
    assert result.error_message == "Select a data row"


def test_fmt_change_redisplays_statistics() -> None:
    state = CalculatorState()
    controller = StatisticsController(state)
    controller.add_values("1,2")

    state.display_mode = DisplayMode.FIX
    result = controller.redisplay()
    items = dict(result.summary_items)

    assert items["Σx"] == "3.0000"
    assert items["x̄"] == "1.5000"


def test_sample_statistics_use_placeholder_for_one_value() -> None:
    controller = StatisticsController(CalculatorState())

    result = controller.add_values("7")
    items = dict(result.summary_items)

    assert items["s²"] == "—"
    assert items["s"] == "—"


def test_extreme_dataset_overflow_is_reported() -> None:
    calculator = OneVariableStatisticsCalculator()

    with pytest.raises(OverflowCalculatorError):
        calculator.summarize([1e308, -1e308, 1e308, -1e308])
