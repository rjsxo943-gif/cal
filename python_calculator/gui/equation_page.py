"""이차방정식 계수 입력과 근 표시를 담당하는 화면."""

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


class EquationPage(QWidget):
    """ax² + bx + c = 0 형태의 이차방정식 입력 화면."""

    solve_requested = Signal(str, str, str)

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        """계수 입력부, 실행 버튼, 결과 영역을 구성한다."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 12, 18, 18)
        main_layout.setSpacing(14)

        title_label = QLabel("Quadratic Equation")
        title_label.setStyleSheet("font-size: 22px; font-weight: 700;")

        equation_label = QLabel("ax² + bx + c = 0")
        equation_label.setStyleSheet(
            "font-size: 24px; color: #1f2937; padding: 8px 0;"
        )

        description_label = QLabel(
            "Enter real coefficients a, b, and c. Coefficient a cannot be zero."
        )
        description_label.setWordWrap(True)
        description_label.setStyleSheet("color: #6b7280;")

        coefficient_frame = QFrame()
        coefficient_frame.setStyleSheet(
            "QFrame {"
            "background: white;"
            "border: 1px solid #d1d5db;"
            "border-radius: 9px;"
            "}"
        )
        coefficient_layout = QGridLayout(coefficient_frame)
        coefficient_layout.setContentsMargins(16, 14, 16, 14)
        coefficient_layout.setHorizontalSpacing(10)
        coefficient_layout.setVerticalSpacing(10)

        self.a_edit = self._create_coefficient_edit("a")
        self.b_edit = self._create_coefficient_edit("b")
        self.c_edit = self._create_coefficient_edit("c")

        coefficient_layout.addWidget(QLabel("a"), 0, 0)
        coefficient_layout.addWidget(self.a_edit, 0, 1)
        coefficient_layout.addWidget(QLabel("b"), 1, 0)
        coefficient_layout.addWidget(self.b_edit, 1, 1)
        coefficient_layout.addWidget(QLabel("c"), 2, 0)
        coefficient_layout.addWidget(self.c_edit, 2, 1)

        button_layout = QHBoxLayout()
        self.solve_button = QPushButton("Solve")
        self.solve_button.setObjectName("equalsButton")
        self.clear_button = QPushButton("Clear")
        button_layout.addWidget(self.solve_button)
        button_layout.addWidget(self.clear_button)

        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(
            "QFrame {"
            "background: #f8fafc;"
            "border: 1px solid #cbd5e1;"
            "border-radius: 9px;"
            "}"
        )
        result_layout = QVBoxLayout(self.result_frame)
        result_layout.setContentsMargins(16, 14, 16, 14)
        result_layout.setSpacing(7)

        self.classification_label = QLabel("Enter coefficients and press Solve.")
        self.classification_label.setStyleSheet(
            "font-size: 17px; font-weight: 700;"
        )
        self.discriminant_label = QLabel("")
        self.roots_label = QLabel("")
        self.roots_label.setStyleSheet("font-size: 18px;")
        self.roots_label.setWordWrap(True)

        result_layout.addWidget(self.classification_label)
        result_layout.addWidget(self.discriminant_label)
        result_layout.addWidget(self.roots_label)

        main_layout.addWidget(title_label)
        main_layout.addWidget(equation_label)
        main_layout.addWidget(description_label)
        main_layout.addWidget(coefficient_frame)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_frame)
        main_layout.addStretch()

    def _connect_signals(self) -> None:
        """입력창과 버튼 동작을 연결한다."""
        self.solve_button.clicked.connect(self._emit_solve_request)
        self.clear_button.clicked.connect(self.clear)

        self.a_edit.returnPressed.connect(self.b_edit.setFocus)
        self.b_edit.returnPressed.connect(self.c_edit.setFocus)
        self.c_edit.returnPressed.connect(self._emit_solve_request)

    @staticmethod
    def _create_coefficient_edit(placeholder: str) -> QLineEdit:
        """과학적 표기법까지 허용하는 계수 입력창을 만든다."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)

        validator = QDoubleValidator(line_edit)
        validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        line_edit.setValidator(validator)
        return line_edit

    def _emit_solve_request(self) -> None:
        """현재 입력된 세 계수를 MainWindow로 전달한다."""
        self.solve_requested.emit(
            self.a_edit.text(),
            self.b_edit.text(),
            self.c_edit.text(),
        )

    def set_solution(
        self,
        classification: str,
        discriminant_text: str,
        root_lines: tuple[str, ...],
    ) -> None:
        """정상 계산된 근과 판별식을 표시한다."""
        self.classification_label.setText(classification)
        self.classification_label.setStyleSheet(
            "font-size: 17px; font-weight: 700; color: #111827;"
        )
        self.discriminant_label.setText(discriminant_text)
        self.roots_label.setText("\n".join(root_lines))

    def set_error(self, message: str) -> None:
        """입력 또는 계산 오류를 결과 영역에 표시한다."""
        self.classification_label.setText(message)
        self.classification_label.setStyleSheet(
            "font-size: 17px; font-weight: 700; color: #b91c1c;"
        )
        self.discriminant_label.clear()
        self.roots_label.clear()

    def clear(self) -> None:
        """계수와 결과를 초기화한다."""
        self.a_edit.clear()
        self.b_edit.clear()
        self.c_edit.clear()
        self.classification_label.setText("Enter coefficients and press Solve.")
        self.classification_label.setStyleSheet(
            "font-size: 17px; font-weight: 700;"
        )
        self.discriminant_label.clear()
        self.roots_label.clear()
        self.a_edit.setFocus()

    def focus_first_coefficient(self) -> None:
        """Equation 모드로 들어왔을 때 첫 입력창에 포커스를 둔다."""
        self.a_edit.setFocus()
