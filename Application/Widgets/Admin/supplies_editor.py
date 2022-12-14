import time

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel, QLineEdit

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import Button, deleteLayout
from Application.Misc.thread import DatabaseThread
from Application.Misc.dotenv_manager import DotEnv

data = DotEnv()


class SuppliesEditor(QWidget):
    leList = list()
    lblList = list()

    def __init__(self):
        super(SuppliesEditor, self).__init__()
        self.getThread, self.postThread = None, None

        self.scrollLayout = VBoxLayout()

        self.setLayout(self.scrollLayout)

        self.scroll = QScrollArea()
        self.scrollLayout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scroll)

        self.scrollLayout = VBoxLayout(margin=(10, 10, 10, 10))
        self.scrollContent.setLayout(self.scrollLayout)
        self.btn = Button(text="Post", min_size=None, max_size=None)
        self.btn.clicked.connect(self.__postData)
        self.regex = QRegExp("[0-9]*")

    def __resupply(self, items):
        self.leList.clear()
        self.lblList.clear()
        deleteLayout(self.scrollLayout)

        for product_name, amount in items:
            layout = HBoxLayout()
            label = QLabel(product_name)
            label.setObjectName("product_name")
            lineEdit = QLineEdit()
            lineEdit.setMaximumHeight(20)
            validator = QRegExpValidator(self.regex, lineEdit)
            lineEdit.setValidator(validator)
            lineEdit.setText(str(amount))


            self.leList.append(lineEdit)
            self.lblList.append(label)

            layout.addWidget(label)
            layout.addWidget(lineEdit)

            self.scrollLayout.addLayout(layout)
        self.scrollLayout.addWidget(self.btn)
        self.scroll.setWidget(self.scrollContent)

    def loadData(self):
        self.getThread = DatabaseThread(data.get("ASEloadData"), self.__resupply)
        self.getThread.run()

    def __postData(self):
        self.postThread = DatabaseThread(
            [data.get("ASEpostData").format(amount, time.strftime("%H:%M:%S"), name) for name, amount in
             zip(self.__labelTextAll(), self.__lineEditTextAll())], None)
        self.postThread.run()
        self.loadData()

    def __labelTextAll(self):
        return [x.text() for x in self.lblList]

    def __lineEditTextAll(self):
        return [int(x.text()) for x in self.leList]
