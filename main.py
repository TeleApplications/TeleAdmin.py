from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QSpacerItem, QSizePolicy, QWidget

from Application.Misc.thread import Thread
from download_images import DownloadImages
from Application.Misc.other import Button, StackedWidget
from Application.Misc.layouts import HBoxLayout, VBoxLayout
from Application.Widgets.Admin.admin import AdminWidget
from Application.Widgets.command_widget import CommandWidget

# TODO: stylesheet font size
from Application.Widgets.offlineorders_widget import OfflineOrdersWidget
from Application.Widgets.orders_widget import OrdersWidget
from Application.Widgets.settings import SettingsWidget
from Application.Widgets.displayproducts_window import DisplayProductsWindow
from email_manager import EmailManager
from json_manager import Json

data = Json().read()["email"]

PATH = "\\".join(__file__.split("\\")[0:-1]) + "\\Assets\\"


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # init widgets

        self.stackedWidget = StackedWidget(OrdersWidget, OfflineOrdersWidget, CommandWidget, AdminWidget,
                                           SettingsWidget)
        self.displayProductsWindow = None

        # init buttons
        self.databaseButton = Button(icon_name=PATH + "basket.png", min_size=(50, 50))
        self.offlineButton = Button(min_size=(50, 50))
        self.adminButton = Button(icon_name=PATH + "database.png", min_size=(50, 50))
        self.commandButton = Button(icon_name=PATH + "command.png", min_size=(50, 50))

        self.refreshButton = Button(icon_name=PATH + "refresh.png", min_size=(50, 50))
        self.displayProductsButton = Button(min_size=(50, 50))
        self.sendEmailButton = Button(min_size=(50, 50))
        self.settingsButton = Button(icon_name=PATH + "settings.png", min_size=(50, 50))
        # button actions
        self.databaseButton.clicked.connect(lambda: self.stackedWidget.changeIndex(0))
        self.offlineButton.clicked.connect(lambda: self.stackedWidget.changeIndex(1))
        self.adminButton.clicked.connect(lambda: self.stackedWidget.changeIndex(3))
        self.commandButton.clicked.connect(lambda: self.stackedWidget.changeIndex(2))

        self.refreshButton.clicked.connect(lambda: self.stackedWidget.classes_in_memory[0].loadData())
        self.displayProductsButton.clicked.connect(self.manageExternalWindow)
        self.sendEmailButton.clicked.connect(self.sendEmail)
        self.settingsButton.clicked.connect(lambda: self.stackedWidget.changeIndex(4))
        # layouts
        mainLayout = HBoxLayout()
        buttonLayout = VBoxLayout(margin=(5, 8, 0, 7))

        # left side top buttons
        buttonLayout.addWidget(self.databaseButton)
        buttonLayout.addWidget(self.offlineButton)
        buttonLayout.addWidget(self.adminButton)
        buttonLayout.addWidget(self.commandButton)
        # spacer (delimeter)
        verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Expanding)
        buttonLayout.addItem(verticalSpacer)
        # left side bottom buttons
        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addWidget(self.displayProductsButton)
        buttonLayout.addWidget(self.sendEmailButton)
        buttonLayout.addWidget(self.settingsButton)
        mainLayout.addLayout(buttonLayout)

        contentLayout = HBoxLayout()
        contentLayout.addWidget(self.stackedWidget)

        mainLayout.addLayout(contentLayout)

        # set widget layout
        self.setLayout(mainLayout)

    def manageExternalWindow(self):
        if self.displayProductsWindow is None:
            self.displayProductsWindow = DisplayProductsWindow()
            self.displayProductsWindow.show()
        else:
            self.displayProductsWindow.destroy()
            self.displayProductsWindow = None

    def sendEmail(self):
        self.em = EmailManager(data["username"], data["password"], data["receiver"], ["logs.txt", "test.py"])
        email = self.em.create_email(subject="PEPEGA", attachments=self.em.attachments)
        self.thread = Thread(self.em, self.em.send_email, email)

        self.thread.run()


class MainWindow(QMainWindow):
    WIDHT, HEIGHT = 900, 600

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(self.WIDHT, self.HEIGHT)
        self.setMinimumSize(self.WIDHT, self.HEIGHT)
        self.setWindowTitle("Telebufet Admin App")
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)
        self.im_downloader = DownloadImages(lock=False)
        self.im_downloader.download()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
