import sys

from PyQt5 import QtWidgets
from PyQt5.QtOpenGL import QGLFormat

from main_window import MainWindow


def main() -> None:
    fmt = QGLFormat()
    fmt.setSampleBuffers(True)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
