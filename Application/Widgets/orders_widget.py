import time

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidget, QWidget, QSizePolicy

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import TreeWidgetItem, Button
from Application.Misc.thread import Thread
from json_manager import Json

data = Json().read()["orders"]


class OrdersWidget(QWidget):
    def __init__(self):
        super(OrdersWidget, self).__init__()
        self.mainLayout = VBoxLayout()
        self.treewidget = TreeWidget()

        # BUTT-ONs
        self.buttonsLayout = HBoxLayout()
        self.approveButton = Button("Approve")
        self.declineButton = Button("Decline")

        self.approveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.declineButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.approveButton.clicked.connect(self.approveButtonFunction)
        self.declineButton.clicked.connect(self.declineButtonFunction)

        self.buttonsLayout.addWidget(self.approveButton)
        self.buttonsLayout.addWidget(self.declineButton)

        self.mainLayout.addWidget(self.treewidget)
        self.mainLayout.addLayout(self.buttonsLayout)

        self.setLayout(self.mainLayout)

        self.loadData()

    def approveButtonFunction(self):
        item = self.treewidget.removeSelectedItem()
        if item:
            order = item.text(0).split(" ")[1::2]
            Thread(
                [data["approveButton"][0].format(order[0], order[-1]),
                 data["approveButton"][1].format(order[1])],
                None).run()

    def declineButtonFunction(self):
        item = self.treewidget.removeSelectedItem()
        if item:
            order = item.text(0).split(" ")[1::2]

            products = self.treewidget.getChildren(item)
            print(products)

            Thread([data["declineButton"][0].format(order[0], order[-1]),
                    data["declineButton"][1].format(order[1])] + [
                       data["declineButton"][2].format(amount, time.strftime("%H:%M:%S"), product) for product, amount
                       in products],
                   None).run()

    def loadData(self):
        Thread(data["refreshDatabase"], self.treewidget.addDatabaseData).run()


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setColumnCount(1)

    def addDatabaseData(self, data: list):
        self.clear()
        for x in data:
            topItem = TreeWidgetItem(self, f"ID: {x[0]} UID: {x[1]} Price: {x[2]},- Time: {x[3]}")
            [TreeWidgetItem(topItem, x, 11, True, color=QColor(100, 100, 100)).setDisabled(True) for x in
             x[4].split(",")]
            self.addTopLevelItem(topItem)
        self.expandAll()

    def removeSelectedItem(self):
        root = self.invisibleRootItem()
        item = self.selectedItems()

        if item:
            return_val = item.copy()[0]

            (item[0].parent() or root).removeChild(item[0])
            return return_val

    def getChildren(self, parent):
        if parent:
            return [parent.child(index).text(0).split(": ") for index in range(parent.childCount())]
