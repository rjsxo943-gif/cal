"""1변수 통계 데이터 입력과 결과 표시를 담당하는 화면."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StatisticsPage(QWidget):
    """데이터 목록과 1변수 요약 통계량을 표시한다."""

    add_values_requested = Signal(str)
    remove_value_requested = Signal(int)
    clear_requested = Signal()

    SUMMARY_DESCRIPTIONS = {
        "n": "Count",
        "Σx": "Sum",
        "x̄": "Mean",
        "min": "Minimum",
        "max": "Maximum",
        "σ²": "Population variance",
        "σ": "Population standard deviation",
        "s²": "Sample variance",
        "s": "Sample standard deviation",
    }

    def __init__(self) -> None:
        super().__init__()
        self.summary_value_labels: dict[str, QLabel] = {}
        self._build_ui()
        self._connect_signals()
        self.set_statistics(
            (),
            (
                ("n", "0"),
                ("Σx", "0"),
                ("x̄", "—"),
                ("min", "—"),
                ("max", "—"),
                ("σ²", "—"),
                ("σ", "—"),
                ("s²", "—"),
                ("s", "—"),
            ),
        )

    def _build_ui(self) -> None:
        """입력부, 데이터 목록, 통계 요약 영역을 구성한다."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 12, 18, 18)
        main_layout.setSpacing(12)

        title_label = QLabel("One-Variable Statistics")
        title_label.setStyleSheet("font-size: 22px; font-weight: 700;")

        description_label = QLabel(
            "Enter one or more real values separated by commas, spaces, or semicolons."
        )
        description_label.setWordWrap(True)
        description_label.setStyleSheet("color: #6b7280;")

        input_layout = QHBoxLayout()
        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText("Example: 10 or 10, 20, 30")
        self.add_button = QPushButton("Add Data")
        self.add_button.setObjectName("equalsButton")
        input_layout.addWidget(self.value_edit, 1)
        input_layout.addWidget(self.add_button)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #b91c1c; font-weight: 600;")
        self.error_label.setWordWrap(True)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        data_frame = QFrame()
        data_frame.setStyleSheet(
            "QFrame { background: white; border: 1px solid #d1d5db; "
            "border-radius: 9px; }"
        )
        data_layout = QVBoxLayout(data_frame)
        data_layout.setContentsMargins(12, 12, 12, 12)
        data_layout.setSpacing(8)

        data_title = QLabel("Data")
        data_title.setStyleSheet("font-size: 17px; font-weight: 700;")
        self.data_list = QListWidget()

        data_button_layout = QHBoxLayout()
        self.remove_button = QPushButton("Delete Selected")
        self.clear_button = QPushButton("Clear All")
        data_button_layout.addWidget(self.remove_button)
        data_button_layout.addWidget(self.clear_button)

        data_layout.addWidget(data_title)
        data_layout.addWidget(self.data_list, 1)
        data_layout.addLayout(data_button_layout)

        summary_frame = QFrame()
        summary_frame.setStyleSheet(
            "QFrame { background: #f8fafc; border: 1px solid #cbd5e1; "
            "border-radius: 9px; }"
        )
        summary_layout = QGridLayout(summary_frame)
        summary_layout.setContentsMargins(14, 12, 14, 12)
        summary_layout.setHorizontalSpacing(12)
        summary_layout.setVerticalSpacing(6)

        summary_title = QLabel("Summary")
        summary_title.setStyleSheet("font-size: 17px; font-weight: 700;")
        summary_layout.addWidget(summary_title, 0, 0, 1, 3)

        for row, symbol in enumerate(self.SUMMARY_DESCRIPTIONS, start=1):
            symbol_label = QLabel(symbol)
            symbol_label.setStyleSheet("font-weight: 700;")
            description = QLabel(self.SUMMARY_DESCRIPTIONS[symbol])
            description.setStyleSheet("color: #6b7280;")
            value_label = QLabel("—")
            value_label.setStyleSheet("font-weight: 600;")

            self.summary_value_labels[symbol] = value_label
            summary_layout.addWidget(symbol_label, row, 0)
            summary_layout.addWidget(description, row, 1)
            summary_layout.addWidget(value_label, row, 2)

        content_layout.addWidget(data_frame, 1)
        content_layout.addWidget(summary_frame, 1)

        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(content_layout, 1)

    def _connect_signals(self) -> None:
        """버튼과 Enter 입력을 외부 요청 Signal로 변환한다."""
        self.add_button.clicked.connect(self._emit_add_request)
        self.value_edit.returnPressed.connect(self._emit_add_request)
        self.remove_button.clicked.connect(self._emit_remove_request)
        self.clear_button.clicked.connect(self.clear_requested.emit)

    def _emit_add_request(self) -> None:
        self.add_values_requested.emit(self.value_edit.text())

    def _emit_remove_request(self) -> None:
        self.remove_value_requested.emit(self.data_list.currentRow())

    def set_statistics(
        self,
        data_rows: tuple[str, ...],
        summary_items: tuple[tuple[str, str], ...],
    ) -> None:
        """데이터 목록과 요약 통계량을 한 번에 갱신한다."""
        self.data_list.clear()
        self.data_list.addItems(data_rows)

        for symbol, value in summary_items:
            label = self.summary_value_labels.get(symbol)
            if label is not None:
                label.setText(value)

        self.error_label.clear()

    def set_error(self, message: str) -> None:
        """통계 입력 또는 삭제 오류를 화면에 표시한다."""
        self.error_label.setText(message)

    def clear_input(self) -> None:
        """성공적으로 데이터를 추가한 뒤 입력창을 비운다."""
        self.value_edit.clear()
        self.value_edit.setFocus()

    def focus_input(self) -> None:
        self.value_edit.setFocus()
