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

        # GUI와 계산 엔진은 이 Controller가 가진 CalculatorState를 공유한다.
        self.calculator_controller = CalculatorController()

        # 창 전체 수준의 설정만 MainWindow에서 담당한다.
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

        # QSplitter를 사용하면 사용자가 경계선을 드래그해
        # 계산기 영역과 기록 패널의 너비를 조절할 수 있다.
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.calculator_widget)
        self.main_splitter.addWidget(self.history_panel)

        # 계산기 본체가 기록 패널보다 더 많이 확장되도록 설정한다.
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
        self.history_panel.expression_selected.connect(
            self.calculator_widget.set_expression
        )

    def _synchronize_state_display(self) -> None:
        """프로그램 시작 시 Controller 상태를 GUI 상태 표시와 맞춘다."""
        self.calculator_widget.set_angle_mode(
            self.calculator_controller.state.angle_mode.value
        )

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

    def _handle_calculate_request(self, expression: str) -> None:
        """Controller에 계산을 요청하고 결과와 기록을 갱신한다."""
        calculation = self.calculator_controller.calculate(expression)

        # 성공과 오류 모두 Controller가 정한 공통 문자열로 표시한다.
        self.calculator_widget.set_result(calculation.display_text)

        # 오류 수식은 계산 기록에 추가하지 않고 성공한 계산만 저장한다.
        if calculation.is_success:
            self.history_panel.add_entry(
                expression,
                calculation.display_text,
            )
