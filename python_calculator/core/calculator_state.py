"""계산 모드와 이후 계산에 필요한 공통 상태를 보관한다."""

from dataclasses import dataclass
from enum import Enum


class AngleMode(str, Enum):
    """삼각함수에서 사용할 각도 단위."""

    DEG = "DEG"
    RAD = "RAD"
    GRAD = "GRAD"


class DisplayMode(str, Enum):
    """계산 결과를 화면에 표시하는 형식."""

    NORM = "NORM"
    FIX = "FIX"
    SCI = "SCI"


@dataclass
class CalculatorState:
    """GUI와 계산 엔진이 공유하는 계산기 상태."""

    angle_mode: AngleMode = AngleMode.DEG
    display_mode: DisplayMode = DisplayMode.NORM
    display_digits: int = 4
    answer: float = 0.0
    last_result: float | None = None
    fraction_display: bool = False

    @property
    def display_mode_label(self) -> str:
        """상단 상태 영역에 보여줄 표시 모드 이름을 만든다."""
        if self.display_mode is DisplayMode.NORM:
            return self.display_mode.value

        return f"{self.display_mode.value}{self.display_digits}"

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

    def set_display_mode(self, display_mode: DisplayMode) -> None:
        """결과 표시 모드를 저장하고 분수 표시를 해제한다."""
        self.display_mode = display_mode
        self.fraction_display = False

    def cycle_display_mode(self) -> DisplayMode:
        """NORM → FIX → SCI 순서로 결과 표시 모드를 순환한다."""
        display_modes = (
            DisplayMode.NORM,
            DisplayMode.FIX,
            DisplayMode.SCI,
        )

        current_index = display_modes.index(self.display_mode)
        next_index = (current_index + 1) % len(display_modes)
        self.display_mode = display_modes[next_index]
        self.fraction_display = False

        return self.display_mode
