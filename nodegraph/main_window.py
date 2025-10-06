from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGraphicsItem,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import Qt, QRectF, QSize, QPoint
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QMouseEvent, QCursor
from nodegraph.infinite_scroller import InfiniteScroller


class NodeGraphicsScene(QGraphicsScene):
    def add_rect_item(self, x: int, y: int, width: int, height: int):
        rect_item = QGraphicsRectItem(0, 0, width, height)
        rect_item.setPen(QPen(Qt.GlobalColor.blue))
        # semi-transparent shallow blue
        rect_item.setBrush(QBrush(QColor(173, 216, 230, 100)))
        rect_item.setPos(x, y)
        self.addItem(rect_item)
        self._adjust_scene_rect()
        return rect_item

    def _adjust_scene_rect(self):
        scene_rect = self.sceneRect()
        total_rect = self.itemsBoundingRect()
        VERTICAL_ADJUST_VALUE = 30
        HORIZONTAL_ADJUST_VALUE = 100
        if total_rect.left() < scene_rect.left():
            scene_rect.adjust(-HORIZONTAL_ADJUST_VALUE, 0, 0, 0)
        if total_rect.right() > scene_rect.right():
            scene_rect.adjust(0, 0, HORIZONTAL_ADJUST_VALUE, 0)
        if total_rect.top() < scene_rect.top():
            scene_rect.adjust(0, -VERTICAL_ADJUST_VALUE, 0, 0)
        if total_rect.bottom() > scene_rect.bottom():
            scene_rect.adjust(0, 0, 0, VERTICAL_ADJUST_VALUE)
        self.setSceneRect(scene_rect)


class NodeGraphiscView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        # self.setSceneRect = lambda rect: None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inf_scroller = None

    def drawBackground(self, painter, rect):
        scene_rect = self.scene().sceneRect()
        # painter.fillRect(rect, QColor(60, 60, 60))
        # painter.fillRect(scene_rect, Qt.GlobalColor.white)
        painter.fillRect(rect, Qt.GlobalColor.white)

        painter.setPen(QColor(233, 233, 233))

        CELL_SIZE = 10
        for i in range(0, int(scene_rect.width() / CELL_SIZE)):
            painter.drawLine(i * CELL_SIZE, 0, i * CELL_SIZE, int(scene_rect.height()))

        for i in range(0, int(scene_rect.height() / CELL_SIZE)):
            painter.drawLine(0, i * CELL_SIZE, int(scene_rect.width()), i * CELL_SIZE)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # scene_pos = self.mapToScene(event.pos())
            # scene = self.scene()
            # scene.add_rect_item(scene_pos, 20, 10)
            # super().mousePressEvent(event)
            pass
        elif event.button() == Qt.MouseButton.MiddleButton:
            r = self.viewport().rect()
            if self.inf_scroller is None:
                self.inf_scroller = InfiniteScroller()
            self.inf_scroller.set_region(r.left(), r.right(), r.top(), r.bottom())
            self.inf_scroller.cursor_callback = lambda x, y: QCursor.setPos(
                self.mapToGlobal(QPoint(x, y))
            )
            self.inf_scroller.horizontal_callback = self._update_horizotal_scroll_bar
            self.inf_scroller.vertical_callback = self._update_vertical_scroll_bar
            self.inf_scroller.start(event.pos().x(), event.pos().y())
            self.setCursor(Qt.CursorShape.SizeAllCursor)

    def mouseMoveEvent(self, event):
        if self.inf_scroller is not None:
            self.inf_scroller.solve(event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pass
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.inf_scroller.end()
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _update_horizotal_scroll_bar(self, value):
        h = self.horizontalScrollBar()
        h.setValue(h.value() - value)

    def _update_vertical_scroll_bar(self, value):
        v = self.verticalScrollBar()
        v.setValue(v.value() - value)


class InfoWidget(QWidget):
    HORIZONTAL_SPACE = 20
    VERTICAL_SPACE = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self._row = 0
        self._col = 0
        self._node_count = 0

    def initUI(self):
        self.setWindowTitle("My node graph")

        layout = QVBoxLayout(self)

        self.scene = NodeGraphicsScene()
        width = 500
        height = 100
        self.scene.setSceneRect(0, 0, width, height)
        self.view = NodeGraphiscView(self.scene)

        # self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        layout.addWidget(self.view)

        txt_edit = QTextEdit()
        layout.addWidget(txt_edit)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        btn_new_to_down = QPushButton("New to down")
        btn_new_to_down.clicked.connect(self.add_node_to_down)
        h_layout.addWidget(btn_new_to_down)

        btn_new_to_right = QPushButton("New to right")
        btn_new_to_right.clicked.connect(self.add_node_to_right)
        h_layout.addWidget(btn_new_to_right)

    def add_node_to_down(self):
        print("add_node_to_down, row={}".format(self._row))
        if self._node_count == 0:
            self._add_node()
        else:
            self._row += 1
            self._add_node()

    def add_node_to_right(self):
        print("add_node_to_right, col={}".format(self._col))
        if self._node_count == 0:
            self._add_node()
        else:
            self._col += 1
            self._add_node()

    def _add_node(self):
        NODE_WIDTH = 100  # TODO: should be dynamic
        NODE_HEIGHT = 20  # TODO: should be dynamic
        x = (
            InfoWidget.HORIZONTAL_SPACE
            + (NODE_WIDTH + InfoWidget.HORIZONTAL_SPACE) * self._col
        )
        y = (
            InfoWidget.VERTICAL_SPACE
            + (NODE_HEIGHT + InfoWidget.VERTICAL_SPACE) * self._row
        )
        item = self.scene.add_rect_item(x, y, NODE_WIDTH, NODE_HEIGHT)
        self._node_count += 1
        # TODO: need to center on the new added node
        self.view.centerOn(item)
