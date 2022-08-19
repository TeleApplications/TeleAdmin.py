from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSplitter, QListWidget

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import deleteLayout, Button, Label
from Application.Misc.thread import Thread

import math


class OfflineOrdersWidget(QWidget):
    def __init__(self, parent=None):
        super(OfflineOrdersWidget, self).__init__(parent)

        self.products_value = float()
        self.idlist = list()

        self.mainLayout = QGridLayout()

        self.productList = QListWidget()
        self.productList.setMaximumWidth(150)

        self.priceLabel = Label("Price: ")

        self.approveButton = Button("Approve")
        self.approveButton.clicked.connect(self.approveButtonFunction)

        # self.mainLayout.addWidget(QSplitter(Qt.Vertical), 1, 0)
        self.mainLayout.addWidget(self.productList, 0, 1)
        self.mainLayout.addWidget(self.approveButton, 2, 0)
        self.mainLayout.addWidget(self.priceLabel, 2, 1)
        self.setLayout(self.mainLayout)
        self.loadData()

    def loadData(self):
        Thread("SELECT ProductID, Name, Price FROM products", self.content).start_()

    def content(self, items):
        # deleteLayout(self.mainLayout)
        layout = QGridLayout()
        x, y, p = 0, 0, 0
        while p < len(items):

            if x % 5 == 0:
                y += 1
                x = 0
            button = QPushButton()
            button.clicked.connect(
                lambda item_id=items[p][0],product_name=items[p][1], price=items[p][2]: self.buttonFunction(item_id,product_name, price))
            layout.addWidget(button, y, x)

            x += 1
            p += 1

        self.mainLayout.addLayout(layout, 0, 0)


    def approveButtonFunction(self):
        print(self.products_value)

    def buttonFunction(self, item_id: int, product_name:str, price: float):
        self.idlist.append(item_id)
        self.products_value += price
        self.priceLabel.setText("Price: " + str(self.products_value) + " kč")
        self.productList.addItem(product_name)
