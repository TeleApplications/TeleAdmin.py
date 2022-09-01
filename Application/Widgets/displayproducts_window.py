from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFrame

from Application.Misc.other import deleteLayout, calculate_lines
from Application.Misc.thread import DatabaseThread
from Application.stylesheets.stylesheet import secondaryStyleSheet
from dictionary import Dictionary

from Application.Misc.dotenv_manager import DotEnv

data = DotEnv()

PATH = "Assets//Products//"
width = 7


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
        self.timer = QTimer()
        self.timer.start(10000)


        self.timer.timeout.connect(self.loadData)
        self.setLayout(self.mainLayout)

    def loadData(self):

        self.getThread = DatabaseThread(data.get("DPWloadDictionary"), self.__init_dict)
        self.getThread2 = DatabaseThread(data.get("DPWloadData"), self.__content)
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
                    frame = QFrame()
                    frame.setObjectName("frame")
                    layout = QGridLayout()

                    item = Item(*items[x * width + y])
                    try:
                        pixmap.loadFromData(self.__open_image(PATH + self.dictionary[item.imid]))
                    except (KeyError, FileNotFoundError):
                        pixmap.loadFromData(self.__open_image(PATH + "Unknown_Image.jpg"))

                    image_label = QLabel()
                    image_label.setContentsMargins(0, 0, 0, 0)
                    amount_label = QLabel(item.amount)
                    amount_label.setFixedSize(150, 25)
                    if int(item.amount.split(" ")[0]) <= 0:
                        amount_label.setText("Vyprodáno")
                        amount_label.setStyleSheet("background-color: red; color:white;")

                    scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
                    image_label.setPixmap(scaled_pixmap)

                    name_label = QLabel(item.name)
                    name_label.setFixedWidth(150)
                    name_label.setWordWrap(True)

                    price_label = QLabel(item.price)
                    price_label.setFixedSize(150, 20)

                    layout.addWidget(image_label, 0, 0)
                    layout.addWidget(name_label, 1, 0)
                    layout.addWidget(price_label, 3, 0)
                    layout.addWidget(amount_label, 2, 0)

                    frame.setLayout(layout)
                    self.mainLayout.addWidget(frame, x, y)

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
