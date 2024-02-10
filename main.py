import sys
import requests
from io import BytesIO

from PIL import Image

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)
        self.url = "https://static-maps.yandex.ru/1.x/"
        self.map = ["map", "sat", "sat,skl"]
        self.counter = 0
        self.DELTA = 0.001
        self.LON, self.LAT = 37.279159, 55.835948
        self.show_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.DELTA /= 2
            if self.DELTA < 0.0001:
                self.DELTA = 0.0001
            self.show_image()
        elif event.key() == Qt.Key_PageDown:
            self.DELTA *= 2
            if self.DELTA > 90:
                self.DELTA = 90
            self.show_image()
        elif event.key() == Qt.Key_Left:
            self.LON -= self.DELTA
            if self.LON < -180:
                self.LON = 360 - abs(self.LON)
            self.show_image()
        elif event.key() == Qt.Key_Right:
            self.LON += self.DELTA
            if self.LON > 180:
                self.LON = -(360 - abs(self.LON))
            self.show_image()
        elif event.key() == Qt.Key_Up:
            self.LAT += self.DELTA
            if self.LAT > 90:
                self.LAT = 90
            self.show_image()
        elif event.key() == Qt.Key_Down:
            self.LAT -= self.DELTA
            if self.LAT < -90:
                self.LAT = -90
            self.show_image()
        elif event.key() == Qt.Key_Q:
            # при нажатии на Q переключается слой карты (схема/спутник/гибрид)
            self.counter += 1
            self.show_image()

    def show_image(self):
        params = {
            "ll": ",".join((str(self.LON), str(self.LAT))),
            "spn": ",".join((str(self.DELTA), str(self.DELTA))),
            "l": self.map[self.counter % 3]
        }

        response = requests.get(self.url, params)
        stream = BytesIO(response.content)

        image = Image.open(stream)

        image = image.convert("RGB")
        data = image.tobytes("raw", "RGB")
        qimage = QImage(data, image.size[0], image.size[1], QImage.Format_RGB888)

        self.pixmap = QPixmap.fromImage(qimage)
        self.img.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
