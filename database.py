import mysql.connector as sql
from PyQt5.QtCore import pyqtSignal, QObject


class Database(QObject):
    data = pyqtSignal(list)

    def __init__(self, host: str, user: str, password: str, database: str, sql_command: str):
        super(Database, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.sql_command = sql_command

    def get(self):
        try:
            db = sql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = db.cursor()
            if isinstance(self.sql_command, list or tuple):
                for x in self.sql_command:
                    if isinstance(x, tuple):
                        for y in x:
                            cursor.execute(y)
                    else:
                        cursor.execute(x)
            else:
                cursor.execute(self.sql_command)
            self.data.emit([x for x in cursor])
            db.commit()
            print(self.sql_command)
        except sql.errors.DatabaseError:
            print("SQL Command Error")
        except sql.errors.InterfaceError:
            print("Database Connection Error")
