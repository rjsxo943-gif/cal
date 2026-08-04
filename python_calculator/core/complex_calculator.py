"""복소수의 직교형·극형 변환과 공통 성질을 계산한다."""

from dataclasses import dataclass
import math

from core.angle_converter import AngleConverter
from core.calculator_errors import (
    InvalidInputError,
    MathCalculatorError,
    OverflowCalculatorError,
)
from core.calculator_state import AngleMode


@dataclass(frozen=True)
class ComplexSummary:
    """복소수 하나에서 파생되는 공통 결과."""

    value: complex
    conjugate: complex
    magnitude: float
    phase_radians: float


class ComplexCalculator:
    """직교형과 극형 입력을 동일한 ComplexSummary로 변환한다."""

    def from_rectangular(self, real: float, imaginary: float) -> ComplexSummary:
        """실수부와 허수부로 복소수를 만든다."""
        self._ensure_finite(real, imaginary)
        return self._summarize(complex(real, imaginary))

    def from_polar(
        self,
        magnitude: float,
        phase: float,
        angle_mode: AngleMode,
    ) -> ComplexSummary:
        """크기와 현재 각도 단위의 위상각으로 복소수를 만든다."""
        self._ensure_finite(magnitude, phase)

        if magnitude < 0.0:
            raise MathCalculatorError("Magnitude must not be negative")

        radians = AngleConverter.to_radians(phase, angle_mode)
        value = complex(
            magnitude * math.cos(radians),
            magnitude * math.sin(radians),
        )
        return self._summarize(value)

    def _summarize(self, value: complex) -> ComplexSummary:
        """직교형 값에서 크기, 위상각, 켤레복소수를 계산한다."""
        self._ensure_finite(value.real, value.imag)

        magnitude = abs(value)
        phase_radians = 0.0 if magnitude == 0.0 else math.atan2(
            value.imag,
            value.real,
        )

        if not math.isfinite(magnitude) or not math.isfinite(phase_radians):
            raise OverflowCalculatorError()

        return ComplexSummary(
            value=value,
            conjugate=value.conjugate(),
            magnitude=magnitude,
            phase_radians=phase_radians,
        )

    @staticmethod
    def _ensure_finite(*values: float) -> None:
        """NaN과 무한대 입력을 거부한다."""
        if any(not math.isfinite(value) for value in values):
            raise InvalidInputError()
