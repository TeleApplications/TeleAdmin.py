from PyQt5.QtCore import QThread, QObject
from json_manager import Json
from database import Database

credentials = Json().load()["credentials"]


class DatabaseThread(QThread):
    def __init__(self, sql_command: iter or str, widget):
        super(DatabaseThread, self).__init__()
        obj = Database(host=credentials["host"], user=credentials["user"], password=credentials["password"],
                       database=credentials["database"])
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
