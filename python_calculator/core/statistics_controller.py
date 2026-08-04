"""1변수 통계 데이터와 표시 형식을 관리한다."""

from dataclasses import dataclass
import math
import re

from core.calculator_errors import CalculatorError, InvalidInputError
from core.calculator_state import CalculatorState
from core.result_formatter import ResultFormatter
from core.statistics_calculator import (
    OneVariableStatisticsCalculator,
    StatisticsSummary,
)


@dataclass(frozen=True)
class StatisticsDisplayResult:
    """StatisticsPage가 바로 표시할 수 있는 데이터와 요약 결과."""

    is_success: bool
    data_rows: tuple[str, ...] = ()
    summary_items: tuple[tuple[str, str], ...] = ()
    error_message: str = ""


class StatisticsController:
    """데이터 추가·삭제와 통계 계산, 결과 포맷을 조정한다."""

    _VALUE_SEPARATOR = re.compile(r"[,;\s]+")

    def __init__(
        self,
        state: CalculatorState,
        calculator: OneVariableStatisticsCalculator | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        self.state = state
        self._calculator = calculator or OneVariableStatisticsCalculator()
        self._formatter = formatter or ResultFormatter()
        self._values: list[float] = []

    @property
    def values(self) -> tuple[float, ...]:
        """현재 저장된 통계 데이터를 읽기 전용 튜플로 반환한다."""
        return tuple(self._values)

    def add_values(self, text: str) -> StatisticsDisplayResult:
        """쉼표·세미콜론·공백으로 구분된 실수들을 데이터에 추가한다."""
        try:
            parsed_values = self._parse_values(text)
            self._values.extend(parsed_values)
            return self._build_display()
        except CalculatorError as error:
            return StatisticsDisplayResult(
                is_success=False,
                error_message=str(error),
            )

    def remove_value(self, index: int) -> StatisticsDisplayResult:
        """목록의 선택된 위치에 있는 값을 삭제한다."""
        if index < 0 or index >= len(self._values):
            return StatisticsDisplayResult(
                is_success=False,
                error_message="Select a data row",
            )

        self._values.pop(index)
        return self._build_display()

    def clear(self) -> StatisticsDisplayResult:
        """모든 데이터를 제거하고 빈 통계 화면 결과를 반환한다."""
        self._values.clear()
        return self._build_display()

    def redisplay(self) -> StatisticsDisplayResult:
        """FMT 변경 뒤 저장된 데이터를 현재 표시 형식으로 다시 만든다."""
        try:
            return self._build_display()
        except CalculatorError as error:
            return StatisticsDisplayResult(
                is_success=False,
                error_message=str(error),
            )

    @classmethod
    def _parse_values(cls, text: str) -> list[float]:
        """입력 문자열 전체가 유효할 때만 실수 목록으로 변환한다."""
        stripped = text.strip()
        if not stripped:
            raise InvalidInputError()

        pieces = [piece for piece in cls._VALUE_SEPARATOR.split(stripped) if piece]
        if not pieces:
            raise InvalidInputError()

        try:
            values = [float(piece) for piece in pieces]
        except ValueError as error:
            raise InvalidInputError() from error

        if any(not math.isfinite(value) for value in values):
            raise InvalidInputError()

        return values

    def _build_display(self) -> StatisticsDisplayResult:
        """현재 데이터를 계산하고 GUI용 문자열로 포맷한다."""
        summary = self._calculator.summarize(self._values)
        data_rows = tuple(
            f"{index}. {self._format(value)}"
            for index, value in enumerate(self._values, start=1)
        )

        return StatisticsDisplayResult(
            is_success=True,
            data_rows=data_rows,
            summary_items=self._summary_items(summary),
        )

    def _summary_items(
        self,
        summary: StatisticsSummary,
    ) -> tuple[tuple[str, str], ...]:
        """통계 기호와 현재 표시 모드로 변환한 값을 묶는다."""
        return (
            ("n", str(summary.count)),
            ("Σx", self._format(summary.total)),
            ("x̄", self._format_optional(summary.mean)),
            ("min", self._format_optional(summary.minimum)),
            ("max", self._format_optional(summary.maximum)),
            ("σ²", self._format_optional(summary.population_variance)),
            (
                "σ",
                self._format_optional(summary.population_standard_deviation),
            ),
            ("s²", self._format_optional(summary.sample_variance)),
            ("s", self._format_optional(summary.sample_standard_deviation)),
        )

    def _format_optional(self, value: float | None) -> str:
        """계산할 수 없는 항목은 em dash로 표시한다."""
        return "—" if value is None else self._format(value)

    def _format(self, value: float) -> str:
        """공유 CalculatorState의 NORM/FIX/SCI 설정을 적용한다."""
        return self._formatter.format(
            value,
            display_mode=self.state.display_mode,
            display_digits=self.state.display_digits,
        )
