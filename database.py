import mysql.connector as sql
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot


class Database(QObject):
    data = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, host: str, user: str, password: str, database: str):
        super(Database, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get(self, sql_command: str) -> None:
        try:
            db = sql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = db.cursor()
            if isinstance(sql_command, list or tuple):
                for x in sql_command:
                    if isinstance(x, tuple):
                        for y in x:
                            cursor.execute(y)
                    else:
                        cursor.execute(x)
            else:
                cursor.execute(sql_command)
            self.data.emit([x for x in cursor])
            db.commit()
            print(sql_command)
        except sql.errors.DatabaseError:
            print("SQL Command Error")
        except sql.errors.InterfaceError:
            print("Database Connection Error")
        self.finished.emit()
