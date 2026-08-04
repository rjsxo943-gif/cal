"""계산 결과를 Python과 C++에서 맞추기 위한 출력 형식 담당."""

import math
from fractions import Fraction

from core.calculator_errors import OverflowCalculatorError
from core.calculator_state import DisplayMode


class ResultFormatter:
    """NORM, FIX, SCI와 간단한 분수 표시를 담당한다."""

    SIGNIFICANT_DIGITS = 10
    MAX_FRACTION_DENOMINATOR = 10_000
    FRACTION_TOLERANCE = 1e-12

    def format(
        self,
        value: float,
        display_mode: DisplayMode = DisplayMode.NORM,
        display_digits: int = 4,
        as_fraction: bool = False,
    ) -> str:
        """현재 표시 상태에 따라 숫자를 문자열로 변환한다."""
        value = self._normalize_value(value)

        if as_fraction:
            fraction_text = self.format_fraction(value)
            if fraction_text is not None:
                return fraction_text

        if display_mode is DisplayMode.FIX:
            return format(value, f".{display_digits}f")

        if display_mode is DisplayMode.SCI:
            return format(value, f".{display_digits}E")

        return format(value, f".{self.SIGNIFICANT_DIGITS}g")

    def format_fraction(self, value: float) -> str | None:
        """값을 단순한 분수로 표현할 수 있으면 문자열로 반환한다."""
        value = self._normalize_value(value)
        fraction = Fraction(value).limit_denominator(
            self.MAX_FRACTION_DENOMINATOR
        )

        error = abs(float(fraction) - value)
        allowed_error = max(
            self.FRACTION_TOLERANCE,
            abs(value) * self.FRACTION_TOLERANCE,
        )

        if error > allowed_error:
            return None

        if fraction.denominator == 1:
            return str(fraction.numerator)

        return f"{fraction.numerator}/{fraction.denominator}"

    def can_format_as_fraction(self, value: float) -> bool:
        """S⇔D 전환에 사용할 단순 분수 표현이 있는지 확인한다."""
        return self.format_fraction(value) is not None

    @staticmethod
    def _normalize_value(value: float) -> float:
        """유한성 검사와 -0 제거를 한곳에서 처리한다."""
        if not math.isfinite(value):
            raise OverflowCalculatorError()

        if abs(value) < 1e-15:
            return 0.0

        return value
