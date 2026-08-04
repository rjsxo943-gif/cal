"""GUI 요청과 계산 엔진 사이를 연결하는 얇은 제어 계층."""

from dataclasses import dataclass

from core.calculator_engine import CalculatorEngine
from core.calculator_errors import CalculatorError
from core.result_formatter import ResultFormatter


@dataclass(frozen=True)
class CalculationResult:
    """GUI가 결과 표시와 기록 추가 여부를 판단할 수 있는 반환값."""

    display_text: str
    is_success: bool
    numeric_value: float | None = None


class CalculatorController:
    """계산 실행, 결과 포맷, 오류 문구 변환을 한곳에서 조정한다."""

    def __init__(
        self,
        engine: CalculatorEngine | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        # 외부 객체를 받을 수 있게 해두면 테스트에서 대체 객체를 넣기 쉽다.
        self._engine = engine or CalculatorEngine()
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

        return CalculationResult(
            display_text=display_text,
            is_success=True,
            numeric_value=numeric_value,
        )
