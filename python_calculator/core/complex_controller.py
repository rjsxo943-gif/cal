"""ComplexPage와 복소수 계산 로직 사이를 연결한다."""

from dataclasses import dataclass
import math

from core.angle_converter import AngleConverter
from core.calculator_errors import CalculatorError, InvalidInputError
from core.calculator_state import AngleMode, CalculatorState
from core.complex_calculator import ComplexCalculator, ComplexSummary
from core.result_formatter import ResultFormatter


@dataclass(frozen=True)
class ComplexDisplayResult:
    """ComplexPage가 바로 표시할 수 있는 결과."""

    is_success: bool
    rectangular_text: str = ""
    polar_text: str = ""
    magnitude_text: str = ""
    phase_text: str = ""
    conjugate_text: str = ""
    error_message: str = ""


class ComplexController:
    """복소수 입력 해석, 변환, 상태 기반 포맷을 담당한다."""

    def __init__(
        self,
        state: CalculatorState,
        calculator: ComplexCalculator | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        self.state = state
        self._calculator = calculator or ComplexCalculator()
        self._formatter = formatter or ResultFormatter()
        self._last_summary: ComplexSummary | None = None

    def from_rectangular(
        self,
        real_text: str,
        imaginary_text: str,
    ) -> ComplexDisplayResult:
        """실수부·허수부 입력을 직교형과 극형 결과로 변환한다."""
        try:
            summary = self._calculator.from_rectangular(
                self._parse_real(real_text),
                self._parse_real(imaginary_text),
            )
        except (ValueError, CalculatorError) as error:
            return self._error(error)

        self._last_summary = summary
        return self._format_summary(summary)

    def from_polar(
        self,
        magnitude_text: str,
        phase_text: str,
    ) -> ComplexDisplayResult:
        """크기·위상각 입력을 직교형과 극형 결과로 변환한다."""
        try:
            summary = self._calculator.from_polar(
                self._parse_real(magnitude_text),
                self._parse_real(phase_text),
                self.state.angle_mode,
            )
        except (ValueError, CalculatorError) as error:
            return self._error(error)

        self._last_summary = summary
        return self._format_summary(summary)

    def redisplay_last_result(self) -> ComplexDisplayResult | None:
        """DRG 또는 FMT 변경 뒤 최근 복소수 결과를 다시 표시한다."""
        if self._last_summary is None:
            return None
        return self._format_summary(self._last_summary)

    @staticmethod
    def _parse_real(text: str) -> float:
        """비어 있지 않은 유한 실수를 읽는다."""
        stripped = text.strip()
        if not stripped:
            raise InvalidInputError()

        value = float(stripped)
        if not math.isfinite(value):
            raise InvalidInputError()
        return value

    def _format_summary(self, summary: ComplexSummary) -> ComplexDisplayResult:
        """현재 각도·표시 모드를 적용해 복소수 결과를 문자열로 만든다."""
        phase = AngleConverter.from_radians(
            summary.phase_radians,
            self.state.angle_mode,
        )
        magnitude_text = self._format_real(summary.magnitude)
        phase_value_text = self._format_real(phase)
        phase_suffix = self._phase_suffix(self.state.angle_mode)

        return ComplexDisplayResult(
            is_success=True,
            rectangular_text=self._format_complex(summary.value),
            polar_text=f"{magnitude_text} ∠ {phase_value_text}{phase_suffix}",
            magnitude_text=magnitude_text,
            phase_text=f"{phase_value_text}{phase_suffix}",
            conjugate_text=self._format_complex(summary.conjugate),
        )

    def _format_complex(self, value: complex) -> str:
        """복소수를 전자공학에서 주로 쓰는 a ± bj 형식으로 표시한다."""
        real = 0.0 if abs(value.real) < 1e-12 else value.real
        imaginary = 0.0 if abs(value.imag) < 1e-12 else value.imag

        if imaginary == 0.0:
            return self._format_real(real)

        imaginary_text = self._format_imaginary_coefficient(abs(imaginary))

        if real == 0.0:
            return imaginary_text if imaginary > 0.0 else f"-{imaginary_text}"

        sign = "+" if imaginary > 0.0 else "-"
        return f"{self._format_real(real)} {sign} {imaginary_text}"

    def _format_imaginary_coefficient(self, magnitude: float) -> str:
        """허수부 계수가 1이면 1j 대신 j로 표시한다."""
        if abs(magnitude - 1.0) < 1e-12:
            return "j"
        return f"{self._format_real(magnitude)}j"

    def _format_real(self, value: float) -> str:
        return self._formatter.format(
            value,
            display_mode=self.state.display_mode,
            display_digits=self.state.display_digits,
        )

    @staticmethod
    def _phase_suffix(angle_mode: AngleMode) -> str:
        if angle_mode is AngleMode.DEG:
            return "°"
        if angle_mode is AngleMode.GRAD:
            return " grad"
        return " rad"

    @staticmethod
    def _error(error: Exception) -> ComplexDisplayResult:
        return ComplexDisplayResult(
            is_success=False,
            error_message=str(error) or "Invalid input",
        )
