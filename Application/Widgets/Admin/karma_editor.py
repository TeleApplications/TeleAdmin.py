from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QWidget, QSplitter

from Application.Misc.layouts import HBoxLayout, VBoxLayout
from Application.Misc.other import Button
from Application.Misc.thread import Thread
from json_manager import Json

data = Json().read()["admin"]["karmaEditor"]


class KarmaEditor(QWidget):
    def __init__(self):
        super(KarmaEditor, self).__init__()
        self.mainLayout = VBoxLayout()
        self.layout = HBoxLayout()

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
        self.loadComboBoxData()

    def loadComboBoxData(self):
        Thread(data["loadData"], self.setComboBoxData).run()

    def __unbanButtonFunction(self):
        Thread(data["postData"].format(int(self.comboBox.currentText())), None).run()
        self.loadComboBoxData()

    def setComboBoxData(self, items):
        self.__hideContent(False)
        self.comboBox.clear()
        self.comboBox.addItems([str(x[0]) for x in items])

    def __hideContent(self, hide: bool = False):
        self.comboBox.setHidden(hide)
        self.button.setHidden(hide)
        self.update()
