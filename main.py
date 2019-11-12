from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QColor, QIcon, QImage, QPainter, QPainterPath, QPixmap, QPen
from PyQt5.QtWidgets import QMainWindow, QWidget, QMenu, QAction, QFileDialog, QColorDialog, QInputDialog
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication, QSpinBox
from sys import argv


class Canvas(QMainWindow):
    def __init__(self, width=1000, height=1000):
        super().__init__()
        top, left = 0, 0
        self.setCursor(Qt.CrossCursor)
        self.setWindowTitle('Paint Canvas')
        self.setGeometry(left, top, width, height)
        self.setWindowIcon(QIcon('icons/paint.png'))
        self.setAttribute(Qt.WA_StaticContents)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.myPenWidth = 4
        self.myPenStyle = Qt.SolidLine
        self.myMainColor = Qt.black
        self.myBackgroundColor = Qt.white
        self.myCurrColor = self.myMainColor
        self.image.fill(self.myBackgroundColor)
        self.path = QPainterPath()
        self.prev_image = []
        self.next_image = []
        self.point = QPoint()
        self.currEvent = "pen"
        self.pattern = "point"

        self.fileMenu = self.menuBar().addMenu('File')

        self.saveAction = QAction(QIcon('icons/save.png'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.fileMenu.addAction(self.saveAction)
        self.saveAction.triggered.connect(self.save_image)

        self.openAction = QAction(QIcon('icons/open.png'), 'Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.fileMenu.addAction(self.openAction)
        self.openAction.triggered.connect(self.open_file)

        self.clearAction = QAction(QIcon('icons/clear.png'), 'Clear', self)
        self.clearAction.setShortcut('Ctrl+C')
        self.fileMenu.addAction(self.clearAction)
        self.clearAction.triggered.connect(self.clear_image)

        self.undoAction = QAction(QIcon('icons/undo.png'), 'Undo', self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.fileMenu.addAction(self.undoAction)
        self.undoAction.triggered.connect(self.undo)
        self.undoAction.setDisabled(True)

        self.redoAction = QAction(QIcon('icons/redo.png'), 'Redo', self)
        self.redoAction.setShortcut('Ctrl+Y')
        self.fileMenu.addAction(self.redoAction)
        self.redoAction.triggered.connect(self.redo)
        self.redoAction.setDisabled(True)

        self.toolMenu = self.menuBar().addMenu('Tool')

        self.pen = QAction(QIcon('icons/pen.png'), 'Pen', self)
        self.pen.setShortcut('Ctrl+1')
        self.toolMenu.addAction(self.pen)
        self.pen.triggered.connect(self.pen_tool)

        self.paintCan = QAction(QIcon('icons/paint_can.png'), 'Paint Can', self)
        self.paintCan.setShortcut('Ctrl+2')
        self.toolMenu.addAction(self.paintCan)
        self.paintCan.triggered.connect(self.paint_can_tool)

        self.colorMenu = self.menuBar().addMenu('Color')

        self.main_color_pixmap = QPixmap(10, 10)
        self.main_color_pixmap.fill(self.myMainColor)
        self.mColorAction = QAction(QIcon(self.main_color_pixmap), 'Main Color', self)
        self.colorMenu.addAction(self.mColorAction)
        self.mColorAction.triggered.connect(lambda: self.set_main_color(''))

        self.background_color_pixmap = QPixmap(10, 10)
        self.background_color_pixmap.fill(self.myBackgroundColor)
        self.bColorAction = QAction(QIcon(self.background_color_pixmap), 'Background Color', self)
        self.colorMenu.addAction(self.bColorAction)
        self.bColorAction.triggered.connect(self.set_background_color)

        self.penMenu = self.menuBar().addMenu('Pen')

        self.widthChoice = QAction(QIcon('icons/width.png'), 'Width', self)
        self.penMenu.addAction(self.widthChoice)
        self.widthChoice.triggered.connect(self.set_width)

        self.styleMenu = QMenu()
        self.styleChoice = QAction(QIcon('icons/style.png'), 'Style', self)
        self.penMenu.addAction(self.styleChoice)
        self.styleChoice.setMenu(self.styleMenu)

        self.solidLine = QAction(QIcon('icons/solid.png'), 'Solid Line', self)
        self.styleMenu.addAction(self.solidLine)
        self.solidLine.triggered.connect(self.style_solid_line)

        self.dashLine = QAction(QIcon('icons/dash.png'), 'Dash Line', self)
        self.styleMenu.addAction(self.dashLine)
        self.dashLine.triggered.connect(self.style_dash_line)

        self.dashDotLine = QAction(QIcon('icons/dash_dot.png'), 'Dash-Dot Line', self)
        self.styleMenu.addAction(self.dashDotLine)
        self.dashDotLine.triggered.connect(self.style_dash_dot_line)

        self.dotLine = QAction(QIcon('icons/dot.png'), 'Dot Line', self)
        self.styleMenu.addAction(self.dotLine)
        self.dotLine.triggered.connect(self.style_dot_line)

        self.dashDotDotLine = QAction(QIcon('icons/dash_dot_dot.png'), 'Dash-Dot-Dot Line', self)
        self.styleMenu.addAction(self.dashDotDotLine)
        self.dashDotDotLine.triggered.connect(self.style_dash_dot_dot_line)

    def clear_image(self):
        self.path = QPainterPath()
        self.image.fill(self.myBackgroundColor)
        self.update()

    def save_image(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, 'Save Image', '', 'PNG (*.png);;JPEG(*.jpg)')
        if fileName == '':
            return
        self.image.save(fileName)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, 'Save Image', '', 'PNG (*.png);;JPEG(*.jpg)')
        if fileName == '':
            return
        self.new_action()
        self.image = QImage(fileName)

    def new_image(self):
        # создание нового холста
        # x, y = self.pos().x(), self.pos().y()
        # widget = QWidget()
        # widget.setGeometry(x, y, 300, 300)
        pass

    def pen_tool(self):
        self.currEvent = "pen"

    def paint_can_tool(self):
        self.currEvent = "fill"

    def text_tool(self):
        self.currEvent = "text"

    def pattern_tool(self):
        self.currEvent = "pattern"

    def new_action(self):
        self.prev_image.append(self.image.copy())
        self.undoAction.setEnabled(True)
        self.redoAction.setDisabled(True)
        self.path = QPainterPath()

    def undo(self):
        self.path = QPainterPath()
        self.next_image.append(self.image.copy())
        self.redoAction.setEnabled(True)
        self.image = self.prev_image.pop()
        self.update()
        if len(self.prev_image) == 0:
            self.undoAction.setDisabled(True)

    def redo(self):
        self.path = QPainterPath()
        self.prev_image.append(self.image.copy())
        self.undoAction.setEnabled(True)
        self.image = self.next_image.pop()
        if len(self.next_image) == 0:
            self.redoAction.setDisabled(True)
        self.update()

    def set_main_color(self, color_str=''):
        if color_str == '':
            color = QColorDialog.getColor()
        else:
            print(color_str)
            color = QColor(color_str)
        if color.isValid():
            self.myMainColor = QColor(color)
            self.main_color_pixmap.fill(self.myMainColor)
            self.mColorAction.setIcon(QIcon(self.main_color_pixmap))

    def set_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.myBackgroundColor = QColor(color)
            self.background_color_pixmap.fill(self.myBackgroundColor)
            self.bColorAction.setIcon(QIcon(self.background_color_pixmap))

    def set_width(self):
        newWidth, _ = QInputDialog.getInt(
            self, "Введите толщину линии", "Толщина линии", self.myPenWidth, 1, 2000)
        self.myPenWidth = newWidth
        self.path = QPainterPath()

    def style_solid_line(self):
        self.myPenStyle = Qt.SolidLine

    def style_dash_line(self):
        self.myPenStyle = Qt.DashLine

    def style_dash_dot_line(self):
        self.myPenStyle = Qt.DashDotLine

    def style_dot_line(self):
        self.myPenStyle = Qt.DotLine

    def style_dash_dot_dot_line(self):
        self.myPenStyle = Qt.DashDotDotLine

    def fill_color(self, event):
        def get_cardinal_points(center_pos):
            cardinal_points = []
            cx, cy = center_pos
            for x0, y0 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x0, cy + y0
                if (xx >= 0 and xx < w and yy >= 0 and yy < h and (xx, yy) not in have_seen):
                    cardinal_points.append((xx, yy))
                    have_seen.add((xx, yy))
            return cardinal_points

        x, y = event.x(), event.y()
        w, h = self.image.width(), self.image.height()

        target_color = self.image.pixel(x, y)

        painter = QPainter(self.image)
        painter.setPen(QPen(self.currColor))
        have_seen = set()
        queue = [(x, y)]
        while queue:
            x, y = queue.pop()
            if self.image.pixel(x, y) == target_color:
                painter.drawPoint(QPoint(x, y))
                points = get_cardinal_points((x, y))
                queue.extend(points)
        self.update()

    def draw_text(self, text):
        # font = QFont(self.fontComboBox.currentFont())
        # font.setPointSizeF(self.sizeSpinBox.value())
        # metrics = QFontMetricsF(font)
        #
        # if not text:
        #     return
        # rect = metrics.boundingRect(text)
        # position = -rect.topLeft()
        #
        # pixmap = QPixmap(rect.width(), rect.height())
        # pixmap.fill(Qt.white)
        #
        # painter = QPainter()
        # painter.begin(pixmap)
        # painter.setFont(font)
        # painter.drawText(position, text)
        # painter.end()
        #
        # self.label.setPixmap(pixmap)
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        self.new_action()
        if self.currEvent == "pattern":
            if self.pattern == "polygon begin":
                self.point = event.pos()
                self.path.moveTo(event.pos())
            elif self.pattern == "polygon":
                pass
        self.path.moveTo(event.pos())
        if event.button() == Qt.LeftButton:
            self.currColor = self.myMainColor
        elif event.button() == Qt.RightButton:
            self.currColor = self.myBackgroundColor
        if self.currEvent == "fill":
            self.fill_color(event)

    def mouseMoveEvent(self, event):
        if self.currEvent == "pen":
            self.path.lineTo(event.pos())
            painter = QPainter(self.image)
            painter.setPen(QPen(self.currColor, self.myPenWidth,
                                self.myPenStyle, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(self.path)
            painter.end()
        else:
            return
        self.update()

    def sizeHint(self):
        return self.image.size()

    def get_menu(self):
        return self.fileMenu, self.toolMenu, self.colorMenu, self.penMenu


# используется только первая палитра
COLORS = [
    ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3',
     '#8fd970', '#5ebb49', '#458352', '#dcd37b', '#fffee5',
     '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a',
     '#c24998', '#81588d', '#bcb0c2', '#ffffff'],
    ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598",
     "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f",
     "#9e0142"],
    ["#a63603", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2",
     "#feedde"],
    ["#49006a", "#7a0177", "#ae017e", "#dd3497", "#f768a1",
     "#fa9fb5", "#fcc5c0", "#fde0dd", "#fff7f3"]
]


class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Paint Application')
        self.setWindowIcon(QIcon('icons/paint.png'))
        self.setGeometry(600, 150, 1020, 510)

        self.canvas = Canvas(1000, 500)
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self.canvas)

        for menu in self.canvas.get_menu():
            self.menuBar().addMenu(menu)
        self.canvas.menuBar().hide()

        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        layout.addLayout(palette)
        spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        layout.addItem(spacer)

        self.setCentralWidget(widget)

    def add_palette_buttons(self, layout, i=0):
        for color in COLORS[i]:
            btn = QPaletteButton(color)
            btn.pressed.connect(lambda c=color: self.canvas.set_main_color(c))
            layout.addWidget(btn)
        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)


app = QApplication(argv)
window = MainWindow()
window.show()
app.exec_()
