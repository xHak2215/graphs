import sys, json, os

from PyQt6 import QtWidgets
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtCore import Qt, QRect, QPoint

# import settings
with open(os.path.join(os.getcwd(), "theme.json"),'r') as f:
    jsontheme = json.load(f)

class theme:
    begraund_color = jsontheme["begraund_color"]
    text_color = jsontheme["text_color"]
    point_color = jsontheme["point_color"]
    colonium_color = jsontheme["colonium_color"]
    graph_edging_color = jsontheme["graph_edging_color"]
    line_color = jsontheme["line_color"]

class Main(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("graph")
        self.setGeometry(100, 100, 800, 600)

        if theme.begraund_color != "auto":
            self.setStyleSheet(f"background-color: {theme.begraund_color};")
        
        self.button = QtWidgets.QPushButton("построить график", self)
        self.button.move(20, 550)

        self.open_file = QtWidgets.QPushButton("открыть файл", self)
        self.open_file.move(20, 40)

        #self.textbox = QtWidgets.QLineEdit(self)
        #self.textbox.move(20, 60)
        #self.textbox.resize(170, 40)

        # параметры области рисования — как атрибуты
        self.area_size = 450
        self.area_x = self.width() - self.area_size - 25
        self.area_y = (self.height() - self.area_size) // 2
        self.font_px = 15

        self.file = None
        self.data = None

        if self.file:
            with open(self.file, "r") as f:
                datas = json.load(f)
            
            self.title = datas["title"]
            self.visuale_type = datas["visuale_type"]
            self.data = datas["elements"]


        self.button.clicked.connect(self.on_click)
        self.open_file.clicked.connect(self.get_file_dialog)

    def on_click(self):
        #text = self.textbox.text()
        #print("Input:", text)
        # пример: добавляем точку вправо при каждом клике
        #new_x = self.area_x + 20 + len(self.points) * 20
        #new_y = self.area_y + self.area_size // 2
        #self.points.append((new_x, new_y))
        #self.update()

        if self.file:
            with open(self.file, "r") as f:
                datas = json.load(f)
        
            self.title = datas["title"]
            self.visuale_type = datas["visuale_type"]
            self.data = datas["elements"]
            self.update()

    def get_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'All Files (*)'
        )
        self.file = file_name
        print(file_name, _)
        return file_name

    def paintEvent(self, event)->None:
        if self.file and self.data:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # рамка области графика
            pen = QPen(QColor(theme.graph_edging_color))
            pen.setWidth(2)
            painter.setPen(pen)
            rect = QRect(self.area_x, self.area_y, self.area_size, self.area_size)
            painter.drawRect(rect)

            painter.setPen(QColor(theme.text_color))
            painter.setFont(QFont("Arial", self.font_px))
            fm = painter.fontMetrics()

            # полоска у низа области
            podpis_y = self.area_y + self.area_size - fm.height()+1
            painter.fillRect(QRect(self.area_x, podpis_y, self.area_size, 5), QColor(theme.line_color))

            max_num = []
            for point in self.data:
                max_num.append(point[1])
            max_num = max(max_num)
            
            if max_num > 38:
                self.font_px = 10

            position=[]
            otstup = fm.height()
            for i in range(1, max_num+1):
                symbol_y = self.area_y + otstup
                otstup += round(self.area_size // max_num)

                painter.drawText(self.area_x - fm.horizontalAdvance(str(i)) - 2, symbol_y, str(i))
                position.append((self.area_x - fm.horizontalAdvance(str(i)) - 2, symbol_y))

            painter.drawText(self.area_x + round(self.area_size / 2 - (fm.horizontalAdvance(self.title)/2)), self.area_y - round(fm.height()/2), self.title)

            # рисуем точки
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(theme.point_color))

            painter.setPen(QColor(theme.text_color))
            painter.setFont(QFont("Arial", round((self.font_px/100)*85)))
            fm2 = painter.fontMetrics()

            px = self.area_x + fm.horizontalAdvance("  ")
            point_size = 6
            for inx in range(len(self.data)):
                if self.data[inx][1] > 0:
                    promeshutok = round(self.area_size / self.data[inx][1])
                else:
                    promeshutok = fm2.horizontalAdvance(self.data[inx][0])+5
                px += promeshutok

                painter.drawEllipse(QPoint(px, position[self.data[inx][1] - 1][1] - round(fm.height() / 2) + round(point_size/2)), point_size, point_size)
                painter.drawText(px - round(fm2.horizontalAdvance(self.data[inx][0])/2), podpis_y + fm2.height(), self.data[inx][0])
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())
