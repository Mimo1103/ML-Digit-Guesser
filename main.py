import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon
import cv2
import numpy as np
import tensorflow as tf


def createProbabilityText(prediction):
    
    infoPrediction = prediction[0]
    infoPrediction = [("0", infoPrediction[0]),
                        ("1", infoPrediction[1]),
                        ("2", infoPrediction[2]),
                        ("3", infoPrediction[3]),
                        ("4", infoPrediction[4]),
                        ("5", infoPrediction[5]),
                        ("6", infoPrediction[6]),
                        ("7", infoPrediction[7]),
                        ("8", infoPrediction[8]),
                        ("9", infoPrediction[9]),
                    ]
    infoPrediction.sort(key=lambda x: x[1], reverse=True)

    probabilityText = f"""
                        {infoPrediction[0][0]}: {infoPrediction[0][1]:.8f}\n
                        {infoPrediction[1][0]}: {infoPrediction[1][1]:.8f}\n
                        {infoPrediction[2][0]}: {infoPrediction[2][1]:.8f}\n
                        {infoPrediction[3][0]}: {infoPrediction[3][1]:.8f}\n
                        {infoPrediction[4][0]}: {infoPrediction[4][1]:.8f}\n
                        {infoPrediction[5][0]}: {infoPrediction[5][1]:.8f}\n
                        {infoPrediction[6][0]}: {infoPrediction[6][1]:.8f}\n
                        {infoPrediction[7][0]}: {infoPrediction[7][1]:.8f}\n
                        {infoPrediction[8][0]}: {infoPrediction[8][1]:.8f}\n
                        {infoPrediction[9][0]}: {infoPrediction[9][1]:.8f}\n
                    """
    
    window.probabilityLabel.setText(f"Probability: {probabilityText}")
 
def digitRecognizer(needTraining: bool, needreset=False):
    modelName = "DigitRecognizerNN"

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data() #Set up the training data
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    if needTraining:
        print("Starting training")
        if needreset:
            model = tf.keras.models.Sequential() #Creating the model
            model.add(tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28))), #layer 1
            model.add(tf.keras.layers.Conv2D(32, (3, 3,), activation="relu")), #layer 2
            model.add(tf.keras.layers.MaxPooling2D((2, 2))),
            model.add(tf.keras.layers.Conv2D(64, (3, 3,), activation="relu")), #layer 3
            model.add(tf.keras.layers.MaxPooling2D((2, 2))),

            model.add(tf.keras.layers.Flatten()), #layer 4
            model.add(tf.keras.layers.Dense(128, activation="relu")), #layer 5
            model.add(tf.keras.layers.Dense(10, activation="softmax")), #layer 6 / output layer


            model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]) #How to train the model
            model.fit(x_train, y_train, epochs=3) #Train the model

            model.save(modelName) #Saves the model under a certain name
            print("Training finished, saved model")

            print("Evaluating:")
            loss, accuracy = model.evaluate(x_test, y_test) #Evaluate the model and print Loss and Accuracy
            print(f"Loss: {loss:.4f}")
            print(f"Accuracy: {accuracy:.4f}")
        else:
            model = tf.keras.models.load_model(modelName)
            for layer in model.layers[:-2]:
                layer.trainable = False

                train_ds = tf.keras.utils.image_dataset_from_directory(
                    "customFineTuningData",
                    labels="inferred",
                    label_mode="int",
                    color_mode="grayscale",
                    image_size=(28, 28),
                    batch_size=(8),
                    shuffle=True
                    )
                
                train_ds = train_ds.map(lambda x, y: (tf.cast(x, tf.float32) / 255.0, y))
                model.compile(
                    optimizer = tf.keras.optimizers.Adam(learning_rate=2.7e-5),
                    loss="sparse_categorical_crossentropy",
                    metrics=["accuracy"]
                )
                model.fit(train_ds, epochs=3)
                model.save(modelName)
    else:
        model = tf.keras.models.load_model(modelName) #Loads the model under a certain name
        print("Loading model")

        try:
            paddedImg = cv2.imread("scaledDown.png", cv2.IMREAD_GRAYSCALE)
            downScaleImg = paddedImg.reshape(1, 28, 28, 1).astype(np.float32) / 255.0
            prediction = model.predict(downScaleImg)
            clonePredi = list(prediction)
            createProbabilityText(clonePredi)
            print(f"Possibility: {np.argmax(prediction)}")
        except:
            print("An error occured :(")

def scaleImageDown():

    img = cv2.imread("digitImage.png", cv2.IMREAD_GRAYSCALE) #Converts image to grayscale
    img = cv2.bitwise_not(img) #Inverts colors
    _, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY) #Removes gray pixels (<50 white, >50 black)
    coords = cv2.findNonZero(img)
    x, y, w, h = cv2.boundingRect(coords) #Creates rectangle around digit
    cropImg = img[y:y+h, x:x+w] #Crops image
    cropImg = cv2.resize(cropImg, (20, 20), interpolation=cv2.INTER_AREA) #Resize to 20x20px
    paddedImg = np.pad(cropImg, ((4, 4), (4, 4)), "constant", constant_values=0) #Adds 4px border around image

    cv2.imwrite(filename="scaledDown.png", img=paddedImg) #und keine hundertfachen Matrizen multiplikationen hintereinander mit verschiedenen Größen

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
        self.probabilityLabel = QLabel("Draw on the whitespace on the left to see the probabilities", self)
        self.clearButton = QPushButton("Clear Drawing", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 210, 1128, 728) #Drawing is 728x728p
        self.setFixedSize(1128, 728)
        self.setWindowIcon(QIcon("customFineTuningData/2/1768832431.0503693.png"))
        self.label.setGeometry(10, 0, 0, 0)
        self.setStyleSheet("background-color: #cfcfcf")
        self.label.setFixedSize(self.canvas.width(), self.canvas.height())
        self.label.setStyleSheet("border-style: 10px solid black;")
        self.mlVisionLabel.setScaledContents(True)
        self.mlVisionLabel.setGeometry(928, 10, 100, 100)
        self.probabilityLabel.setGeometry(768, 120, 320, 608)
        self.probabilityLabel.setStyleSheet("background-color: #cfcfcf; font-size: 20px; font-family: Arial; border: 4px #a3a3a3; border-style: dashed;")
        self.probabilityLabel.setWordWrap(True)
        self.clearButton.setStyleSheet("font-family: Arial; font-size: 20px; border: 4px #5e5e5e; border-style: dashed;") 
        self.clearButton.setGeometry(768, 10, 150, 100)
        self.clearButton.pressed.connect(self.clearButtonPress) 

    def mouseMoveEvent(self, event): #Draws on canvas if lc is clicked and inside of canvas
        if self.leftClick:
            if event.x() <= 728 and event.y() <= 728:
                self.painter = QPainter(self.canvas)
                self.pen = QPen()
                self.pen.setWidth(60)
                self.painter.setPen(self.pen)
                self.painter.drawPoint(event.x(), event.y())
                self.label.setPixmap(self.canvas)
                self.update()
    
    def mouseReleaseEvent(self, event): #Detects when lc is released
        if event.button() == Qt.LeftButton:
            if event.x() <= 728 and event.y() <= 728:
                self.leftClick = False
                self.canvas.save("digitImage.png", "PNG", -1)
                scaleImageDown()
                self.mlVisionPixmap = QPixmap("scaledDown.png")
                self.mlVisionLabel.setPixmap(self.mlVisionPixmap)
                digitRecognizer(needTraining=False) #Get the CNN to recognnize the drawn number

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
    print("Main is running")

if __name__ == "__main__":
    main()
    

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())