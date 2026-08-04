"""프로그램의 최상위 창과 좌우 패널을 관리한다."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter

from core.calculator_controller import CalculatorController
from gui.calculator_widget import CalculatorWidget
from gui.history_panel import HistoryPanel


class MainWindow(QMainWindow):
    """계산기 본체와 계산 기록 패널을 담는 최상위 창."""

    def __init__(self) -> None:
        super().__init__()

        self.calculator_controller = CalculatorController()

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
        """FMT 요청을 처리하고 최근 결과를 새 형식으로 다시 표시한다."""
        self.calculator_controller.cycle_display_mode()
        state = self.calculator_controller.state
        self.calculator_widget.set_display_mode(state.display_mode_label)

        calculation = self.calculator_controller.redisplay_last_result()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

    def _toggle_fraction_display(self) -> None:
        """S⇔D 요청으로 최근 결과의 소수·분수 표시를 전환한다."""
        calculation = self.calculator_controller.toggle_fraction_display()
        if calculation is not None:
            self.calculator_widget.set_result(calculation.display_text)

    def _handle_calculate_request(self, expression: str) -> None:
        """Controller에 계산을 요청하고 결과와 기록을 갱신한다."""
        calculation = self.calculator_controller.calculate(expression)
        self.calculator_widget.set_result(calculation.display_text)

        if calculation.is_success:
            self.history_panel.add_entry(
                expression,
                calculation.display_text,
            )
