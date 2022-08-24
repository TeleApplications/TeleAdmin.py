import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter

from Application.Misc.other import TextEdit
from Application.Misc.layouts import *
from json_manager import Json

data = Json().read()["settings"]


# right side should be stacked widget not textedit

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # init
        self.listWidget = QListWidget()
        self.listWidget.setFont(QFont("Open Sans", 12))
        self.listWidget.currentItemChanged.connect(self.changeText)
        self.textEdit = TextEdit()

        # splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.listWidget)
        splitter.addWidget(self.textEdit)

        # layout
        layout = HBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        # add items
        self.listWidget.addItems(["About"])

    def changeText(self):
        index = self.listWidget.currentIndex().row()
        match index:
            case 0:
                self.teAbout()
            case 1:
                ...
            case _:
                return None

    def teAbout(self):
        self.textEdit.setText(data["text"].format(u"\u00A9", datetime.date.today().year, u"\U0001F40D"))
