"""프로그램의 최상위 창과 좌우 패널을 관리한다."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter

from core.calculator_controller import CalculatorController
from core.complex_controller import ComplexController, ComplexDisplayResult
from core.equation_controller import EquationController, EquationDisplayResult
from core.statistics_controller import (
    StatisticsController,
    StatisticsDisplayResult,
)
from gui.calculator_widget import CalculatorWidget
from gui.history_panel import HistoryPanel


class MainWindow(QMainWindow):
    """계산기 본체와 계산 기록 패널을 담는 최상위 창."""

    def __init__(self) -> None:
        super().__init__()

        self.calculator_controller = CalculatorController()
        shared_state = self.calculator_controller.state

        # 모든 모드는 동일한 각도·표시 상태를 공유한다.
        self.statistics_controller = StatisticsController(shared_state)
        self.equation_controller = EquationController(shared_state)
        self.complex_controller = ComplexController(shared_state)

        self.setWindowTitle("Scientific Calculator")
        self.resize(1050, 720)
        self.setMinimumSize(780, 600)

        self._build_ui()
        self._connect_signals()
        self._synchronize_state_display()

    def _build_ui(self) -> None:
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
        widget = self.calculator_widget

        widget.history_toggle_requested.connect(self._toggle_history_panel)
        widget.calculate_requested.connect(self._handle_calculate_request)
        widget.statistics_add_requested.connect(
            self._handle_statistics_add_request
        )
        widget.statistics_remove_requested.connect(
            self._handle_statistics_remove_request
        )
        widget.statistics_clear_requested.connect(
            self._handle_statistics_clear_request
        )
        widget.quadratic_solve_requested.connect(
            self._handle_quadratic_solve_request
        )
        widget.complex_rectangular_requested.connect(
            self._handle_complex_rectangular_request
        )
        widget.complex_polar_requested.connect(
            self._handle_complex_polar_request
        )
        widget.angle_mode_requested.connect(self._cycle_angle_mode)
        widget.display_mode_requested.connect(self._cycle_display_mode)
        widget.fraction_toggle_requested.connect(
            self._toggle_fraction_display
        )
        self.history_panel.expression_selected.connect(widget.set_expression)

    def _synchronize_state_display(self) -> None:
        state = self.calculator_controller.state
        self.calculator_widget.set_angle_mode(state.angle_mode.value)
        self.calculator_widget.set_display_mode(state.display_mode_label)
        self._display_statistics_result(
            self.statistics_controller.redisplay()
        )

    def _toggle_history_panel(self) -> None:
        if self.history_panel.isVisible():
            self.history_panel.hide()
        else:
            self.history_panel.show()
            self.main_splitter.setSizes([800, 250])

    def _cycle_angle_mode(self) -> None:
        angle_mode = self.calculator_controller.cycle_angle_mode()
        self.calculator_widget.set_angle_mode(angle_mode.value)

        complex_result = self.complex_controller.redisplay_last_result()
        if complex_result is not None:
            self._display_complex_result(complex_result)

    def _cycle_display_mode(self) -> None:
        self.calculator_controller.cycle_display_mode()
        state = self.calculator_controller.state
        self.calculator_widget.set_display_mode(state.display_mode_label)

        calculation = self.calculator_controller.redisplay_last_result()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

        self._display_statistics_result(
            self.statistics_controller.redisplay()
        )

        equation_result = self.equation_controller.redisplay_last_solution()
        if equation_result is not None:
            self._display_equation_result(equation_result)

        complex_result = self.complex_controller.redisplay_last_result()
        if complex_result is not None:
            self._display_complex_result(complex_result)

    def _toggle_fraction_display(self) -> None:
        calculation = self.calculator_controller.toggle_fraction_display()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

    def _handle_calculate_request(self, expression: str) -> None:
        calculation = self.calculator_controller.calculate(expression)
        self.calculator_widget.set_result(calculation.display_text)

        if calculation.is_success:
            self.history_panel.add_entry(
                expression,
                calculation.display_text,
            )

    def _handle_statistics_add_request(self, text: str) -> None:
        result = self.statistics_controller.add_values(text)
        self._display_statistics_result(result)

        if result.is_success:
            self.calculator_widget.clear_statistics_input()

    def _handle_statistics_remove_request(self, index: int) -> None:
        self._display_statistics_result(
            self.statistics_controller.remove_value(index)
        )

    def _handle_statistics_clear_request(self) -> None:
        self._display_statistics_result(
            self.statistics_controller.clear()
        )

    def _display_statistics_result(
        self,
        result: StatisticsDisplayResult,
    ) -> None:
        if not result.is_success:
            self.calculator_widget.set_statistics_error(
                result.error_message
            )
            return

        self.calculator_widget.set_statistics_display(
            result.data_rows,
            result.summary_items,
        )

    def _handle_quadratic_solve_request(
        self,
        a_text: str,
        b_text: str,
        c_text: str,
    ) -> None:
        self._display_equation_result(
            self.equation_controller.solve(a_text, b_text, c_text)
        )

    def _display_equation_result(
        self,
        result: EquationDisplayResult,
    ) -> None:
        if not result.is_success:
            self.calculator_widget.set_equation_error(result.error_message)
            return

        self.calculator_widget.set_equation_solution(
            result.classification,
            result.discriminant_text,
            result.root_lines,
        )

    def _handle_complex_rectangular_request(
        self,
        real_text: str,
        imaginary_text: str,
    ) -> None:
        self._display_complex_result(
            self.complex_controller.from_rectangular(
                real_text,
                imaginary_text,
            )
        )

    def _handle_complex_polar_request(
        self,
        magnitude_text: str,
        phase_text: str,
    ) -> None:
        self._display_complex_result(
            self.complex_controller.from_polar(
                magnitude_text,
                phase_text,
            )
        )

    def _display_complex_result(
        self,
        result: ComplexDisplayResult,
    ) -> None:
        if not result.is_success:
            self.calculator_widget.set_complex_error(result.error_message)
            return

        self.calculator_widget.set_complex_result(
            result.rectangular_text,
            result.polar_text,
            result.magnitude_text,
            result.phase_text,
            result.conjugate_text,
        )
