import os

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from Application.Misc.other import Label, deleteLayout, calculate_lines
from Application.Misc.thread import Thread
from dictionary import Dictionary
from download_images import threaded_downloading
from json_manager import Json

# TODO: settings reset image cache

data = Json().read()["displayProductsWindow"]
PATH = "Assets//Products//"
width = 5


class Item:
    def __init__(self, name: str, amount: str, price: str, imid: int):
        self.name = name
        self.amount = amount
        self.price = price
        self.imid = imid


class DisplayProductsWindow(QWidget):
    def __init__(self):
        super(DisplayProductsWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPostition = QPoint()
        self.mainLayout = QGridLayout()
        self.dictionary = Dictionary()
        self.setLayout(self.mainLayout)
        self.downloadImages()

    def loadData(self):
        Thread(data["loadDictionary"], self.init_dict).run()
        Thread(data["loadData"], self.content).run()

    def init_dict(self, items):
        self.dictionary.clear()
        for image_id, url in items:
            self.dictionary.add_item(image_id, url.rsplit("/", 1)[1])

    def content(self, items):
        deleteLayout(self.mainLayout)

        pixmap = QPixmap()

        items_number = len(items)
        number_of_lines = calculate_lines(items_number, width)

        for x in range(number_of_lines):
            for y in range(width):
                if items_number > 0:
                    items_number -= 1
                    layout = QGridLayout()
                    item = Item(*items[x * width + y])
                    try:
                        pixmap.loadFromData(self.open_image(PATH + self.dictionary[item.imid]))
                    except FileNotFoundError:
                        pixmap.loadFromData(self.open_image(PATH + "Unknown_Image.jpg"))

                    label = Label(alignment=Qt.AlignCenter)

                    scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
                    label.setPixmap(scaled_pixmap)
                    layout.addWidget(label, 0, 0, 1, 2)
                    layout.addWidget(Label(item.name, font_size=10, alignment=Qt.AlignCenter), 1, 0, 1, 2)
                    layout.addWidget(Label(item.amount), 2, 1)
                    layout.addWidget(Label(item.price, alignment=Qt.AlignRight), 2, 0)
                    self.mainLayout.addLayout(layout, x, y)

    def open_image(self, image):
        with open(image, "rb") as f:
            return f.read()

    def mousePressEvent(self, event):
        self.oldPostition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPostition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPostition = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.update()

    def downloadImages(self):
        if len(os.listdir("Assets//Products//")) == 1:
            Thread(data["loadDictionary"], self.initImages).run()

    def initImages(self, items):
        threaded_downloading([url for _, url in items])

    def show(self) -> None:
        super(DisplayProductsWindow, self).show()
        self.loadData()