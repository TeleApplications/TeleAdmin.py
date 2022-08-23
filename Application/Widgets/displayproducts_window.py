import os

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from Application.Misc.other import Label
from Application.Misc.thread import Thread
from dictionary import Dictionary
from download_images import threaded_downloading
from json_manager import Json

# TODO: settings reset image cache

data = Json().read()["displayProductsWindow"]

PATH = "Assets//Products//"


class DisplayProductsWindow(QWidget):
    def __init__(self):
        super(DisplayProductsWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPostition = QPoint()
        self.mainLayout = QGridLayout()
        self.dictionary = Dictionary()
        self.setLayout(self.mainLayout)
        self.loadData()

    def loadData(self):
        Thread(data["loadDictionary"], self.init_dict).run()
        Thread(data["loadData"], self.content).run()


    def init_dict(self, items):
        for image_id, url in items:
            self.dictionary.add_item(image_id, url.rsplit("/", 1)[1])

    def content(self, items):
        for i, item in enumerate(items):
            layout = QGridLayout()
            lbl = Label(alignment=Qt.AlignCenter)
            lbl.setMaximumSize(256, 256)
            lbl.setMinimumSize(256, 256)
            pixmap = QPixmap()
            try:
                pixmap.loadFromData(self.open_image(PATH + self.dictionary[item[3]]))
            except FileNotFoundError:
                self.downloadImages()
                pixmap.loadFromData(self.open_image(PATH + "Unknown_Image.jpg"))

            scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
            lbl.setPixmap(scaled_pixmap)
            # lbl.setScaledContents(True)
            layout.addWidget(lbl,0, 0, 1, 2)
            layout.addWidget(Label(item[0], font_size=10, alignment=Qt.AlignCenter), 1, 0, 1, 2)
            layout.addWidget(Label(str(item[1])), 2, 1)
            layout.addWidget(Label(str(item[2]), alignment=Qt.AlignRight), 2, 0)
            self.mainLayout.addLayout(layout, 0, i)

    def open_image(self, image):
        with open(image, "rb") as f:
            return f.read()

    def mousePressEvent(self, event):
        self.oldPostition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPostition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPostition = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.update()


    def downloadImages(self):
        if len(os.listdir("Assets//Products//")) == 1:
            Thread(data["loadDictionary"], self.initImages).run()

    def initImages(self, items):
        threaded_downloading([url for _, url in items])
