"""DEG, RAD, GRAD 각도 단위를 라디안과 상호 변환한다."""

import math

from core.calculator_state import AngleMode


class AngleConverter:
    """삼각함수의 내부 계산 단위를 라디안으로 통일한다."""

    @staticmethod
    def to_radians(value: float, mode: AngleMode) -> float:
        """현재 각도 모드의 값을 라디안으로 변환한다."""
        if mode is AngleMode.DEG:
            return math.radians(value)

        if mode is AngleMode.GRAD:
            return value * math.pi / 200.0

        return value

    @staticmethod
    def from_radians(value: float, mode: AngleMode) -> float:
        """라디안 값을 현재 각도 모드로 변환한다."""
        if mode is AngleMode.DEG:
            return math.degrees(value)

        if mode is AngleMode.GRAD:
            return value * 200.0 / math.pi

        return value
