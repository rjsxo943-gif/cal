"""복소수의 직교형·극형 입력과 변환 결과를 표시한다."""

from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ComplexPage(QWidget):
    """a + bj와 r∠θ 입력을 서로 변환하는 Complex 모드 화면."""

    rectangular_requested = Signal(str, str)
    polar_requested = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._connect_signals()
        self.set_angle_mode("DEG")

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 12, 18, 18)
        main_layout.setSpacing(12)

        title_label = QLabel("Complex Number")
        title_label.setStyleSheet("font-size: 22px; font-weight: 700;")

        description_label = QLabel(
            "Engineering notation uses j = √-1. Enter rectangular or polar values."
        )
        description_label.setWordWrap(True)
        description_label.setStyleSheet("color: #6b7280;")

        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)

        rectangular_frame = self._create_input_frame()
        rectangular_layout = QGridLayout(rectangular_frame)
        rectangular_layout.setContentsMargins(14, 12, 14, 12)
        rectangular_layout.setSpacing(8)

        rectangular_title = QLabel("Rectangular  a + bj")
        rectangular_title.setStyleSheet("font-size: 17px; font-weight: 700;")
        self.real_edit = self._create_number_edit("Real part a")
        self.imaginary_edit = self._create_number_edit("Imaginary part b")
        self.rectangular_button = QPushButton("Convert from a + bj")
        self.rectangular_button.setObjectName("equalsButton")

        rectangular_layout.addWidget(rectangular_title, 0, 0, 1, 2)
        rectangular_layout.addWidget(QLabel("a"), 1, 0)
        rectangular_layout.addWidget(self.real_edit, 1, 1)
        rectangular_layout.addWidget(QLabel("b"), 2, 0)
        rectangular_layout.addWidget(self.imaginary_edit, 2, 1)
        rectangular_layout.addWidget(self.rectangular_button, 3, 0, 1, 2)

        polar_frame = self._create_input_frame()
        polar_layout = QGridLayout(polar_frame)
        polar_layout.setContentsMargins(14, 12, 14, 12)
        polar_layout.setSpacing(8)

        polar_title = QLabel("Polar  r ∠ θ")
        polar_title.setStyleSheet("font-size: 17px; font-weight: 700;")
        self.magnitude_edit = self._create_number_edit("Magnitude r")
        self.phase_edit = self._create_number_edit("Phase θ")
        self.phase_unit_label = QLabel("θ (DEG)")
        self.polar_button = QPushButton("Convert from r ∠ θ")
        self.polar_button.setObjectName("equalsButton")

        polar_layout.addWidget(polar_title, 0, 0, 1, 2)
        polar_layout.addWidget(QLabel("r"), 1, 0)
        polar_layout.addWidget(self.magnitude_edit, 1, 1)
        polar_layout.addWidget(self.phase_unit_label, 2, 0)
        polar_layout.addWidget(self.phase_edit, 2, 1)
        polar_layout.addWidget(self.polar_button, 3, 0, 1, 2)

        input_layout.addWidget(rectangular_frame, 1)
        input_layout.addWidget(polar_frame, 1)

        action_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        action_layout.addStretch()
        action_layout.addWidget(self.clear_button)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #b91c1c; font-weight: 600;")

        result_frame = QFrame()
        result_frame.setStyleSheet(
            "QFrame { background: #f8fafc; border: 1px solid #cbd5e1; "
            "border-radius: 9px; }"
        )
        result_layout = QGridLayout(result_frame)
        result_layout.setContentsMargins(16, 14, 16, 14)
        result_layout.setHorizontalSpacing(14)
        result_layout.setVerticalSpacing(9)

        result_title = QLabel("Conversion Result")
        result_title.setStyleSheet("font-size: 17px; font-weight: 700;")
        result_layout.addWidget(result_title, 0, 0, 1, 2)

        self.rectangular_result_label = self._add_result_row(
            result_layout, 1, "Rectangular"
        )
        self.polar_result_label = self._add_result_row(
            result_layout, 2, "Polar"
        )
        self.magnitude_result_label = self._add_result_row(
            result_layout, 3, "Magnitude |z|"
        )
        self.phase_result_label = self._add_result_row(
            result_layout, 4, "Phase arg(z)"
        )
        self.conjugate_result_label = self._add_result_row(
            result_layout, 5, "Conjugate z̄"
        )

        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(result_frame)
        main_layout.addStretch()

        self.clear()

    def _connect_signals(self) -> None:
        self.rectangular_button.clicked.connect(
            self._emit_rectangular_request
        )
        self.polar_button.clicked.connect(self._emit_polar_request)
        self.clear_button.clicked.connect(self.clear)

        self.real_edit.returnPressed.connect(self.imaginary_edit.setFocus)
        self.imaginary_edit.returnPressed.connect(
            self._emit_rectangular_request
        )
        self.magnitude_edit.returnPressed.connect(self.phase_edit.setFocus)
        self.phase_edit.returnPressed.connect(self._emit_polar_request)

    @staticmethod
    def _create_input_frame() -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(
            "QFrame { background: white; border: 1px solid #d1d5db; "
            "border-radius: 9px; }"
        )
        return frame

    @staticmethod
    def _create_number_edit(placeholder: str) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        validator = QDoubleValidator(line_edit)
        validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        line_edit.setValidator(validator)
        return line_edit

    @staticmethod
    def _add_result_row(
        layout: QGridLayout,
        row: int,
        title: str,
    ) -> QLabel:
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6b7280;")
        value_label = QLabel("—")
        value_label.setStyleSheet("font-size: 17px; font-weight: 600;")
        value_label.setWordWrap(True)
        layout.addWidget(title_label, row, 0)
        layout.addWidget(value_label, row, 1)
        return value_label

    def _emit_rectangular_request(self) -> None:
        self.rectangular_requested.emit(
            self.real_edit.text(),
            self.imaginary_edit.text(),
        )

    def _emit_polar_request(self) -> None:
        self.polar_requested.emit(
            self.magnitude_edit.text(),
            self.phase_edit.text(),
        )

    def set_result(
        self,
        rectangular_text: str,
        polar_text: str,
        magnitude_text: str,
        phase_text: str,
        conjugate_text: str,
    ) -> None:
        self.rectangular_result_label.setText(rectangular_text)
        self.polar_result_label.setText(polar_text)
        self.magnitude_result_label.setText(magnitude_text)
        self.phase_result_label.setText(phase_text)
        self.conjugate_result_label.setText(conjugate_text)
        self.error_label.clear()

    def set_error(self, message: str) -> None:
        self.error_label.setText(message)

    def set_angle_mode(self, angle_mode_name: str) -> None:
        self.phase_unit_label.setText(f"θ ({angle_mode_name})")

    def clear(self) -> None:
        self.real_edit.clear()
        self.imaginary_edit.clear()
        self.magnitude_edit.clear()
        self.phase_edit.clear()
        self.error_label.clear()

        for label in (
            self.rectangular_result_label,
            self.polar_result_label,
            self.magnitude_result_label,
            self.phase_result_label,
            self.conjugate_result_label,
        ):
            label.setText("—")

        self.real_edit.setFocus()

    def focus_rectangular_input(self) -> None:
        self.real_edit.setFocus()
