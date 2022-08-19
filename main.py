from PyQt5.QtWidgets import QMainWindow, QApplication, QSpacerItem, QSizePolicy, QWidget

from Application.Misc.other import Button, StackedWidget
from Application.Misc.layouts import HBoxLayout, VBoxLayout
from Application.Widgets.Admin.admin import AdminWidget
from Application.Widgets.command_widget import CommandWidget

# TODO: stylesheet font size
from Application.Widgets.offlineorders_widget import OfflineOrdersWidget
from Application.Widgets.orders_widget import OrdersWidget
from Application.Widgets.settings import SettingsWidget

PATH = "\\".join(__file__.split("\\")[0:-1]) + "\\Assets\\"


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # init widgets
        self.stackedWidget = StackedWidget(OrdersWidget,OfflineOrdersWidget, CommandWidget, AdminWidget, SettingsWidget)

        # init buttons
        self.databaseButton = Button(icon_name=PATH + "basket.png", min_size=(50, 50))
        self.offlineButton = Button(min_size=(50, 50))
        self.commandButton = Button(icon_name=PATH + "command.png", min_size=(50, 50))
        self.adminButton = Button(icon_name=PATH + "database.png", min_size=(50, 50))
        self.refreshButton = Button(icon_name=PATH + "refresh.png", min_size=(50, 50))
        self.settingsButton = Button(icon_name=PATH + "settings.png", min_size=(50, 50))

        # button actions
        self.databaseButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.offlineButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.commandButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.adminButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.refreshButton.clicked.connect(lambda: OrdersWidget().treewidget.refreshDatabase())
        self.settingsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        # layouts
        mainLayout = HBoxLayout()
        buttonLayout = VBoxLayout(margin=(5, 8, 0, 7))

        # left side buttons
        buttonLayout.addWidget(self.databaseButton)
        buttonLayout.addWidget(self.offlineButton)
        buttonLayout.addWidget(self.adminButton)
        buttonLayout.addWidget(self.commandButton)
        # spacer
        verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Expanding)
        buttonLayout.addItem(verticalSpacer)
        # settings button
        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addWidget(self.settingsButton)
        mainLayout.addLayout(buttonLayout)

        contentLayout = HBoxLayout()
        contentLayout.addWidget(self.stackedWidget)

        mainLayout.addLayout(contentLayout)

        # set widget layout
        self.setLayout(mainLayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(850, 600)
        self.setMinimumSize(850, 600)
        self.setWindowTitle("Telebufet Admin App")
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
