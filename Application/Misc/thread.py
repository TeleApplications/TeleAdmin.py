from PyQt5.QtCore import QThread

from database import Database


class Thread(QThread):
    def __init__(self, sql_command: iter or str, widget):
        super(Thread, self).__init__()
        self.obj = Database(host="localhost", user="root", password="", database="telebufettestdatabase", sql_command=sql_command)
        if widget is not None:
            self.obj.data.connect(widget)
        self.obj.moveToThread(self)
        self.started.connect(self.obj.get)

    def start_(self) -> None:
        self.start()
        self.quit()
        self.wait()
