import sys, json, os

from PyQt6 import QtWidgets
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtCore import Qt, QRect, QPoint

# import settings
with open(os.path.join(os.getcwd(), "theme.json"),'r') as f:
    jsontheme = json.load(f)

class theme:
    begraund_color = jsontheme.get("begraund_color", "auto")
    text_color = jsontheme.get("text_color", "#CCCBCB")
    point_color = jsontheme.get("point_color", "#4c82f7")
    colonium_color = jsontheme.get("colonium_color", "#4c82f7")
    graph_edging_color = jsontheme.get("graph_edging_color", "#000001")
    line_color = jsontheme.get("line_color", "#1a1a1a")

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
            
            self.data = sorted(self.data, key=lambda itm: itm[1], reverse=True)

            num = []
            for point in self.data:
                num.append(point[1])
            
            l_str_len = []
            for strs in self.data:
                l_str_len.append(len(strs[0]))
            
            max_str_len = max(l_str_len)
            
            if len(num)>10:
                self.font_px = 10

            position={}
            indent_y = fm.height()
            indent_x = self.area_x + fm.horizontalAdvance(" "*(max_str_len+1))
            index = 0
            
            for i in num:
                symbol_y = self.area_y + indent_y
                indent_y += round(self.area_size // len(num))

                indent_x -= fm.horizontalAdvance(self.data[index][0]) + fm.horizontalAdvance(" ") * round((max_str_len - len(self.data[index][0]))/2)

                painter.drawText(self.area_x - fm.horizontalAdvance(str(self.data[index][1])), symbol_y, str(i))
                position[index] = (indent_x , symbol_y)
                index += 1


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

                painter.drawEllipse(QPoint(self.area_x + position[inx][0], position[inx][1] - round(fm.height() / 2 + point_size/2)), point_size, point_size)
                painter.drawText(self.area_x + position[inx][0] - round((fm2.horizontalAdvance(self.data[inx][0])+5) / 2), podpis_y + fm2.height() , self.data[inx][0])
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())
