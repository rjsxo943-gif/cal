"""GUI 스타일을 계산 로직과 분리해서 관리한다."""

APP_STYLE = """
QWidget {
    font-family: "Segoe UI";
    font-size: 14px;
}

QMainWindow {
    background-color: #f3f4f6;
}

QFrame#displayFrame,
QFrame#historyFrame {
    background-color: white;
    border: 1px solid #d1d5db;
    border-radius: 10px;
}

QLabel#statusLabel {
    color: #4b5563;
    font-size: 12px;
    font-weight: 600;
}

QLineEdit#expressionEdit {
    border: none;
    background: transparent;
    font-size: 21px;
    padding: 8px;
}

QLabel#resultLabel {
    color: #111827;
    font-size: 28px;
    font-weight: 600;
    padding: 8px;
}

QPushButton {
    min-height: 42px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    background-color: white;
}

QPushButton:hover {
    background-color: #eef2ff;
}

QPushButton:pressed {
    background-color: #dbeafe;
}

QPushButton#shiftButton[active="true"] {
    background-color: #fef3c7;
    border-color: #f59e0b;
    font-weight: 700;
}

QPushButton[shifted="true"] {
    background-color: #fff7ed;
    border-color: #fb923c;
    color: #9a3412;
    font-weight: 700;
}

QPushButton#equalsButton {
    background-color: #dbeafe;
    font-weight: 700;
}

QListWidget {
    border: none;
    background: transparent;
}
"""
