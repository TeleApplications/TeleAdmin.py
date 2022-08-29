from PyQt5.QtCore import pyqtSignal, QObject

import mysql.connector as sql
from typing import Iterable

from unpack_array import UnpackArray


class Database(QObject):
    data = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, host: str, user: str, password: str, database: str):
        super(Database, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.unpack = UnpackArray()

    def get(self, sql_command: Iterable) -> None:
        try:
            db = sql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = db.cursor()

            self.unpack.unpack_array(sql_command, list | tuple)
            for query in self.unpack:
                cursor.execute(str(query))
            self.data.emit([x for x in cursor])
            db.commit()

        except sql.errors.DatabaseError:
            print("SQL Command Error")
        except sql.errors.InterfaceError:
            print("Database Connection Error")
        self.finished.emit()

