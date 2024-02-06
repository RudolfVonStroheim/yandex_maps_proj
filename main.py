import sys
import requests
from io import BytesIO

from PIL import Image

from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)
        self.url = "https://static-maps.yandex.ru/1.x/"
        self.DELTA = 0.002
        self.LON, self.LAT = 37.279159, 55.835948
        self.show_image()

    def show_image(self):
        params = {
            "ll": ",".join((str(self.LON), str(self.LAT))),
            "spn": ",".join((str(self.DELTA), str(self.DELTA))),
            "l": "map"
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