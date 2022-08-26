from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QSplitter

from Application.Misc.layouts import HBoxLayout, VBoxLayout
from Application.Misc.other import Button
from Application.Misc.thread import DatabaseThread
from json_manager import Json

data = Json().load()["admin"]["karmaEditor"]


class KarmaEditor(QWidget):
    def __init__(self):
        super(KarmaEditor, self).__init__()
        self.mainLayout = VBoxLayout()
        self.layout = HBoxLayout()

        self.getThread, self.postThread = None, None
        self.comboBox = QComboBox()
        self.comboBox.setMinimumHeight(30)

        self.button = Button(text="Unban! :(")
        self.button.clicked.connect(self.__unbanButtonFunction)

        self.__hideContent(True)

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.button)
        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(self.mainLayout)

    def loadData(self):
        self.getThread = DatabaseThread(data["loadData"], self.setComboBoxData)
        self.getThread.run()

    def __unbanButtonFunction(self):
        self.postThread = DatabaseThread(data["postData"].format(int(self.comboBox.currentText())), None)
        self.postThread.run()

        self.loadData()

    def setComboBoxData(self, items):
        self.__hideContent(False)
        self.comboBox.clear()
        self.comboBox.addItems([str(x[0]) for x in items])

    def __hideContent(self, hide: bool = False):
        self.comboBox.setHidden(hide)
        self.button.setHidden(hide)
        self.update()
