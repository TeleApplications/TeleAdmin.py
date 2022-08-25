import time
import sys as sus

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidget

from Application.Misc.other import Label, Button, deleteLayout, calculate_lines
from Application.Misc.thread import Thread
from json_manager import Json
from dictionary import Dictionary

data = Json().read()["offlineOrders"]
PATH = sus.path[0] + "\Assets\Products"
width = 5
size = QSize(64, 64)


class Item:
    def __init__(self, name: str, price: str, url: str):
        self.name = name
        self.price = price
        self.url = PATH + "\\" + url.rsplit("/", 1)[1]


class OfflineOrdersWidget(QWidget):
    def __init__(self, parent=None):
        super(OfflineOrdersWidget, self).__init__(parent)

        self.products_value = float()
        self.idlist = list()
        self.dictionary = Dictionary()

        self.mainLayout = QGridLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.productList = QListWidget()
        self.productList.setFixedWidth(175)

        self.priceLabel = Label("Price: 0.0 kč")

        self.approveButton = Button("Approve")
        self.approveButton.clicked.connect(self.approveButtonFunction)

        self.clearButton = Button("Clear")
        self.clearButton.clicked.connect(self.clearButtonFunction)

        # self.mainLayout.addWidget(QSplitter(Qt.Vertical), 1, 0)
        self.mainLayout.addWidget(self.productList, 0, 2)
        self.mainLayout.addWidget(self.approveButton, 2, 0)
        self.mainLayout.addWidget(self.clearButton, 2, 1)
        self.mainLayout.addWidget(self.priceLabel, 2, 2)
        self.mainLayout.setColumnStretch(0, 1)
        self.setLayout(self.mainLayout)

    def loadData(self):
        Thread(data["loadData"], self.content).run()

    def content(self, items):

        deleteLayout(self.layout)
        self.layout = QGridLayout()
        pixmap = QPixmap()
        item_layout = QGridLayout()
        item_layout.setContentsMargins(0, 0, 0, 0)
        items_number = len(items)
        number_of_lines = calculate_lines(items_number, width)

        for x in range(number_of_lines):
            for y in range(width):
                if items_number > 0:
                    items_number -= 1
                    item = Item(*items[x * width + y])
                    pixmap.loadFromData(open(item.url, "rb").read())
                    button = Button(text=item.name)
                    button.setIcon(QIcon(pixmap))
                    button.setIconSize(size)
                    button.setStyleSheet("QPushButton {text-align: left;}")
                    button.clicked.connect(
                        lambda a, product_name=item.name, price=item.price: self.buttonFunction(product_name, price))

                    item_layout.addWidget(button, x, y)
                    self.layout.addLayout(item_layout, x, y)

        self.mainLayout.addLayout(self.layout, 0, 0, 1, 2)

    def approveButtonFunction(self):
        if self.dictionary.items():
            Thread(
                [(data["postData"][0].format(v, 4, k), data["postData"][1].format(v, time.strftime("%H:%M:%S"), k)) for
                 k, v in self.dictionary.items()], None).run()
            self.clear()

    def clearButtonFunction(self):
        self.clear()

    def clear(self):
        self.productList.clear()
        self.products_value = 0.0
        self.priceLabel.setText("Price: 0.0 kč")
        self.dictionary.clear()

    def buttonFunction(self, product_name: str, price: float):
        self.products_value += price
        self.priceLabel.setText("Price: " + str(round(self.products_value, 0)) + " kč")
        self.productList.addItem(str(product_name))
        self.dictionary.add_item(product_name, 1)
