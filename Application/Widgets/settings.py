import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter

from Application.Misc.other import TextEdit
from Application.Misc.layouts import *
from json_manager import Json
from download_images import DownloadImages

data = Json().load()["settings"]


# right side should be stacked widget not textedit

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # init
        self.listWidget = QListWidget()
        self.listWidget.setFont(QFont("Open Sans", 12))
        self.listWidget.currentItemChanged.connect(self.changeText)
        self.textEdit = TextEdit()

        self.im_downloader = DownloadImages(lock=False)

        # splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.listWidget)
        splitter.addWidget(self.textEdit)

        # layout
        layout = HBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        # add items
        self.listWidget.addItems(["About", "Download Images"])

    def changeText(self):
        index = self.listWidget.currentIndex().row()
        match index:
            case 0:
                self.teAbout()
            case 1:
                self.im_downloader.download()
            case _:
                return None

    def teAbout(self):
        self.textEdit.setText(data["text"].format(u"\u00A9", datetime.date.today().year, u"\U0001F40D"))
