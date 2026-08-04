"""프로그램의 최상위 창과 좌우 패널을 관리한다."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter

from core.calculator_controller import CalculatorController
from core.equation_controller import EquationController, EquationDisplayResult
from gui.calculator_widget import CalculatorWidget
from gui.history_panel import HistoryPanel


class MainWindow(QMainWindow):
    """계산기 본체와 계산 기록 패널을 담는 최상위 창."""

    def __init__(self) -> None:
        super().__init__()

        self.calculator_controller = CalculatorController()

        # EquationController도 같은 CalculatorState를 공유하므로
        # FMT 변경이 일반 계산과 방정식 결과에 동일하게 적용된다.
        self.equation_controller = EquationController(
            self.calculator_controller.state
        )

        self.setWindowTitle("Scientific Calculator")
        self.resize(1050, 720)
        self.setMinimumSize(780, 600)

        self._build_ui()
        self._connect_signals()
        self._synchronize_state_display()

    def _build_ui(self) -> None:
        """왼쪽 계산기와 오른쪽 기록 패널을 배치한다."""
        self.calculator_widget = CalculatorWidget()
        self.history_panel = HistoryPanel()

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.calculator_widget)
        self.main_splitter.addWidget(self.history_panel)

        self.main_splitter.setStretchFactor(0, 4)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setSizes([800, 250])

        self.setCentralWidget(self.main_splitter)

    def _connect_signals(self) -> None:
        """하위 위젯의 요청을 창 수준 동작과 연결한다."""
        self.calculator_widget.history_toggle_requested.connect(
            self._toggle_history_panel
        )
        self.calculator_widget.calculate_requested.connect(
            self._handle_calculate_request
        )
        self.calculator_widget.quadratic_solve_requested.connect(
            self._handle_quadratic_solve_request
        )
        self.calculator_widget.angle_mode_requested.connect(
            self._cycle_angle_mode
        )
        self.calculator_widget.display_mode_requested.connect(
            self._cycle_display_mode
        )
        self.calculator_widget.fraction_toggle_requested.connect(
            self._toggle_fraction_display
        )
        self.history_panel.expression_selected.connect(
            self.calculator_widget.set_expression
        )

    def _synchronize_state_display(self) -> None:
        """프로그램 시작 시 Controller 상태와 GUI 표시를 맞춘다."""
        state = self.calculator_controller.state
        self.calculator_widget.set_angle_mode(state.angle_mode.value)
        self.calculator_widget.set_display_mode(state.display_mode_label)

    def _toggle_history_panel(self) -> None:
        """HISTORY 버튼으로 오른쪽 패널을 열거나 닫는다."""
        if self.history_panel.isVisible():
            self.history_panel.hide()
        else:
            self.history_panel.show()
            self.main_splitter.setSizes([800, 250])

    def _cycle_angle_mode(self) -> None:
        """DRG 요청을 처리하고 변경된 각도 모드를 화면에 표시한다."""
        angle_mode = self.calculator_controller.cycle_angle_mode()
        self.calculator_widget.set_angle_mode(angle_mode.value)

    def _cycle_display_mode(self) -> None:
        """FMT 요청을 처리하고 최근 결과들을 새 형식으로 다시 표시한다."""
        self.calculator_controller.cycle_display_mode()
        state = self.calculator_controller.state
        self.calculator_widget.set_display_mode(state.display_mode_label)

        calculation = self.calculator_controller.redisplay_last_result()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

        equation_result = self.equation_controller.redisplay_last_solution()
        if equation_result is not None:
            self._display_equation_result(equation_result)

    def _toggle_fraction_display(self) -> None:
        """S⇔D 요청으로 최근 일반 계산 결과의 소수·분수 표시를 전환한다."""
        calculation = self.calculator_controller.toggle_fraction_display()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

    def _handle_calculate_request(self, expression: str) -> None:
        """Controller에 일반 계산을 요청하고 결과와 기록을 갱신한다."""
        calculation = self.calculator_controller.calculate(expression)
        self.calculator_widget.set_result(calculation.display_text)

        if calculation.is_success:
            self.history_panel.add_entry(
                expression,
                calculation.display_text,
            )

    def _handle_quadratic_solve_request(
        self,
        a_text: str,
        b_text: str,
        c_text: str,
    ) -> None:
        """EquationPage의 계수로 이차방정식을 계산한다."""
        result = self.equation_controller.solve(a_text, b_text, c_text)
        self._display_equation_result(result)

    def _display_equation_result(
        self,
        result: EquationDisplayResult,
    ) -> None:
        """EquationController 결과를 성공 또는 오류 화면으로 전달한다."""
        if not result.is_success:
            self.calculator_widget.set_equation_error(result.error_message)
            return

        self.calculator_widget.set_equation_solution(
            result.classification,
            result.discriminant_text,
            result.root_lines,
        )
