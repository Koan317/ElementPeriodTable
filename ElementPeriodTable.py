import math
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLFormat
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import (
    GL_AMBIENT_AND_DIFFUSE,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DIFFUSE,
    GL_FRONT_AND_BACK,
    GL_LIGHT0,
    GL_LIGHTING,
    GL_MODELVIEW,
    GL_POSITION,
    GL_PROJECTION,
    GL_QUADS,
    GL_SHININESS,
    GL_SPECULAR,
    glBegin,
    glClear,
    glClearColor,
    glDisable,
    glEnable,
    glEnd,
    glGetDoublev,
    glGetIntegerv,
    glLightfv,
    glLoadIdentity,
    glMaterialfv,
    glMatrixMode,
    glPopMatrix,
    glPushMatrix,
    glTranslatef,
    glVertex3f,
)
from OpenGL.GLU import gluLookAt, gluPerspective, gluProject, gluUnProject


@dataclass(frozen=True)
class Element:
    number: int
    symbol: str
    name_cn: str
    period: int
    group: int
    series: str


GROUP_COLORS_IUPAC: Dict[int, Tuple[int, int, int]] = {
    1: (203, 77, 77),
    2: (203, 119, 77),
    3: (203, 161, 77),
    4: (203, 203, 77),
    5: (161, 203, 77),
    6: (119, 203, 77),
    7: (77, 203, 77),
    8: (77, 203, 119),
    9: (77, 203, 161),
    10: (77, 203, 203),
    11: (77, 161, 203),
    12: (77, 119, 203),
    13: (77, 77, 203),
    14: (119, 77, 203),
    15: (161, 77, 203),
    16: (203, 77, 203),
    17: (203, 77, 161),
    18: (203, 77, 119),
}

GROUP_LABELS = {
    "iupac": [str(i) for i in range(1, 19)],
    "cas": [
        "IA",
        "IIA",
        "IIIB",
        "IVB",
        "VB",
        "VIB",
        "VIIB",
        "VIIIB",
        "VIIIB",
        "VIIIB",
        "IB",
        "IIB",
        "IIIA",
        "IVA",
        "VA",
        "VIA",
        "VIIA",
        "VIIIA",
    ],
    "cn": [
        "IA",
        "IIA",
        "IIIB",
        "IVB",
        "VB",
        "VIB",
        "VIIB",
        "VIII B",
        "VIII B",
        "VIII B",
        "IB",
        "IIB",
        "IIIA",
        "IVA",
        "VA",
        "VIA",
        "VIIA",
        "0",
    ],
}

PERIOD_NOBLE_GAS_SHELLS = {
    1: (["2"], ["K"]),
    2: (["2", "8"], ["K", "L"]),
    3: (["2", "8", "8"], ["K", "L", "M"]),
    4: (["2", "8", "18", "8"], ["K", "L", "M", "N"]),
    5: (["2", "8", "18", "18", "8"], ["K", "L", "M", "N", "O"]),
    6: (["2", "8", "18", "32", "18", "8"], ["K", "L", "M", "N", "O", "P"]),
    7: (
        ["2", "8", "18", "32", "32", "18", "8"],
        ["K", "L", "M", "N", "O", "P", "Q"],
    ),
}

METALLOID_LINE = {"B", "Si", "Ge", "As", "Sb", "Te", "Po", "At"}
NON_METALS = {
    "H",
    "He",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "P",
    "S",
    "Cl",
    "Ar",
    "Se",
    "Br",
    "Kr",
    "I",
    "Xe",
    "Rn",
    "Og",
    "At",
    "Ts",
}

RADIOACTIVE = {43, 61} | set(range(84, 119))


ELEMENT_SYMBOLS = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]

ELEMENT_NAMES_CN = [
    "氢",
    "氦",
    "锂",
    "铍",
    "硼",
    "碳",
    "氮",
    "氧",
    "氟",
    "氖",
    "钠",
    "镁",
    "铝",
    "硅",
    "磷",
    "硫",
    "氯",
    "氩",
    "钾",
    "钙",
    "钪",
    "钛",
    "钒",
    "铬",
    "锰",
    "铁",
    "钴",
    "镍",
    "铜",
    "锌",
    "镓",
    "锗",
    "砷",
    "硒",
    "溴",
    "氪",
    "铷",
    "锶",
    "钇",
    "锆",
    "铌",
    "钼",
    "锝",
    "钌",
    "铑",
    "钯",
    "银",
    "镉",
    "铟",
    "锡",
    "锑",
    "碲",
    "碘",
    "氙",
    "铯",
    "钡",
    "镧",
    "铈",
    "镨",
    "钕",
    "钷",
    "钐",
    "铕",
    "钆",
    "铽",
    "镝",
    "钬",
    "铒",
    "铥",
    "镱",
    "镥",
    "铪",
    "钽",
    "钨",
    "铼",
    "锇",
    "铱",
    "铂",
    "金",
    "汞",
    "铊",
    "铅",
    "铋",
    "钋",
    "砹",
    "氡",
    "钫",
    "镭",
    "锕",
    "钍",
    "镤",
    "铀",
    "镎",
    "钚",
    "镅",
    "锔",
    "锫",
    "锎",
    "锿",
    "镄",
    "钔",
    "锘",
    "铹",
    "𬬻",
    "𬭊",
    "𬭳",
    "𬭛",
    "𬭶",
    "鿏",
    "𫟼",
    "𬬭",
    "鿔",
    "鿭",
    "𫟷",
    "镆",
    "鉝",
    "鿬",
    "鿫",
]


PERIOD_LAYOUT = {
    1: [(1, "H"), (18, "He")],
    2: [(1, "Li"), (2, "Be"), (13, "B"), (14, "C"), (15, "N"), (16, "O"), (17, "F"), (18, "Ne")],
    3: [(1, "Na"), (2, "Mg"), (13, "Al"), (14, "Si"), (15, "P"), (16, "S"), (17, "Cl"), (18, "Ar")],
    4: [(1, "K"), (2, "Ca"), (3, "Sc"), (4, "Ti"), (5, "V"), (6, "Cr"), (7, "Mn"), (8, "Fe"), (9, "Co"), (10, "Ni"), (11, "Cu"), (12, "Zn"), (13, "Ga"), (14, "Ge"), (15, "As"), (16, "Se"), (17, "Br"), (18, "Kr")],
    5: [(1, "Rb"), (2, "Sr"), (3, "Y"), (4, "Zr"), (5, "Nb"), (6, "Mo"), (7, "Tc"), (8, "Ru"), (9, "Rh"), (10, "Pd"), (11, "Ag"), (12, "Cd"), (13, "In"), (14, "Sn"), (15, "Sb"), (16, "Te"), (17, "I"), (18, "Xe")],
    6: [(1, "Cs"), (2, "Ba"), (3, "La"), (4, "Hf"), (5, "Ta"), (6, "W"), (7, "Re"), (8, "Os"), (9, "Ir"), (10, "Pt"), (11, "Au"), (12, "Hg"), (13, "Tl"), (14, "Pb"), (15, "Bi"), (16, "Po"), (17, "At"), (18, "Rn")],
    7: [(1, "Fr"), (2, "Ra"), (3, "Ac"), (4, "Rf"), (5, "Db"), (6, "Sg"), (7, "Bh"), (8, "Hs"), (9, "Mt"), (10, "Ds"), (11, "Rg"), (12, "Cn"), (13, "Nh"), (14, "Fl"), (15, "Mc"), (16, "Lv"), (17, "Ts"), (18, "Og")],
}

LANTHANIDES = [
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
]

ACTINIDES = [
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
]


def build_elements() -> List[Element]:
    symbol_to_name = dict(zip(ELEMENT_SYMBOLS, ELEMENT_NAMES_CN))
    symbol_to_number = {symbol: idx + 1 for idx, symbol in enumerate(ELEMENT_SYMBOLS)}
    elements: List[Element] = []
    for period, entries in PERIOD_LAYOUT.items():
        for group, symbol in entries:
            elements.append(
                Element(
                    number=symbol_to_number[symbol],
                    symbol=symbol,
                    name_cn=symbol_to_name[symbol],
                    period=period,
                    group=group,
                    series="主族",
                )
            )
    for offset, symbol in enumerate(LANTHANIDES):
        elements.append(
            Element(
                number=symbol_to_number[symbol],
                symbol=symbol,
                name_cn=symbol_to_name[symbol],
                period=8,
                group=3 + offset,
                series="镧系",
            )
        )
    for offset, symbol in enumerate(ACTINIDES):
        elements.append(
            Element(
                number=symbol_to_number[symbol],
                symbol=symbol,
                name_cn=symbol_to_name[symbol],
                period=9,
                group=3 + offset,
                series="锕系",
            )
        )
    return sorted(elements, key=lambda e: e.number)


ELEMENTS = build_elements()


def is_metal(symbol: str) -> bool:
    if symbol in NON_METALS:
        return False
    if symbol in METALLOID_LINE:
        return False
    return True


def group_color(group: int, mode: str) -> Tuple[float, float, float]:
    mapped_group = group
    if mode in {"cas", "cn"} and group in {8, 9, 10}:
        mapped_group = 9
    rgb = GROUP_COLORS_IUPAC.get(mapped_group, (180, 180, 180))
    return tuple(channel / 255.0 for channel in rgb)


class PeriodicTableGLWidget(QOpenGLWidget):
    elementClicked = QtCore.pyqtSignal(int)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.group_mode = "iupac"
        self.hovered_symbol: Optional[str] = None
        self._modelview = None
        self._projection = None
        self._viewport = None
        self._cube_size = 0.9
        self._x_spacing = 1.05
        self._y_spacing = 1.05
        self._right_header_offset = 2.5
        self._left_header_offset = 2.0
        self._split_offset = 0.15

    def set_group_mode(self, mode: str) -> None:
        self.group_mode = mode
        self.update()

    def initializeGL(self) -> None:
        glClearColor(0.08, 0.1, 0.12, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [30.0, 40.0, 60.0, 1.0])

    def resizeGL(self, w: int, h: int) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1.0
        gluPerspective(35.0, aspect, 0.1, 200.0)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera_radius = 45.0
        angle = math.radians(80)
        camera_x = camera_radius * math.cos(angle)
        camera_z = camera_radius * math.sin(angle)
        gluLookAt(camera_x, 0.0, camera_z, 9.0, -4.0, 0.0, 0.0, 1.0, 0.0)

        self._modelview = glGetDoublev(GL_MODELVIEW)
        self._projection = glGetDoublev(GL_PROJECTION)
        self._viewport = glGetIntegerv(GL_VIEWPORT)

        for element in ELEMENTS:
            position = self._element_position(element)
            z_offset = 0.3 if element.symbol == self.hovered_symbol else 0.0
            glPushMatrix()
            glTranslatef(position[0], position[1], position[2] + z_offset)
            self._apply_material(element)
            self._draw_cube(self._cube_size)
            glPopMatrix()

        self._draw_overlay()

    def _apply_material(self, element: Element) -> None:
        color = group_color(element.group, self.group_mode)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [*color, 1.0])
        if is_metal(element.symbol):
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [64.0])
        else:
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [8.0])

    def _draw_cube(self, size: float) -> None:
        half = size / 2
        glBegin(GL_QUADS)
        glVertex3f(-half, -half, half)
        glVertex3f(half, -half, half)
        glVertex3f(half, half, half)
        glVertex3f(-half, half, half)

        glVertex3f(-half, -half, -half)
        glVertex3f(-half, half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, -half, -half)

        glVertex3f(-half, half, -half)
        glVertex3f(-half, half, half)
        glVertex3f(half, half, half)
        glVertex3f(half, half, -half)

        glVertex3f(-half, -half, -half)
        glVertex3f(half, -half, -half)
        glVertex3f(half, -half, half)
        glVertex3f(-half, -half, half)

        glVertex3f(half, -half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, half, half)
        glVertex3f(half, -half, half)

        glVertex3f(-half, -half, -half)
        glVertex3f(-half, -half, half)
        glVertex3f(-half, half, half)
        glVertex3f(-half, half, -half)
        glEnd()

    def _draw_overlay(self) -> None:
        glDisable(GL_LIGHTING)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self._draw_group_headers(painter)
        self._draw_period_headers(painter)
        self._draw_right_headers(painter)
        for element in ELEMENTS:
            self._draw_element_text(painter, element)
        painter.end()
        glEnable(GL_LIGHTING)

    def _draw_group_headers(self, painter: QtGui.QPainter) -> None:
        labels = GROUP_LABELS[self.group_mode]
        font = QtGui.QFont("Microsoft YaHei", 10, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(235, 235, 235))
        for group in range(1, 19):
            x, y, _ = self._grid_to_world(group, 0)
            screen = self._project_point(x, y, 0.0)
            if screen:
                painter.drawText(screen[0] - 14, screen[1] - 12, 28, 20, QtCore.Qt.AlignCenter, labels[group - 1])

    def _draw_period_headers(self, painter: QtGui.QPainter) -> None:
        font = QtGui.QFont("Microsoft YaHei", 10, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(235, 235, 235))
        for period in range(1, 8):
            x, y, _ = self._grid_to_world(0, period)
            screen = self._project_point(x, y, 0.0)
            if screen:
                painter.drawText(screen[0] - 12, screen[1] - 12, 24, 24, QtCore.Qt.AlignCenter, str(period))

    def _draw_right_headers(self, painter: QtGui.QPainter) -> None:
        font = QtGui.QFont("Microsoft YaHei", 9, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(235, 235, 235))
        for period in range(1, 8):
            numbers, shells = PERIOD_NOBLE_GAS_SHELLS[period]
            x_num, y_num, _ = self._grid_to_world(19, period)
            x_shell, y_shell, _ = self._grid_to_world(20, period)
            numbers_screen = self._project_point(x_num, y_num, 0.0)
            shells_screen = self._project_point(x_shell, y_shell, 0.0)
            if numbers_screen:
                self._draw_vertical_stack(painter, numbers_screen, numbers)
            if shells_screen:
                self._draw_vertical_stack(painter, shells_screen, shells)

    def _draw_vertical_stack(self, painter: QtGui.QPainter, pos: Tuple[int, int], items: List[str]) -> None:
        line_height = 12
        x, y = pos
        total_height = line_height * len(items)
        start_y = y - total_height + line_height
        for idx, item in enumerate(items):
            painter.drawText(x - 8, start_y + idx * line_height, 16, line_height, QtCore.Qt.AlignCenter, item)

    def _draw_element_text(self, painter: QtGui.QPainter, element: Element) -> None:
        position = self._element_position(element)
        base = self._project_point(position[0], position[1], position[2] + self._cube_size / 2)
        if not base:
            return
        x, y = base
        number = str(element.number)
        symbol_color = QtGui.QColor(220, 80, 80) if element.number in RADIOACTIVE else QtGui.QColor(245, 245, 245)

        font_small = QtGui.QFont("Microsoft YaHei", 8)
        font_symbol = QtGui.QFont("Microsoft YaHei", 10, QtGui.QFont.Bold)
        font_name = QtGui.QFont("Microsoft YaHei", 9)

        painter.setFont(font_small)
        painter.setPen(QtGui.QColor(240, 240, 240))
        painter.drawText(x - 38, y - 32, 30, 12, QtCore.Qt.AlignLeft, number)

        painter.setFont(font_symbol)
        painter.setPen(symbol_color)
        painter.drawText(x + 6, y - 34, 30, 14, QtCore.Qt.AlignRight, element.symbol)

        painter.setFont(font_name)
        painter.setPen(QtGui.QColor(240, 240, 240))
        painter.drawText(x - 38, y - 8, 76, 16, QtCore.Qt.AlignCenter, element.name_cn)

        painter.setFont(font_small)
        painter.drawText(x - 38, y + 8, 76, 12, QtCore.Qt.AlignCenter, "待补充")
        painter.drawText(x - 38, y + 22, 76, 12, QtCore.Qt.AlignCenter, "待补充")

    def _grid_to_world(self, group: int, period: int) -> Tuple[float, float, float]:
        x = (group - 1) * self._x_spacing
        y = -(period - 1) * self._y_spacing
        if group >= 13:
            x += self._split_offset
        if period == 0:
            y += 0.7
        if group == 0:
            x -= self._left_header_offset
        if group >= 19:
            x += self._right_header_offset
        return x, y, 0.0

    def _element_position(self, element: Element) -> Tuple[float, float, float]:
        group = element.group
        period = element.period
        x, y, z = self._grid_to_world(group, period)
        if element.symbol in METALLOID_LINE or element.symbol in NON_METALS:
            x += self._split_offset
        return x, y, z

    def _project_point(self, x: float, y: float, z: float) -> Optional[Tuple[int, int]]:
        if self._modelview is None or self._projection is None or self._viewport is None:
            return None
        win = gluProject(x, y, z, self._modelview, self._projection, self._viewport)
        if not win:
            return None
        return int(win[0]), int(self.height() - win[1])

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        hovered = self._pick_element(event.pos())
        if hovered != self.hovered_symbol:
            self.hovered_symbol = hovered
            self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton and self.hovered_symbol:
            element = next((el for el in ELEMENTS if el.symbol == self.hovered_symbol), None)
            if element:
                self.elementClicked.emit(element.number)

    def _pick_element(self, pos: QtCore.QPoint) -> Optional[str]:
        if self._modelview is None or self._projection is None or self._viewport is None:
            return None
        x = pos.x()
        y = self.height() - pos.y()
        near = gluUnProject(x, y, 0.0, self._modelview, self._projection, self._viewport)
        far = gluUnProject(x, y, 1.0, self._modelview, self._projection, self._viewport)
        if not near or not far:
            return None
        ray_dir = (
            far[0] - near[0],
            far[1] - near[1],
            far[2] - near[2],
        )
        if ray_dir[2] == 0:
            return None
        t = -near[2] / ray_dir[2]
        if t < 0:
            return None
        hit_x = near[0] + ray_dir[0] * t
        hit_y = near[1] + ray_dir[1] * t
        for element in ELEMENTS:
            pos_x, pos_y, _ = self._element_position(element)
            if abs(hit_x - pos_x) <= self._cube_size / 2 and abs(hit_y - pos_y) <= self._cube_size / 2:
                return element.symbol
        return None


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


def main() -> None:
    fmt = QGLFormat()
    fmt.setSampleBuffers(True)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
