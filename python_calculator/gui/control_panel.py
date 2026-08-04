"""SHIFT, MODE, 표시 모드, 방향키, DEL, AC 등 공통 제어 버튼 영역."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget


class ControlPanel(QWidget):
    """모든 계산 모드에서 공통으로 사용하는 조작 버튼을 제공한다."""

    shift_requested = Signal()
    mode_requested = Signal()
    angle_mode_requested = Signal()
    display_mode_requested = Signal()
    fraction_toggle_requested = Signal()
    cursor_left_requested = Signal()
    cursor_right_requested = Signal()
    history_up_requested = Signal()
    history_down_requested = Signal()
    delete_requested = Signal()
    clear_requested = Signal()
    history_toggle_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        """공통 제어 버튼을 2행 7열 그리드로 배치한다."""
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.shift_button = self._add_button(layout, "SHIFT", 0, 0)
        self.shift_button.setObjectName("shiftButton")
        self.shift_button.setProperty("active", False)

        self.mode_button = self._add_button(layout, "MODE", 0, 1)
        self.angle_mode_button = self._add_button(layout, "DRG", 0, 2)

        left_button = self._add_button(layout, "◀", 0, 3)
        up_button = self._add_button(layout, "▲", 0, 4)
        down_button = self._add_button(layout, "▼", 0, 5)
        right_button = self._add_button(layout, "▶", 0, 6)

        history_button = self._add_button(layout, "HISTORY", 1, 0, 1, 2)
        self.format_button = self._add_button(layout, "FMT", 1, 2)
        self.fraction_button = self._add_button(layout, "S⇔D", 1, 3)
        delete_button = self._add_button(layout, "DEL", 1, 4)
        clear_button = self._add_button(layout, "AC", 1, 5, 1, 2)

        self.shift_button.clicked.connect(self.shift_requested.emit)
        self.mode_button.clicked.connect(self.mode_requested.emit)
        self.angle_mode_button.clicked.connect(self.angle_mode_requested.emit)
        self.format_button.clicked.connect(self.display_mode_requested.emit)
        self.fraction_button.clicked.connect(self.fraction_toggle_requested.emit)
        left_button.clicked.connect(self.cursor_left_requested.emit)
        right_button.clicked.connect(self.cursor_right_requested.emit)
        up_button.clicked.connect(self.history_up_requested.emit)
        down_button.clicked.connect(self.history_down_requested.emit)
        delete_button.clicked.connect(self.delete_requested.emit)
        clear_button.clicked.connect(self.clear_requested.emit)
        history_button.clicked.connect(self.history_toggle_requested.emit)

    @staticmethod
    def _add_button(
        layout: QGridLayout,
        text: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
    ) -> QPushButton:
        """버튼 생성과 배치를 반복하지 않도록 묶은 보조 함수다."""
        button = QPushButton(text)
        layout.addWidget(button, row, column, row_span, column_span)
        return button

    def set_shift_active(self, active: bool) -> None:
        """SHIFT 버튼의 시각적 활성 상태를 갱신한다."""
        self.shift_button.setProperty("active", active)
        self.shift_button.style().unpolish(self.shift_button)
        self.shift_button.style().polish(self.shift_button)
