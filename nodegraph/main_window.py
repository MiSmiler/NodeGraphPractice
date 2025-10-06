from PyQt6.QtWidgets import (QMainWindow, QGraphicsView,
                             QGraphicsScene, QGraphicsRectItem, QVBoxLayout, QWidget, QGraphicsItem)
from PyQt6.QtCore import Qt, QRectF, QSize, QPoint
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QMouseEvent, QCursor
from nodegraph.infinite_scroller import InfiniteScroller


class NodeGraphicsScene(QGraphicsScene):
    def adjust_scene_rect(self):
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

    def add_rect_item(self, pos, width, height):
        rect_item = QGraphicsRectItem(0, 0, width, height)
        rect_item.setPen(QPen(Qt.GlobalColor.blue))
        # semi-transparent shallow blue
        rect_item.setBrush(QBrush(QColor(173, 216, 230, 100)))
        rect_item.setPos(pos)
        self.addItem(rect_item)
        self.adjust_scene_rect()


class NodeGraphiscView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        # self.setSceneRect = lambda rect: None
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inf_scroller = None

    def drawBackground(self, painter, rect):
        scene_rect = self.scene().sceneRect()
        painter.fillRect(rect, QColor(60, 60, 60))
        painter.fillRect(scene_rect, Qt.GlobalColor.white)

        painter.setPen(QColor(233, 233, 233))
        painter.drawLine(int(scene_rect.left()), 0, int(scene_rect.right()), 0)
        painter.drawLine(0, int(scene_rect.top()), 0, int(scene_rect.bottom()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            scene = self.scene()
            scene.add_rect_item(scene_pos, 20, 10)
            super().mousePressEvent(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            r = self.viewport().rect()
            self.inf_scroller = InfiniteScroller()
            self.inf_scroller.set_region(
                r.left(), r.right(), r.top(), r.bottom())
            self.inf_scroller.cursor_callback = lambda x, y: QCursor.setPos(
                self.mapToGlobal(QPoint(x, y)))
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My node graph")
        # self.setGeometry(-1, -1, 800, 600)
        # self.setBaseSize(400, 300)
        # self.setFixedSize(800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建图形场景和视图
        self.scene = NodeGraphicsScene()
        width = 500
        height = 100
        self.scene.setSceneRect(-width/2, -height/2, width, height)
        self.view = NodeGraphiscView(self.scene)

        # 设置视图属性
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
        # self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # 拖拽模式

        # 将视图添加到布局
        layout.addWidget(self.view)
