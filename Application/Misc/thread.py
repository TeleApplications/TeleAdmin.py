from PyQt5.QtCore import QThread, QObject
from database import Database

from Application.Misc.dotenv_manager import DotEnv

credentials = DotEnv()


class DatabaseThread(QThread):
    def __init__(self, sql_command: iter or str, widget):
        super(DatabaseThread, self).__init__()
        obj = Database(host=credentials.get("Dhost"),
                       user=credentials.get("Duser"),
                       password=credentials.get("Dpassword"),
                       database=credentials.get("Ddatabase"))
        obj.moveToThread(self)
        if widget is not None:
            obj.data.connect(widget)

        obj.finished.connect(self.quit)
        obj.finished.connect(obj.deleteLater)
        obj.finished.connect(self.deleteLater)

        self.started.connect(lambda: obj.get(sql_command))

    def run(self):
        self.start()
        self.wait()


class Thread(QThread):
    def __init__(self, object_: QObject, func_, *args):
        super(Thread, self).__init__()
        object_.moveToThread(self)
        object_.finished.connect(self.quit)
        object_.finished.connect(object_.deleteLater)
        object_.finished.connect(self.deleteLater)

        self.started.connect(lambda: func_(*args))

    def run(self):
        self.start()
        self.wait()
