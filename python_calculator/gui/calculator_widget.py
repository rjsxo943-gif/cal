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


class CalculatorWidget(QWidget):
    """디스플레이, 공통 제어부, 모드별 입력 화면을 조립한다."""

    # 계산과 상태 변경 요청을 MainWindow에 전달한다.
    calculate_requested = Signal(str)
    history_toggle_requested = Signal()
    angle_mode_requested = Signal()

    # QStackedWidget의 페이지 번호와 화면 표시 이름을 연결한다.
    MODE_NAMES = {
        0: "CALC",
        1: "STAT",
        2: "EQN",
        3: "CMPLX",
    }

    def __init__(self) -> None:
        super().__init__()

        # SHIFT는 한 번 사용할 때까지 유지되는 계산기 상태다.
        self.shift_active = False

        self._build_ui()
        self._connect_signals()

        # 실행 직후 바로 키보드로 수식을 입력할 수 있게 한다.
        self.display_panel.expression_edit.setFocus()

    def _build_ui(self) -> None:
        """계산기 본체를 위에서 아래 방향으로 조립한다."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.display_panel = DisplayPanel()
        self.control_panel = ControlPanel()

        # QStackedWidget은 여러 모드 화면 중 하나만 표시한다.
        # 모든 기능을 한 화면에 동시에 노출하지 않기 위해 사용한다.
        self.mode_stack = QStackedWidget()
        self.mode_stack.addWidget(self._create_calculate_page())
        self.mode_stack.addWidget(self._create_placeholder_page("Statistics Mode"))
        self.mode_stack.addWidget(self._create_placeholder_page("Equation Mode"))
        self.mode_stack.addWidget(self._create_placeholder_page("Complex Mode"))

        self.mode_menu = self._create_mode_menu()

        layout.addWidget(self.display_panel)
        layout.addWidget(self.control_panel)
        layout.addWidget(self.mode_stack, 1)

    def _connect_signals(self) -> None:
        """공통 제어 버튼의 요청을 실제 GUI 동작과 연결한다."""
        control = self.control_panel

        control.shift_requested.connect(self._toggle_shift)
        control.mode_requested.connect(self._show_mode_menu)
        control.angle_mode_requested.connect(self.angle_mode_requested.emit)
        control.cursor_left_requested.connect(
            lambda: self.display_panel.move_cursor(-1)
        )
        control.cursor_right_requested.connect(
            lambda: self.display_panel.move_cursor(1)
        )
        control.delete_requested.connect(
            self.display_panel.delete_previous_character
        )
        control.clear_requested.connect(self.display_panel.clear)
        control.history_toggle_requested.connect(
            self.history_toggle_requested.emit
        )

        # 위/아래 계산 기록 탐색은 기록 데이터 모델을 구현하는
        # 후속 단계에서 실제 동작과 연결한다.
        control.history_up_requested.connect(lambda: None)
        control.history_down_requested.connect(lambda: None)

        # 입력창에서 Enter를 누르면 '=' 버튼과 같은 요청을 발생시킨다.
        self.display_panel.expression_edit.returnPressed.connect(
            self._request_calculation
        )

    def _create_calculate_page(self) -> QWidget:
        """일반 계산 모드의 버튼 그리드를 만든다."""
        page = QWidget()
        layout = QGridLayout(page)
        layout.setSpacing(7)

        # 튜플의 첫 값은 버튼 표기, 두 번째 값은 입력창에 넣을 문자열이다.
        # 화면에는 ÷, ×를 보여주지만 파서 입력은 /, *로 통일한다.
        buttons: list[tuple[str, str | None]] = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("log", "log("),
            ("ln", "ln("),
            ("x²", "^2"),
            ("xʸ", "^"),
            ("√", "sqrt("),
            ("π", "pi"),
            ("e", "e"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("÷", "/"),
            ("(", "("),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("×", "*"),
            (")", ")"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("-", "-"),
            ("Ans", "Ans"),
            ("0", "0"),
            (".", "."),
            ("EXP", "E"),
            ("+", "+"),
            ("=", None),
        ]

        for index, (label, inserted_text) in enumerate(buttons):
            # divmod(index, 5)는 5열 그리드의 행과 열을 동시에 계산한다.
            row, column = divmod(index, 5)
            button = QPushButton(label)

            if label == "=":
                button.setObjectName("equalsButton")
                button.clicked.connect(self._request_calculation)
            else:
                # 반복문 안의 값을 각 버튼에 고정하기 위해
                # 별도의 handler 생성 함수를 사용한다.
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
        """각 입력 버튼이 눌렸을 때 실행할 함수를 만들어 반환한다."""

        def handler() -> None:
            # SHIFT가 켜졌을 때 지원되는 보조 기능이다.
            shift_text = {
                "sin": "asin(",
                "cos": "acos(",
                "tan": "atan(",
                "log": "10^(",
                "ln": "e^(",
            }.get(button_label)

            if self.shift_active and shift_text is not None:
                self.display_panel.insert_text(shift_text)

                # 카시오 계산기처럼 보조 기능을 한 번 사용하면 해제한다.
                self._set_shift_active(False)
            else:
                self.display_panel.insert_text(normal_text)

        return handler

    @staticmethod
    def _create_placeholder_page(title: str) -> QWidget:
        """후속 Phase에서 구현할 모드의 임시 화면을 만든다."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel(f"{title}\nUI will be added in Phase 5")
        label.setStyleSheet("font-size: 20px; color: #6b7280;")

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return page

    def _create_mode_menu(self) -> QMenu:
        """MODE 버튼에서 열리는 모드 선택 메뉴를 만든다."""
        menu = QMenu(self)

        mode_items = [
            ("Calculate", 0),
            ("Statistics", 1),
            ("Equation", 2),
            ("Complex", 3),
        ]

        for text, index in mode_items:
            action = QAction(text, self)

            # page_index=index 기본 인자를 사용해 반복문 현재 값을 고정한다.
            # 이를 생략하면 모든 메뉴가 마지막 index만 참조할 수 있다.
            action.triggered.connect(
                lambda checked=False, page_index=index: self._set_mode(page_index)
            )
            menu.addAction(action)

        return menu

    def _show_mode_menu(self) -> None:
        """MODE 버튼 바로 아래에 모드 메뉴를 표시한다."""
        button = self.control_panel.mode_button
        menu_position = button.mapToGlobal(button.rect().bottomLeft())
        self.mode_menu.popup(menu_position)

    def _set_mode(self, page_index: int) -> None:
        """선택한 모드 페이지와 상단 상태 표시를 함께 변경한다."""
        self.mode_stack.setCurrentIndex(page_index)
        self.display_panel.set_mode_name(self.MODE_NAMES[page_index])
        self.display_panel.expression_edit.setFocus()

    def _toggle_shift(self) -> None:
        """SHIFT 활성 상태를 반전한다."""
        self._set_shift_active(not self.shift_active)

    def _set_shift_active(self, active: bool) -> None:
        """SHIFT 내부 상태와 두 표시 영역을 동시에 갱신한다."""
        self.shift_active = active
        self.display_panel.set_shift_active(active)
        self.control_panel.set_shift_active(active)

    def _request_calculation(self) -> None:
        """현재 수식을 계산 요청 Signal로 전달한다."""
        expression = self.display_panel.expression().strip()

        if not expression:
            self.display_panel.set_result("Invalid input")
            return

        self.calculate_requested.emit(expression)

    def set_result(self, text: str) -> None:
        """MainWindow 또는 Controller가 전달한 결과를 표시한다."""
        self.display_panel.set_result(text)

    def set_expression(self, expression: str) -> None:
        """계산 기록에서 선택한 수식을 입력창으로 복원한다."""
        self.display_panel.expression_edit.setText(expression)
        self.display_panel.expression_edit.setCursorPosition(len(expression))
        self.display_panel.expression_edit.setFocus()

    def set_angle_mode(self, angle_mode_name: str) -> None:
        """Controller의 각도 모드 상태를 디스플레이에 반영한다."""
        self.display_panel.set_angle_mode(angle_mode_name)
        self.display_panel.expression_edit.setFocus()
