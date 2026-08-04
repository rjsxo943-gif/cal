"""GUI 요청과 계산 엔진 사이를 연결하는 얇은 제어 계층."""

from dataclasses import dataclass

from core.calculator_engine import CalculatorEngine
from core.calculator_errors import CalculatorError
from core.calculator_state import AngleMode, CalculatorState
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
            display_text = self._formatter.format(numeric_value)
        except CalculatorError as error:
            return CalculationResult(
                display_text=str(error),
                is_success=False,
            )

        # 오류가 아닌 가장 최근 성공 결과만 Ans로 저장한다.
        self.state.answer = numeric_value

        return CalculationResult(
            display_text=display_text,
            is_success=True,
            numeric_value=numeric_value,
        )

    def set_angle_mode(self, angle_mode: AngleMode) -> None:
        """GUI에서 직접 선택한 각도 모드를 상태에 반영한다."""
        self.state.set_angle_mode(angle_mode)

    def cycle_angle_mode(self) -> AngleMode:
        """다음 각도 모드로 전환하고 변경된 모드를 반환한다."""
        return self.state.cycle_angle_mode()
