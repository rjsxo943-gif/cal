"""계산기 본체 GUI와 입력 흐름을 관리한다."""

from collections.abc import Callable

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMenu,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gui.control_panel import ControlPanel
from gui.display_panel import DisplayPanel
from gui.equation_page import EquationPage
from gui.statistics_page import StatisticsPage


class CalculatorWidget(QWidget):
    """디스플레이, 공통 제어부, 모드별 입력 화면을 조립한다."""

    calculate_requested = Signal(str)
    statistics_add_requested = Signal(str)
    statistics_remove_requested = Signal(int)
    statistics_clear_requested = Signal()
    quadratic_solve_requested = Signal(str, str, str)
    history_toggle_requested = Signal()
    angle_mode_requested = Signal()
    display_mode_requested = Signal()
    fraction_toggle_requested = Signal()

    MODE_NAMES = {
        0: "CALC",
        1: "STAT",
        2: "EQN",
        3: "CMPLX",
    }

    SHIFT_INSERT_TEXT = {
        "sin": "asin(",
        "cos": "acos(",
        "tan": "atan(",
        "log": "10^(",
        "ln": "e^(",
        "Ran#": "randint(",
    }

    SHIFT_BUTTON_LABELS = {
        "sin": "asin",
        "cos": "acos",
        "tan": "atan",
        "log": "10ˣ",
        "ln": "eˣ",
        "Ran#": "RanInt",
    }

    def __init__(self) -> None:
        super().__init__()
        self.shift_active = False
        self.calculate_buttons: dict[str, QPushButton] = {}
        self._build_ui()
        self._connect_signals()
        self.display_panel.expression_edit.setFocus()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.display_panel = DisplayPanel()
        self.control_panel = ControlPanel()

        self.mode_stack = QStackedWidget()
        self.mode_stack.addWidget(self._create_calculate_page())

        self.statistics_page = StatisticsPage()
        self.mode_stack.addWidget(self.statistics_page)

        self.equation_page = EquationPage()
        self.mode_stack.addWidget(self.equation_page)

        self.mode_stack.addWidget(self._create_placeholder_page("Complex Mode"))
        self.mode_menu = self._create_mode_menu()

        layout.addWidget(self.display_panel)
        layout.addWidget(self.control_panel)
        layout.addWidget(self.mode_stack, 1)

    def _connect_signals(self) -> None:
        control = self.control_panel
        control.shift_requested.connect(self._toggle_shift)
        control.mode_requested.connect(self._show_mode_menu)
        control.angle_mode_requested.connect(self.angle_mode_requested.emit)
        control.display_mode_requested.connect(self.display_mode_requested.emit)
        control.fraction_toggle_requested.connect(
            self.fraction_toggle_requested.emit
        )
        control.cursor_left_requested.connect(
            lambda: self.display_panel.move_cursor(-1)
        )
        control.cursor_right_requested.connect(
            lambda: self.display_panel.move_cursor(1)
        )
        control.delete_requested.connect(
            self.display_panel.delete_previous_character
        )
        control.clear_requested.connect(self._handle_clear_request)
        control.history_toggle_requested.connect(
            self.history_toggle_requested.emit
        )
        control.history_up_requested.connect(lambda: None)
        control.history_down_requested.connect(lambda: None)

        self.display_panel.expression_edit.returnPressed.connect(
            self._request_calculation
        )
        self.statistics_page.add_values_requested.connect(
            self.statistics_add_requested.emit
        )
        self.statistics_page.remove_value_requested.connect(
            self.statistics_remove_requested.emit
        )
        self.statistics_page.clear_requested.connect(
            self.statistics_clear_requested.emit
        )
        self.equation_page.solve_requested.connect(
            self.quadratic_solve_requested.emit
        )

    def _create_calculate_page(self) -> QWidget:
        page = QWidget()
        layout = QGridLayout(page)
        layout.setSpacing(7)

        buttons: list[tuple[str, str | None]] = [
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("log", "log("), ("ln", "ln("),
            ("x²", "^2"), ("xʸ", "^"), ("√", "sqrt("),
            ("π", "pi"), ("e", "e"),
            ("abs", "abs("), ("1/x", "recip("), ("x!", "!"),
            ("nPr", "npr("), ("nCr", "ncr("),
            ("mod", "mod("), ("GCD", "gcd("), ("LCM", "lcm("),
            (",", ","), ("(", "("),
            ("quot", "quot("), ("rem", "rem("), ("%", "%"),
            ("root", "root("), ("Ran#", "random()"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), (")", ")"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("Ans", "Ans"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"), ("EXP", "E"),
            ("0", "0"), (".", "."), ("+", "+"), ("=", None),
        ]

        for index, (label, inserted_text) in enumerate(buttons):
            row, column = divmod(index, 5)
            button = QPushButton(label)

            if label == "=":
                button.setObjectName("equalsButton")
                button.clicked.connect(self._request_calculation)
                layout.addWidget(button, row, column, 1, 2)
                continue

            self.calculate_buttons[label] = button
            button.setProperty("shifted", False)
            button.clicked.connect(
                self._make_insert_handler(label, inserted_text or "")
            )
            layout.addWidget(button, row, column)

        return page

    def _make_insert_handler(
        self,
        button_label: str,
        normal_text: str,
    ) -> Callable[[], None]:
        def handler() -> None:
            shift_text = self.SHIFT_INSERT_TEXT.get(button_label)

            if self.shift_active and shift_text is not None:
                self.display_panel.insert_text(shift_text)
                self._set_shift_active(False)
            else:
                self.display_panel.insert_text(normal_text)

        return handler

    @staticmethod
    def _create_placeholder_page(title: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(f"{title}\nUI will be added in a later phase")
        label.setStyleSheet("font-size: 20px; color: #6b7280;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return page

    def _create_mode_menu(self) -> QMenu:
        menu = QMenu(self)
        for text, index in (
            ("Calculate", 0),
            ("Statistics", 1),
            ("Equation", 2),
            ("Complex", 3),
        ):
            action = QAction(text, self)
            action.triggered.connect(
                lambda checked=False, page_index=index: self._set_mode(page_index)
            )
            menu.addAction(action)
        return menu

    def _show_mode_menu(self) -> None:
        button = self.control_panel.mode_button
        self.mode_menu.popup(button.mapToGlobal(button.rect().bottomLeft()))

    def _set_mode(self, page_index: int) -> None:
        self.mode_stack.setCurrentIndex(page_index)
        self.display_panel.set_mode_name(self.MODE_NAMES[page_index])

        if page_index == 1:
            self.statistics_page.focus_input()
        elif page_index == 2:
            self.equation_page.focus_first_coefficient()
        else:
            self.display_panel.expression_edit.setFocus()

    def _toggle_shift(self) -> None:
        self._set_shift_active(not self.shift_active)

    def _set_shift_active(self, active: bool) -> None:
        self.shift_active = active
        self.display_panel.set_shift_active(active)
        self.control_panel.set_shift_active(active)
        self._update_shift_button_labels()

    def _update_shift_button_labels(self) -> None:
        for normal_label, shifted_label in self.SHIFT_BUTTON_LABELS.items():
            button = self.calculate_buttons[normal_label]
            button.setText(shifted_label if self.shift_active else normal_label)
            button.setProperty("shifted", self.shift_active)
            button.style().unpolish(button)
            button.style().polish(button)

    def _handle_clear_request(self) -> None:
        current_mode = self.mode_stack.currentIndex()

        if current_mode == 1:
            self.statistics_clear_requested.emit()
        elif current_mode == 2:
            self.equation_page.clear()
        else:
            self.display_panel.clear()

    def _request_calculation(self) -> None:
        expression = self.display_panel.expression().strip()
        if not expression:
            self.display_panel.set_result("Invalid input")
            return
        self.calculate_requested.emit(expression)

    def set_result(self, text: str) -> None:
        self.display_panel.set_result(text)

    def set_expression(self, expression: str) -> None:
        self.display_panel.expression_edit.setText(expression)
        self.display_panel.expression_edit.setCursorPosition(len(expression))
        self.display_panel.expression_edit.setFocus()

    def set_angle_mode(self, angle_mode_name: str) -> None:
        self.display_panel.set_angle_mode(angle_mode_name)

    def set_display_mode(self, display_mode_name: str) -> None:
        self.display_panel.set_display_mode(display_mode_name)

    def set_statistics_display(
        self,
        data_rows: tuple[str, ...],
        summary_items: tuple[tuple[str, str], ...],
    ) -> None:
        self.statistics_page.set_statistics(data_rows, summary_items)

    def set_statistics_error(self, message: str) -> None:
        self.statistics_page.set_error(message)

    def clear_statistics_input(self) -> None:
        self.statistics_page.clear_input()

    def set_equation_solution(
        self,
        classification: str,
        discriminant_text: str,
        root_lines: tuple[str, ...],
    ) -> None:
        self.equation_page.set_solution(
            classification,
            discriminant_text,
            root_lines,
        )

    def set_equation_error(self, message: str) -> None:
        self.equation_page.set_error(message)
