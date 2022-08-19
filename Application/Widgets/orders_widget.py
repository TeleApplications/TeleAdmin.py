from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidget, QWidget, QSizePolicy

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import TreeWidgetItem, Button
from Application.Misc.thread import Thread


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

    def approveButtonFunction(self):
        item = self.treewidget.removeSelectedItem()
        if item:
            order = item.text(0).split(" ")[1:4:2]

            Thread(
                (f"UPDATE orders SET Status='done' WHERE OrderNumber={order[0]}",
                 f"UPDATE users SET Karma=Karma + 20 WHERE UserID={order[1]}"), None).start_()

    def declineButtonFunction(self):
        item = self.treewidget.removeSelectedItem()
        if item:
            order = item.text(0).split(" ")[1:4:2]
            products = self.treewidget.getChildren(item)
            Thread([f"UPDATE orders SET Status='canceled' WHERE OrderNumber={order[0]}",
                    f"UPDATE users SET Karma=Karma - 20 WHERE UserID={order[1]}"] + [
                       f"UPDATE products SET Amount=Amount + {amount} WHERE Name = '{product}'" for product, amount in
                       products], None).start_()


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.refreshDatabase()

    def addDatabaseData(self, data: list):
        self.clear()
        for x in data:
            topItem = TreeWidgetItem(self, f"ID: {x[0]} UID: {x[1]} Price: {x[2]},- Time: {x[3]}")
            [TreeWidgetItem(topItem, x, 11, True, color=QColor(100, 100, 100)).setDisabled(True) for x in
             x[4].split(",")]
            self.addTopLevelItem(topItem)
        self.expandAll()

    def refreshDatabase(self):
        Thread(
            "SELECT o.OrderNumber, o.UserID, SUM(p.Price * o.Amount) as OrderPrice, o.ReservedTime,"
            " GROUP_CONCAT(p.Name, ': ', o.Amount SEPARATOR ',') as Items FROM orders o"
            " INNER JOIN products p ON p.ProductID = o.ProductID WHERE Status = 'pending'"
            " GROUP BY o.OrderNumber, ReservedTime ORDER BY o.OrderNumber;",
            self.addDatabaseData
        ).start_()

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
