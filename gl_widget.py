import math
from typing import List, Optional, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import (
    GL_AMBIENT_AND_DIFFUSE,
    GL_AMBIENT,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DIFFUSE,
    GL_FRONT_AND_BACK,
    GL_LIGHT0,
    GL_LIGHT_MODEL_AMBIENT,
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
    glLightModelfv,
    glLoadIdentity,
    glMaterialfv,
    glMatrixMode,
    glNormal3f,
    glOrtho,
    glPopMatrix,
    glPushMatrix,
    glTranslatef,
    glViewport,
    glVertex3f,
)
from OpenGL.GLU import gluLookAt, gluProject, gluUnProject

from element_data import ELEMENTS, GROUP_LABELS, PERIOD_NOBLE_GAS_SHELLS, RADIOACTIVE, Element, element_color, is_metal


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
        self._cube_size = 1.35
        self._x_spacing = 1.55
        self._y_spacing = 1.55
        self._right_header_offset = 1.6
        self._left_header_offset = 1.2
        self._font_family = "Noto Sans Mono CJK SC"
        self._group_font_family = "Noto Sans CJK SC"
        self._margin_cells = 1.0
        self._camera_radius = 38.0
        self._camera_angle = math.radians(78)
        self._camera_target = (9.0, -4.2, 0.0)

    def set_group_mode(self, mode: str) -> None:
        self.group_mode = mode
        self.update()

    def initializeGL(self) -> None:
        glClearColor(0.08, 0.1, 0.12, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 80.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.12, 1.12, 1.12, 1.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1.0
        left, right, bottom, top = self._projection_bounds(aspect)
        glOrtho(left, right, bottom, top, -200.0, 200.0)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera_x, camera_z = self._camera_position()
        target_x, target_y, target_z = self._camera_target
        gluLookAt(camera_x, 0.0, camera_z, target_x, target_y, target_z, 0.0, 1.0, 0.0)

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
        color = element_color(element, self.group_mode)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [*color, 1.0])
        if is_metal(element.symbol):
            specular = [0.9, 0.9, 0.9, 1.0]
            shininess = [64.0]
            if self._has_metal_radical(element.name_cn):
                specular = [1.0, 1.0, 1.0, 1.0]
                shininess = [96.0]
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
        else:
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [8.0])

    def _draw_cube(self, size: float) -> None:
        half = size / 2
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-half, -half, half)
        glVertex3f(half, -half, half)
        glVertex3f(half, half, half)
        glVertex3f(-half, half, half)

        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, -half, -half)

        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-half, half, -half)
        glVertex3f(-half, half, half)
        glVertex3f(half, half, half)
        glVertex3f(half, half, -half)

        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-half, -half, -half)
        glVertex3f(half, -half, -half)
        glVertex3f(half, -half, half)
        glVertex3f(-half, -half, half)

        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(half, -half, -half)
        glVertex3f(half, half, -half)
        glVertex3f(half, half, half)
        glVertex3f(half, -half, half)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-half, -half, -half)
        glVertex3f(-half, -half, half)
        glVertex3f(-half, half, half)
        glVertex3f(-half, half, -half)
        glEnd()

    def _camera_position(self) -> Tuple[float, float]:
        camera_x = self._camera_radius * math.cos(self._camera_angle)
        camera_z = self._camera_radius * math.sin(self._camera_angle)
        return camera_x, camera_z

    def _projection_bounds(self, aspect: float) -> Tuple[float, float, float, float]:
        min_x, max_x, min_y, max_y = self._table_bounds_world()
        view_min_x, view_max_x, view_min_y, view_max_y = self._table_bounds_view(
            min_x,
            max_x,
            min_y,
            max_y,
        )
        margin_x = self._margin_cells * self._x_spacing
        margin_y = self._margin_cells * self._y_spacing
        left = view_min_x - margin_x
        right = view_max_x + margin_x
        bottom = view_min_y - margin_y
        top = view_max_y + margin_y
        width = right - left
        height = top - bottom
        if height <= 0 or width <= 0:
            return left, right, bottom, top
        current_aspect = width / height
        if current_aspect < aspect:
            right = left + height * aspect
        elif current_aspect > aspect:
            bottom = top - width / aspect
        return left, right, bottom, top

    def _table_bounds_world(self) -> Tuple[float, float, float, float]:
        min_x = float("inf")
        max_x = float("-inf")
        min_y = float("inf")
        max_y = float("-inf")
        for element in ELEMENTS:
            x, y, _ = self._element_position(element)
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        half = self._cube_size / 2
        return min_x - half, max_x + half, min_y - half, max_y + half

    def _table_bounds_view(
        self,
        min_x: float,
        max_x: float,
        min_y: float,
        max_y: float,
    ) -> Tuple[float, float, float, float]:
        camera_x, camera_z = self._camera_position()
        target_x, target_y, target_z = self._camera_target
        view_matrix = self._look_at_matrix(
            (camera_x, 0.0, camera_z),
            (target_x, target_y, target_z),
            (0.0, 1.0, 0.0),
        )
        z_half = self._cube_size / 2
        min_view_x = float("inf")
        max_view_x = float("-inf")
        min_view_y = float("inf")
        max_view_y = float("-inf")
        for x in (min_x, max_x):
            for y in (min_y, max_y):
                for z in (-z_half, z_half):
                    view_x, view_y, _ = self._transform_point(view_matrix, (x, y, z))
                    min_view_x = min(min_view_x, view_x)
                    max_view_x = max(max_view_x, view_x)
                    min_view_y = min(min_view_y, view_y)
                    max_view_y = max(max_view_y, view_y)
        return min_view_x, max_view_x, min_view_y, max_view_y

    def _look_at_matrix(
        self,
        eye: Tuple[float, float, float],
        center: Tuple[float, float, float],
        up: Tuple[float, float, float],
    ) -> List[List[float]]:
        fx, fy, fz = (
            center[0] - eye[0],
            center[1] - eye[1],
            center[2] - eye[2],
        )
        f_len = math.sqrt(fx * fx + fy * fy + fz * fz)
        if f_len == 0:
            f_len = 1.0
        fx, fy, fz = fx / f_len, fy / f_len, fz / f_len
        up_len = math.sqrt(up[0] * up[0] + up[1] * up[1] + up[2] * up[2])
        if up_len == 0:
            up_len = 1.0
        upx, upy, upz = up[0] / up_len, up[1] / up_len, up[2] / up_len
        sx = fy * upz - fz * upy
        sy = fz * upx - fx * upz
        sz = fx * upy - fy * upx
        s_len = math.sqrt(sx * sx + sy * sy + sz * sz)
        if s_len == 0:
            s_len = 1.0
        sx, sy, sz = sx / s_len, sy / s_len, sz / s_len
        ux = sy * fz - sz * fy
        uy = sz * fx - sx * fz
        uz = sx * fy - sy * fx
        return [
            [
                sx,
                sy,
                sz,
                -(sx * eye[0] + sy * eye[1] + sz * eye[2]),
            ],
            [
                ux,
                uy,
                uz,
                -(ux * eye[0] + uy * eye[1] + uz * eye[2]),
            ],
            [
                -fx,
                -fy,
                -fz,
                fx * eye[0] + fy * eye[1] + fz * eye[2],
            ],
            [0.0, 0.0, 0.0, 1.0],
        ]

    def _transform_point(
        self,
        matrix: List[List[float]],
        point: Tuple[float, float, float],
    ) -> Tuple[float, float, float]:
        x, y, z = point
        view_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3]
        view_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3]
        view_z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3]
        return view_x, view_y, view_z

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
        font = QtGui.QFont(self._group_font_family, 8, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(235, 235, 235))
        for group in range(1, 19):
            x, y, _ = self._grid_to_world(group, 1)
            y += self._cube_size / 2 - 0.05
            screen = self._project_point(x, y, 0.0)
            if screen:
                painter.drawText(screen[0] - 20, screen[1] - 14, 40, 16, QtCore.Qt.AlignCenter, labels[group - 1])

    def _draw_period_headers(self, painter: QtGui.QPainter) -> None:
        font = QtGui.QFont(self._font_family, 11, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(235, 235, 235))
        for period in range(1, 8):
            x, y, _ = self._grid_to_world(0, period)
            screen = self._project_point(x, y, 0.0)
            if screen:
                painter.drawText(screen[0] - 12, screen[1] - 12, 24, 24, QtCore.Qt.AlignCenter, str(period))

    def _draw_right_headers(self, painter: QtGui.QPainter) -> None:
        font = QtGui.QFont(self._font_family, 10, QtGui.QFont.Bold)
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
        line_height = 14
        x, y = pos
        total_height = line_height * len(items)
        start_y = y - total_height + line_height
        for idx, item in enumerate(items):
            painter.drawText(x - 8, start_y + idx * line_height, 16, line_height, QtCore.Qt.AlignCenter, item)

    def _draw_element_text(self, painter: QtGui.QPainter, element: Element) -> None:
        position = self._element_position(element)
        half = self._cube_size / 2
        front_z = position[2] + half
        top_left = self._project_point(position[0] - half, position[1] + half, front_z)
        bottom_right = self._project_point(position[0] + half, position[1] - half, front_z)
        if not top_left or not bottom_right:
            return
        left = min(top_left[0], bottom_right[0])
        top = min(top_left[1], bottom_right[1])
        rect = QtCore.QRectF(
            left,
            top,
            max(1.0, abs(bottom_right[0] - top_left[0])),
            max(1.0, abs(bottom_right[1] - top_left[1])),
        )
        number = str(element.number)
        symbol_color = QtGui.QColor(220, 80, 80) if element.number in RADIOACTIVE else QtGui.QColor(245, 245, 245)

        font_small = QtGui.QFont(self._font_family, 9)
        font_symbol = QtGui.QFont(self._font_family, 14, QtGui.QFont.Bold)
        font_name = QtGui.QFont(self._font_family, 10)

        padding = 4.0
        inner_rect = rect.adjusted(padding, padding, -padding, -padding)

        painter.save()
        painter.setClipRect(inner_rect)

        painter.setFont(font_small)
        painter.setPen(QtGui.QColor(240, 240, 240))
        top_line_height = max(font_small.pointSizeF() + 6, font_symbol.pointSizeF() + 6)
        top_line = QtCore.QRectF(inner_rect.left(), inner_rect.top(), inner_rect.width(), top_line_height)
        painter.drawText(top_line, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, number)

        painter.setFont(font_symbol)
        painter.setPen(symbol_color)
        painter.drawText(top_line, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, element.symbol)

        painter.setFont(font_name)
        painter.setPen(QtGui.QColor(240, 240, 240))
        name_line = QtCore.QRectF(
            inner_rect.left(),
            top_line.bottom(),
            inner_rect.width(),
            font_name.pointSizeF() + 8,
        )
        painter.drawText(name_line, QtCore.Qt.AlignCenter, element.name_cn)

        painter.setFont(font_small)
        tail_line_height = font_small.pointSizeF() + 6
        line3 = QtCore.QRectF(inner_rect.left(), name_line.bottom(), inner_rect.width(), tail_line_height)
        line4 = QtCore.QRectF(inner_rect.left(), line3.bottom(), inner_rect.width(), tail_line_height)
        painter.drawText(line3, QtCore.Qt.AlignCenter, "待补充")
        painter.drawText(line4, QtCore.Qt.AlignCenter, "待补充")

        painter.restore()

    def _has_metal_radical(self, name: str) -> bool:
        metal_radical_chars = {
            "锂",
            "铍",
            "钠",
            "镁",
            "铝",
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
        }
        return any(char in metal_radical_chars for char in name)

    def _grid_to_world(self, group: int, period: int) -> Tuple[float, float, float]:
        x = (group - 1) * self._x_spacing
        y = -(period - 1) * self._y_spacing
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
        if element.series in {"镧系", "锕系"}:
            y -= self._y_spacing * 0.5
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
