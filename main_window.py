from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets

from element_data import ELEMENTS, Element
from element_wikipedia_data import PROPERTY_LABELS, PROPERTY_ORDER, get_allotropes
from gl_widget import PeriodicTableGLWidget


class ElementDetailPage(QtWidgets.QWidget):
    backRequested = QtCore.pyqtSignal()

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background-color: #0C1218;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        header = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QToolButton()
        self.back_button.setText("返回")
        self.back_button.setStyleSheet(
            "QToolButton { color: #F5F7FA; background-color: #1C2731; padding: 12px 20px; border-radius: 6px;"
            " font-size: 36px; }"
            "QToolButton:hover { background-color: #2A3948; }"
        )
        self.title_label = QtWidgets.QLabel("元素详情")
        self.title_label.setStyleSheet("color: #F5F7FA; font-size: 54px; font-weight: bold;")
        header.addWidget(self.back_button, alignment=QtCore.Qt.AlignLeft)
        header.addSpacing(8)
        header.addWidget(self.title_label)
        header.addStretch()
        layout.addLayout(header)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: #0C1218; }")
        self.content = QtWidgets.QWidget()
        self.content.setStyleSheet("background-color: #0C1218;")
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content_layout.setSpacing(24)
        self.content_layout.addStretch()
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)

        self.back_button.clicked.connect(self.backRequested.emit)

    def set_element(self, element: Element) -> None:
        self.title_label.setText(f"{element.name_cn} ({element.symbol}) 常见单质")
        self._clear_content()
        allotropes = get_allotropes(element.symbol)
        if not allotropes:
            placeholder = QtWidgets.QLabel("暂无可用的维基百科数据。")
            placeholder.setStyleSheet("color: #F5F7FA; font-size: 42px;")
            self.content_layout.addWidget(placeholder)
            self.content_layout.addStretch()
            return

        for allotrope in allotropes:
            group = QtWidgets.QGroupBox(allotrope.name)
            group.setStyleSheet(
                "QGroupBox { color: #F5F7FA; font-size: 42px; font-weight: bold; border: 1px solid #2A3948;"
                " border-radius: 6px; margin-top: 14px; background-color: #141D26; }"
                "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }"
            )
            box_layout = QtWidgets.QVBoxLayout(group)
            box_layout.setContentsMargins(18, 20, 18, 20)
            box_layout.setSpacing(18)

            form = QtWidgets.QFormLayout()
            form.setLabelAlignment(QtCore.Qt.AlignLeft)
            form.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            form.setHorizontalSpacing(40)
            form.setVerticalSpacing(28)
            form.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
            form.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
            for key in PROPERTY_ORDER:
                if key not in allotrope.properties:
                    continue
                value = allotrope.properties[key]
                label = QtWidgets.QLabel(PROPERTY_LABELS.get(key, key))
                label.setStyleSheet("color: #F5F7FA; font-size: 36px;")
                label.setWordWrap(True)
                label.setMinimumWidth(280)
                label.setSizePolicy(
                    QtWidgets.QSizePolicy.Fixed,
                    QtWidgets.QSizePolicy.Preferred,
                )
                value_label = QtWidgets.QLabel(value)
                value_label.setStyleSheet("color: #F5F7FA; font-size: 36px;")
                value_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
                value_label.setWordWrap(True)
                value_label.setSizePolicy(
                    QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Preferred,
                )
                form.addRow(label, value_label)
            if form.rowCount() == 0:
                empty = QtWidgets.QLabel("暂无可展示的属性数据。")
                empty.setStyleSheet("color: #CFD6DE; font-size: 36px;")
                box_layout.addWidget(empty)
            else:
                box_layout.addLayout(form)
            self.content_layout.addWidget(group)
        self.content_layout.addStretch()

    def _clear_content(self) -> None:
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("元素周期表")
        self.resize(1400, 900)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        left_panel = QtWidgets.QFrame()
        left_panel_width = 160
        left_panel.setFixedWidth(left_panel_width)
        left_panel.setStyleSheet("background-color: #111921; border-radius: 6px;")
        left_panel.setVisible(True)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setAlignment(QtCore.Qt.AlignTop)
        left_label = QtWidgets.QLabel("功能区域")
        left_label.setStyleSheet("color: #EDEDED; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(left_label)

        left_toggle = QtWidgets.QToolButton()
        left_toggle.setFixedWidth(12)
        left_toggle.setCheckable(True)
        left_toggle.setChecked(True)
        left_toggle.setStyleSheet(
            "QToolButton { background-color: #1C2731; border: none; }"
            "QToolButton:hover { background-color: #2A3948; }"
        )

        center_panel = QtWidgets.QFrame()
        center_layout = QtWidgets.QStackedLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        table_page = QtWidgets.QWidget()
        table_layout = QtWidgets.QVBoxLayout(table_page)
        table_layout.setContentsMargins(0, 0, 0, 0)
        gl_widget = PeriodicTableGLWidget()
        table_layout.addWidget(gl_widget)
        detail_page = ElementDetailPage()
        center_layout.addWidget(table_page)
        center_layout.addWidget(detail_page)
        center_layout.setCurrentWidget(table_page)

        right_toggle = QtWidgets.QToolButton()
        right_toggle.setFixedWidth(12)
        right_toggle.setCheckable(True)
        right_toggle.setChecked(True)
        right_toggle.setStyleSheet(
            "QToolButton { background-color: #1C2731; border: none; }"
            "QToolButton:hover { background-color: #2A3948; }"
        )

        right_panel = QtWidgets.QFrame()
        right_panel_width = 150
        right_panel.setFixedWidth(right_panel_width)
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

        element_by_number = {element.number: element for element in ELEMENTS}

        def show_element_detail(number: int) -> None:
            element = element_by_number.get(number)
            if element is None:
                return
            detail_page.set_element(element)
            center_layout.setCurrentWidget(detail_page)
            right_panel.setVisible(False)
            right_panel.setFixedWidth(0)
            right_toggle.setVisible(False)
            right_toggle.setFixedWidth(0)

        def show_table() -> None:
            center_layout.setCurrentWidget(table_page)
            right_panel.setVisible(True)
            right_panel.setFixedWidth(right_panel_width)
            right_toggle.setVisible(True)
            right_toggle.setFixedWidth(12)

        def toggle_left_panel(checked: bool) -> None:
            left_panel.setVisible(checked)
            left_panel.setFixedWidth(left_panel_width if checked else 0)

        def toggle_right_panel(checked: bool) -> None:
            right_panel.setVisible(checked)
            right_panel.setFixedWidth(right_panel_width if checked else 0)

        left_toggle.toggled.connect(toggle_left_panel)
        right_toggle.toggled.connect(toggle_right_panel)
        gl_widget.elementClicked.connect(show_element_detail)
        detail_page.backRequested.connect(show_table)

        layout.addWidget(left_panel)
        layout.addWidget(left_toggle)
        layout.addWidget(center_panel, stretch=1)
        layout.addWidget(right_toggle)
        layout.addWidget(right_panel)
        self.setCentralWidget(central)
