from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from Application.Misc.other import deleteLayout, calculate_lines
from Application.Misc.thread import DatabaseThread
from Application.stylesheets.stylesheet import secondaryStyleSheet
from dictionary import Dictionary

from Application.Misc.dotenv_manager import DotEnv

data = DotEnv()

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
        self.setStyleSheet(secondaryStyleSheet)
        self.getThread, self.getThread2 = None, None
        self.oldPostition = QPoint()
        self.mainLayout = QGridLayout()
        self.dictionary = Dictionary()
        self.setLayout(self.mainLayout)

        self.getThread = DatabaseThread(data.get("DPWloadDictionary"), self.__init_dict)
        self.getThread2 = DatabaseThread(data.get("DPWloadData"), self.__content)

    def loadData(self):
        self.getThread.run()
        self.getThread2.run()

    def __init_dict(self, items):
        self.dictionary.clear()
        for image_id, url in items:
            self.dictionary.add_item(image_id, url.rsplit("/", 1)[1])

    def __content(self, items):
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
                        pixmap.loadFromData(self.__open_image(PATH + self.dictionary[item.imid]))
                    except (KeyError, FileNotFoundError):
                        pixmap.loadFromData(self.__open_image(PATH + "Unknown_Image.jpg"))

                    label = QLabel()

                    scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
                    label.setPixmap(scaled_pixmap)
                    layout.addWidget(label, 0, 0, 1, 2)
                    layout.addWidget(QLabel(item.name), 1, 0, 1, 2)
                    layout.addWidget(QLabel(item.amount), 2, 1)
                    layout.addWidget(QLabel(item.price), 2, 0)
                    self.mainLayout.addLayout(layout, x, y)

    @staticmethod
    def __open_image(image):
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

    def show(self) -> None:
        super(DisplayProductsWindow, self).show()
        self.loadData()
