from PyQt5 import QtCore, QtWidgets

from gl_widget import PeriodicTableGLWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("元素周期表")
        self.resize(1400, 900)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        left_panel = QtWidgets.QFrame()
        left_panel.setFixedWidth(130)
        left_panel.setStyleSheet("background-color: #111921; border-radius: 6px;")
        left_panel.setVisible(True)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setAlignment(QtCore.Qt.AlignTop)
        left_label = QtWidgets.QLabel("功能区域")
        left_label.setStyleSheet("color: #EDEDED; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(left_label)

        left_toggle = QtWidgets.QToolButton()
        left_toggle.setFixedWidth(10)
        left_toggle.setCheckable(True)
        left_toggle.setChecked(True)
        left_toggle.setStyleSheet(
            "QToolButton { background-color: #1C2731; border: none; }"
            "QToolButton:hover { background-color: #2A3948; }"
        )

        center_panel = QtWidgets.QFrame()
        center_layout = QtWidgets.QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        gl_widget = PeriodicTableGLWidget()
        center_layout.addWidget(gl_widget)

        right_toggle = QtWidgets.QToolButton()
        right_toggle.setFixedWidth(10)
        right_toggle.setCheckable(True)
        right_toggle.setChecked(True)
        right_toggle.setStyleSheet(
            "QToolButton { background-color: #1C2731; border: none; }"
            "QToolButton:hover { background-color: #2A3948; }"
        )

        right_panel = QtWidgets.QFrame()
        right_panel.setFixedWidth(120)
        right_panel.setStyleSheet("background-color: #111921; border-radius: 6px;")
        right_panel.setVisible(True)
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

        def toggle_left_panel(checked: bool) -> None:
            left_panel.setVisible(checked)
            left_panel.setFixedWidth(130 if checked else 0)

        def toggle_right_panel(checked: bool) -> None:
            right_panel.setVisible(checked)
            right_panel.setFixedWidth(120 if checked else 0)

        left_toggle.toggled.connect(toggle_left_panel)
        right_toggle.toggled.connect(toggle_right_panel)

        layout.addWidget(left_panel)
        layout.addWidget(left_toggle)
        layout.addWidget(center_panel, stretch=1)
        layout.addWidget(right_toggle)
        layout.addWidget(right_panel)
        self.setCentralWidget(central)
