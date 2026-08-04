"""계산 모드와 이후 계산에 필요한 공통 상태를 보관한다."""

from dataclasses import dataclass
from enum import Enum


class AngleMode(str, Enum):
    """삼각함수에서 사용할 각도 단위."""

    DEG = "DEG"
    RAD = "RAD"
    GRAD = "GRAD"


@dataclass
class CalculatorState:
    """GUI와 계산 엔진이 공유하는 계산기 상태."""

    angle_mode: AngleMode = AngleMode.DEG
    answer: float = 0.0
