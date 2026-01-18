import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QMouseEvent, QPixmap
import cv2
from PIL import Image

def digitRecognizer():
    pass

def scaleImageDown():
    digitImage = cv2.imread("digitImage.png")
    newHeight = 28
    newWidth = 28
    
    resizedImage = cv2.resize(digitImage, (newWidth, newHeight), interpolation=cv2.INTER_AREA)
    cv2.imwrite(filename="scaledDown.png", img=resizedImage)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.canvas = QtGui.QPixmap(728, 728)
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)
        self.leftClick = False
        self.mlVisionPixmap = QPixmap("scaledDown.png")
        self.mlVisionLabel = QLabel(self)
        self.mlVisionLabel.setPixmap(self.mlVisionPixmap)
        self.probabilityLabel = QLabel("Probability:", self)
        self.clearButton = QPushButton("Clear Drawing", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 210, 1128, 728) #Drawing is 728x728p
        self.setFixedSize(1128, 728)
        self.label.setGeometry(10, 0, 0, 0)
        self.setStyleSheet("background-color: #696969")
        self.label.setFixedSize(self.canvas.width(), self.canvas.height())
        self.label.setStyleSheet("border-style: 10px solid black;")
        self.mlVisionLabel.setScaledContents(True)
        self.mlVisionLabel.setGeometry(928, 10, 100, 100)
        self.probabilityLabel.setGeometry(768, 120, 320, 608)
        self.probabilityLabel.setStyleSheet("background-color: #7dbbff; font-size: 20px; font-family: Arial;")
        self.clearButton.setStyleSheet("font-family: Arial; font-size: 20px;")
        self.clearButton.setGeometry(768, 10, 150, 100)
        self.clearButton.pressed.connect(self.clearButtonPress)
        

    def mouseMoveEvent(self, event): #Draws on canvas if lc is clicked and inside of canvas
        if self.leftClick:
            if event.x() <= 728 and event.y() <= 728:
                print(f"X: {event.x()}; Y: {event.y()}")
                self.painter = QPainter(self.canvas)
                self.pen = QPen()
                self.pen.setWidth(30)
                self.painter.setPen(self.pen)
                self.painter.drawPoint(event.x(), event.y())
                self.label.setPixmap(self.canvas)
                self.update()
    
    def mouseReleaseEvent(self, event): #Detects when lc is released
        if event.button() == Qt.LeftButton:
            self.leftClick = False
            self.canvas.save("digitImage.png", "PNG", -1)
            scaleImageDown()
            self.mlVisionPixmap = QPixmap("scaledDown.png")
            self.mlVisionLabel.setPixmap(self.mlVisionPixmap)
            digitRecognizer() #Get the ML to recognnize the drawn number

    def mousePressEvent(self, event): #Detects when lc is pressed
        if event.button() == Qt.LeftButton:
            self.leftClick = True

    def clearButtonPress(self): #Clears the drawing
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.canvas.save("digitImage.png", "PNG", -1)
        self.mlVisionPixmap = QPixmap("digitImage.png")
        self.mlVisionLabel.setPixmap(self.mlVisionPixmap)
        
        print("Cleared Drawing")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    