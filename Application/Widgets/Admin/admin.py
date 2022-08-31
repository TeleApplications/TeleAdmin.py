from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter

from Application.Misc.layouts import HBoxLayout
from Application.Misc.other import QLineEdit, StackedWidget
from Application.Widgets.Admin.karma_editor import KarmaEditor
from Application.Widgets.Admin.price_editor import PriceEditor
from Application.Widgets.Admin.supplies_editor import SuppliesEditor


class AdminWidget(QWidget):
    def __init__(self, parent=None):
        super(AdminWidget, self).__init__(parent)
        # init widgets
        self.listWidget = QListWidget()
        self.listWidget.setFont(QFont("Open Sans", 12))
        self.listWidget.currentItemChanged.connect(
            lambda: self.adminStack.changeIndex(self.listWidget.currentIndex().row()))

        self.lineEdit = QLineEdit()
        self.adminStack = StackedWidget(KarmaEditor, SuppliesEditor, PriceEditor, size=(0, 0, 0, 0))

        # splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.listWidget)
        self.splitter.addWidget(self.adminStack)

        # layout
        layout = HBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        # listbox data
        self.listWidget.addItems(["Karma", "Resupply", "Prices"])
