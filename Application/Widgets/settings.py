import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter

from Application.Misc.other import TextEdit
from Application.Misc.layouts import *


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
        text = f"""Application for Telebufet by github.com/<b>Vi-tek</b><br><br>
© {datetime.date.today().year} schemeXY All Rights Reserved<hr>Powered by: Python 3.10 🐍<hr>Something went wrong?<br>Contact us at: TeleApplications@protonmail.com<hr>credits: @Ma-Tes<br>"""
        self.textEdit.setText(text)
