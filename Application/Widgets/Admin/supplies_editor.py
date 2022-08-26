import time

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QScrollArea

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import Button, deleteLayout, Label, LineEdit
from Application.Misc.thread import DatabaseThread
from json_manager import Json

data = Json().load()["admin"]["suppliesEditor"]


class SuppliesEditor(QWidget):
    leList = list()
    lblList = list()

    def __init__(self):
        super(SuppliesEditor, self).__init__()
        self.scrollLayout = VBoxLayout(margin=(0, 0, 10, 0))
        self.setLayout(self.scrollLayout)

        self.scroll = QScrollArea()
        self.scrollLayout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scroll)

        self.scrollLayout = VBoxLayout(margin=(10, 10, 10, 10))
        self.scrollContent.setLayout(self.scrollLayout)
        self.btn = Button(text="Post", min_size=None, max_size=None)
        self.btn.clicked.connect(self.postData)
        self.regex = QRegExp("[0-9]*")

    def resupply(self, items):
        self.leList.clear()
        self.lblList.clear()
        deleteLayout(self.scrollLayout)

        for x in items:
            layout = HBoxLayout()
            label = Label(str(x[0]), font_size=12)
            lineEdit = LineEdit(font_size=12, max_size=(250, 20))
            validator = QRegExpValidator(self.regex, lineEdit)
            lineEdit.setValidator(validator)
            lineEdit.setText(f"{x[1]}")

            self.leList.append(lineEdit)
            self.lblList.append(label)

            layout.addWidget(label)
            layout.addWidget(lineEdit)

            self.scrollLayout.addLayout(layout)
        self.scrollLayout.addWidget(self.btn)
        self.scroll.setWidget(self.scrollContent)

    def loadData(self):
        self.getThread = DatabaseThread(data["loadData"], self.resupply)
        self.getThread.run()

    def postData(self):
        self.postThread = DatabaseThread(
            [data["postData"].format(amount, time.strftime("%H:%M:%S"), name) for name, amount in
             zip(self.labelTextAll(), self.lineEditTextAll())], None)
        self.postThread.run()
        self.loadData()

    def labelTextAll(self):
        return [x.text() for x in self.lblList]

    def lineEditTextAll(self):
        return [int(x.text()) for x in self.leList]
