import sys
sys.path.append(".")
import os
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets, QtGui
from recognize_panel import recognize


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        self.setWindowTitle("Mnist 手写数字识别")
        self.pix = QPixmap()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.initUi()
 
    def initUi(self):
        self.setFixedSize(600, 500)
 
        self.pix = QPixmap(500, 500)
        self.pix.fill(Qt.black)
 
        self.offset = QPoint(self.width() - self.pix.width(), self.height() - self.pix.height())
 
        btn_clear = QPushButton(self)
        btn_clear.setText("清空")
        btn_clear.resize(80, 30)
        btn_clear.move(10, 30)
        btn_clear.clicked.connect(self.clear)
 
        btn_save = QPushButton(self)
        btn_save.setText("识别")
        btn_save.resize(80, 30)
        btn_save.move(10, 80)
        btn_save.clicked.connect(self.recognize)
 
        label = QLabel(self)
        label.setText(" 识别结果：")
        label.resize(80, 30)
        label.move(10, 130)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.resize(80, 30)
        self.lineEdit.move(10, 180)

 
    def clear(self):
        self.pix.fill(Qt.black)
        self.update()
    
    def recognize(self):
        self.pix.save("./recognize_panel/data/digit.png")
        result = recognize.recognize("./recognize_panel/data/digit.png")
        self.lineEdit.setText(str(result))
  
 
    def paintEvent(self, event):
        pp = QPainter(self.pix)
        pen = QPen(Qt.white, 30, Qt.SolidLine, cap = Qt.RoundCap)
        pp.setPen(pen)
        pp.drawLine(self.lastPoint, self.endPoint)
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(100, 0, self.pix)
 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos() - self.offset
            self.endPoint = self.lastPoint
            # print(self.endPoint)
 
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            self.update()
 
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            self.update()
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()
    sys.exit(app.exec_())