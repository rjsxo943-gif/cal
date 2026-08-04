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

    def set_angle_mode(self, angle_mode: AngleMode) -> None:
        """외부에서 선택한 각도 모드를 현재 상태에 저장한다."""
        self.angle_mode = angle_mode

    def cycle_angle_mode(self) -> AngleMode:
        """DEG → RAD → GRAD 순서로 각도 모드를 순환한다."""
        angle_modes = (
            AngleMode.DEG,
            AngleMode.RAD,
            AngleMode.GRAD,
        )

        current_index = angle_modes.index(self.angle_mode)
        next_index = (current_index + 1) % len(angle_modes)
        self.angle_mode = angle_modes[next_index]

        return self.angle_mode
