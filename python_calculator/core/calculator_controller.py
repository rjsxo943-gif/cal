"""GUI 요청과 계산 엔진 사이를 연결하는 얇은 제어 계층."""

from dataclasses import dataclass

from core.calculator_engine import CalculatorEngine
from core.calculator_errors import CalculatorError
from core.calculator_state import (
    AngleMode,
    CalculatorState,
    DisplayMode,
)
from core.result_formatter import ResultFormatter


@dataclass(frozen=True)
class CalculationResult:
    """GUI가 결과 표시와 기록 추가 여부를 판단할 수 있는 반환값."""

    display_text: str
    is_success: bool
    numeric_value: float | None = None


class CalculatorController:
    """계산 실행, 상태 갱신, 결과 포맷, 오류 변환을 조정한다."""

    def __init__(
        self,
        state: CalculatorState | None = None,
        engine: CalculatorEngine | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        self.state = state or CalculatorState()
        self._engine = engine or CalculatorEngine(self.state)
        self._formatter = formatter or ResultFormatter()

    def calculate(self, expression: str) -> CalculationResult:
        """수식을 계산하고 GUI에서 바로 사용할 결과 객체를 반환한다."""
        try:
            numeric_value = self._engine.evaluate(expression)

            # 새 계산은 현재 표시 모드의 소수 표현부터 시작한다.
            self.state.fraction_display = False
            display_text = self._format_value(numeric_value)
        except CalculatorError as error:
            return CalculationResult(
                display_text=str(error),
                is_success=False,
            )

        self.state.answer = numeric_value
        self.state.last_result = numeric_value

        return CalculationResult(
            display_text=display_text,
            is_success=True,
            numeric_value=numeric_value,
        )

    def redisplay_last_result(self) -> CalculationResult | None:
        """표시 모드 변경 뒤 최근 결과를 새 형식으로 다시 표시한다."""
        if self.state.last_result is None:
            return None

        numeric_value = self.state.last_result
        return CalculationResult(
            display_text=self._format_value(numeric_value),
            is_success=True,
            numeric_value=numeric_value,
        )

    def toggle_fraction_display(self) -> CalculationResult | None:
        """최근 결과를 소수 표시와 단순 분수 표시 사이에서 전환한다."""
        if self.state.last_result is None:
            return None

        numeric_value = self.state.last_result

        if self.state.fraction_display:
            self.state.fraction_display = False
        elif self._formatter.can_format_as_fraction(numeric_value):
            self.state.fraction_display = True

        return self.redisplay_last_result()

    def set_angle_mode(self, angle_mode: AngleMode) -> None:
        """GUI에서 직접 선택한 각도 모드를 상태에 반영한다."""
        self.state.set_angle_mode(angle_mode)

    def cycle_angle_mode(self) -> AngleMode:
        """다음 각도 모드로 전환하고 변경된 모드를 반환한다."""
        return self.state.cycle_angle_mode()

    def set_display_mode(self, display_mode: DisplayMode) -> None:
        """GUI에서 직접 선택한 결과 표시 모드를 상태에 반영한다."""
        self.state.set_display_mode(display_mode)

    def cycle_display_mode(self) -> DisplayMode:
        """다음 결과 표시 모드로 전환하고 변경된 모드를 반환한다."""
        return self.state.cycle_display_mode()

    def _format_value(self, value: float) -> str:
        """현재 CalculatorState를 ResultFormatter 인자로 변환한다."""
        return self._formatter.format(
            value,
            display_mode=self.state.display_mode,
            display_digits=self.state.display_digits,
            as_fraction=self.state.fraction_display,
        )
