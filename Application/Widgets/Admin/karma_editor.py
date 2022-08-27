from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QSplitter

from Application.Misc.layouts import HBoxLayout, VBoxLayout
from Application.Misc.other import Button, deleteLayout
from Application.Misc.thread import DatabaseThread
from Application.Misc.dotenv_manager import DotEnv


data = DotEnv()


class KarmaEditor(QWidget):
    def __init__(self):
        super(KarmaEditor, self).__init__()
        self.mainLayout = VBoxLayout()
        self.layout = HBoxLayout()

        self.getThread, self.postThread = None, None
        self.comboBox = QComboBox()
        self.comboBox.setMinimumHeight(30)

        self.button = Button(text="Unban! :(")
        self.button.clicked.connect(self.__postData)

        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(self.mainLayout)

    def loadData(self):
        self.getThread = DatabaseThread(data.get("AKEloadData"), self.__setComboBoxData)
        self.getThread.run()

    def __postData(self):
        self.postThread = DatabaseThread(data.get("AKEpostData").format(int(self.comboBox.currentText())), None)
        self.postThread.run()

        self.loadData()

    def __setComboBoxData(self, items):
        deleteLayout(self.layout)
        self.comboBox.clear()
        self.comboBox.addItems([str(x[0]) for x in items])
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.button)
