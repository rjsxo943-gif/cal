"""상태, 수식, 결과를 표시하는 화면 영역."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class DisplayPanel(QFrame):
    """계산기 상단의 상태 표시와 수식 입력을 담당한다."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("displayFrame")
        self._build_ui()

    def _build_ui(self) -> None:
        """상태 표시, 수식 입력창, 결과 표시창을 배치한다."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(4)

        status_layout = QHBoxLayout()

        self.angle_label = self._create_status_label("DEG")
        self.format_label = self._create_status_label("NORM")
        self.mode_label = self._create_status_label("CALC")
        self.shift_label = self._create_status_label("SHIFT OFF")

        status_layout.addWidget(self.angle_label)
        status_layout.addWidget(self.format_label)
        status_layout.addWidget(self.mode_label)
        status_layout.addStretch()
        status_layout.addWidget(self.shift_label)

        self.expression_edit = QLineEdit()
        self.expression_edit.setObjectName("expressionEdit")
        self.expression_edit.setPlaceholderText("수식을 입력하세요")
        self.expression_edit.setClearButtonEnabled(False)

        self.result_label = QLabel("0")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        main_layout.addLayout(status_layout)
        main_layout.addWidget(self.expression_edit)
        main_layout.addWidget(self.result_label)

    @staticmethod
    def _create_status_label(text: str) -> QLabel:
        """동일한 스타일을 사용하는 상태 라벨을 만든다."""
        label = QLabel(text)
        label.setObjectName("statusLabel")
        return label

    def insert_text(self, text: str) -> None:
        """현재 커서 위치에 문자열을 삽입한다."""
        self.expression_edit.insert(text)
        self.expression_edit.setFocus()

    def delete_previous_character(self) -> None:
        """입력창에서 Backspace와 같은 동작을 실행한다."""
        self.expression_edit.backspace()
        self.expression_edit.setFocus()

    def clear(self) -> None:
        """수식과 결과 표시를 초기화한다."""
        self.expression_edit.clear()
        self.result_label.setText("0")
        self.expression_edit.setFocus()

    def move_cursor(self, offset: int) -> None:
        """커서를 왼쪽(-1) 또는 오른쪽(+1)으로 이동한다."""
        current_position = self.expression_edit.cursorPosition()
        new_position = max(
            0,
            min(len(self.expression_edit.text()), current_position + offset),
        )
        self.expression_edit.setCursorPosition(new_position)
        self.expression_edit.setFocus()

    def expression(self) -> str:
        """현재 입력된 수식을 반환한다."""
        return self.expression_edit.text()

    def set_result(self, text: str) -> None:
        """결과 표시 문자열을 변경한다."""
        self.result_label.setText(text)

    def set_shift_active(self, active: bool) -> None:
        """SHIFT 상태 표시를 갱신한다."""
        self.shift_label.setText("SHIFT ON" if active else "SHIFT OFF")

    def set_mode_name(self, mode_name: str) -> None:
        """현재 계산 모드의 축약 이름을 표시한다."""
        self.mode_label.setText(mode_name)

    def set_angle_mode(self, angle_mode_name: str) -> None:
        """현재 삼각함수 각도 단위를 표시한다."""
        self.angle_label.setText(angle_mode_name)

    def set_display_mode(self, display_mode_name: str) -> None:
        """현재 결과 표시 형식을 상단 상태 영역에 표시한다."""
        self.format_label.setText(display_mode_name)
