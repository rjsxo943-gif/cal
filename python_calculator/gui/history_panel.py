"""오른쪽 계산 기록 패널."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout


class HistoryPanel(QFrame):
    """프로그램 실행 중 발생한 계산 기록을 화면에 보관한다."""

    # 기록 항목을 다시 불러올 때 원본 수식을 외부로 전달한다.
    expression_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("historyFrame")
        self.setMinimumWidth(230)
        self._build_ui()

    def _build_ui(self) -> None:
        """제목과 계산 기록 목록을 배치한다."""
        layout = QVBoxLayout(self)

        title = QLabel("Calculation History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.history_list = QListWidget()

        # 기록을 더블클릭하면 그 계산의 원본 수식을 입력창으로 보낸다.
        self.history_list.itemDoubleClicked.connect(self._emit_expression)

        self.empty_item = QListWidgetItem("No calculations yet")
        self.empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.history_list.addItem(self.empty_item)

        layout.addWidget(title)
        layout.addWidget(self.history_list)

    def add_entry(self, expression: str, result: str) -> None:
        """화면용 문자열과 원본 수식을 함께 저장한다."""
        if self.empty_item is not None:
            row = self.history_list.row(self.empty_item)
            self.history_list.takeItem(row)
            self.empty_item = None

        item = QListWidgetItem(f"{expression} = {result}")

        # 화면에는 완성된 기록을 보여주지만, UserRole에는 원본 수식을
        # 별도로 저장해 재입력할 때 결과 문자열이 섞이지 않게 한다.
        item.setData(Qt.ItemDataRole.UserRole, expression)
        self.history_list.insertItem(0, item)

    def _emit_expression(self, item: QListWidgetItem) -> None:
        """선택한 기록에 저장된 원본 수식을 Signal로 전달한다."""
        expression = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(expression, str):
            self.expression_selected.emit(expression)
