"""Scientific Calculator 프로그램의 실행 시작점."""

import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.styles import APP_STYLE


def main() -> int:
    """Qt 애플리케이션을 만들고 메인 창을 실행한다."""
    # QApplication은 Qt GUI 프로그램 전체를 관리하는 객체다.
    # 하나의 프로그램에는 QApplication 객체가 하나만 있어야 한다.
    app = QApplication(sys.argv)
    app.setApplicationName("Scientific Calculator")

    # 스타일 코드를 별도 파일에서 가져와 GUI 전체에 적용한다.
    app.setStyleSheet(APP_STYLE)

    # 프로그램의 최상위 창을 생성하고 화면에 표시한다.
    window = MainWindow()
    window.show()

    # 버튼 클릭과 키보드 입력을 계속 처리하는 Qt 이벤트 루프를 시작한다.
    return app.exec()


# 이 파일을 직접 실행했을 때만 프로그램을 시작한다.
# 다른 파일에서 main.py를 import할 때 자동 실행되는 것을 막는다.
if __name__ == "__main__":
    sys.exit(main())
