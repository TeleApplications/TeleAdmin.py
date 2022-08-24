from PyQt5.QtCore import QThread
from json_manager import Json
from database import Database

credentials = Json().read()["credentials"]


class Thread(QThread):
    def __init__(self, sql_command: iter or str, widget):
        super(Thread, self).__init__()
        self.obj = Database(host=credentials["host"], user=credentials["user"], password=credentials["password"],
                            database=credentials["database"],
                            sql_command=sql_command)
        if widget is not None:
            self.obj.data.connect(widget)
        self.obj.moveToThread(self)
        self.started.connect(self.obj.get)

    def run(self) -> None:
        self.start()
        self.quit()
        self.wait()
