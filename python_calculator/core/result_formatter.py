"""계산 결과를 Python과 C++에서 맞추기 위한 출력 형식 담당."""

import math

from core.calculator_errors import OverflowCalculatorError


class ResultFormatter:
    """Phase 2의 NORM 방식으로 실수 결과를 문자열로 변환한다."""

    SIGNIFICANT_DIGITS = 10

    def format(self, value: float) -> str:
        """최대 10개의 유효 숫자를 사용해 결과를 표시한다."""
        if not math.isfinite(value):
            raise OverflowCalculatorError()

        # 부동소수점 계산에서 생길 수 있는 -0 표시를 제거한다.
        if abs(value) < 1e-15:
            value = 0.0

        return format(value, f".{self.SIGNIFICANT_DIGITS}g")
