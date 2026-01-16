from PyQt5 import QtCore, QtWidgets

from gl_widget import PeriodicTableGLWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("元素周期表")
        self.resize(1400, 900)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)

        left_panel = QtWidgets.QFrame()
        left_panel.setFixedWidth(180)
        left_panel.setStyleSheet("background-color: #111921; border-radius: 6px;")
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setAlignment(QtCore.Qt.AlignTop)
        left_label = QtWidgets.QLabel("功能区域")
        left_label.setStyleSheet("color: #EDEDED; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(left_label)

        center_panel = QtWidgets.QFrame()
        center_layout = QtWidgets.QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        gl_widget = PeriodicTableGLWidget()
        center_layout.addWidget(gl_widget)

        right_panel = QtWidgets.QFrame()
        right_panel.setFixedWidth(160)
        right_panel.setStyleSheet("background-color: #111921; border-radius: 6px;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setAlignment(QtCore.Qt.AlignTop)
        right_layout.setSpacing(12)

        mode_label = QtWidgets.QLabel("族号切换")
        mode_label.setStyleSheet("color: #EDEDED; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(mode_label)

        group = QtWidgets.QButtonGroup(self)
        buttons = [
            ("IUPAC族号", "iupac"),
            ("CAS族号", "cas"),
            ("大陆惯用族号", "cn"),
        ]
        for idx, (text, mode) in enumerate(buttons):
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet(
                "QPushButton { color: #EDEDED; background-color: #1C2731; padding: 8px; border-radius: 6px; }"
                "QPushButton:checked { background-color: #32455A; }"
            )
            if idx == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, m=mode: gl_widget.set_group_mode(m))
            group.addButton(btn)
            right_layout.addWidget(btn)

        layout.addWidget(left_panel)
        layout.addWidget(center_panel, stretch=1)
        layout.addWidget(right_panel)
        self.setCentralWidget(central)
