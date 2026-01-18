import math
from typing import List, Optional, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import (
    GL_AMBIENT_AND_DIFFUSE,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_FRONT_AND_BACK,
    GL_LIGHT0,
    GL_LIGHTING,
    GL_MODELVIEW,
    GL_MODELVIEW_MATRIX,
    GL_POSITION,
    GL_PROJECTION,
    GL_PROJECTION_MATRIX,
    GL_QUADS,
    GL_SHININESS,
    GL_SPECULAR,
    GL_VIEWPORT,
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
    glViewport,
    glVertex3f,
)
from OpenGL.GLU import gluLookAt, gluPerspective, gluProject, gluUnProject

from element_data import (
    ELEMENTS,
    GROUP_LABELS,
    METALLOID_LINE,
    NON_METALS,
    PERIOD_NOBLE_GAS_SHELLS,
    RADIOACTIVE,
    Element,
    group_color,
    is_metal,
)


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
        glViewport(0, 0, w, h)
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

        self._modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        self._projection = glGetDoublev(GL_PROJECTION_MATRIX)
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
