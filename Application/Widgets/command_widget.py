from PyQt5.QtWidgets import QWidget, QLineEdit

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import Button, TextEdit
from Application.Misc.thread import DatabaseThread


class CommandWidget(QWidget):
    def __init__(self, parent=None):
        super(CommandWidget, self).__init__(parent)
        self.textEdit = TextEdit()
        self.postThread = None

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter a SQL command! (Do not touch if you don't know how to work with it!)")
        self.button = Button(text="Send", min_size=(100, 30))
        self.button.clicked.connect(self.__postData)
        layout = VBoxLayout()

        btnleLayout = HBoxLayout()
        btnleLayout.addWidget(self.lineEdit)
        btnleLayout.addWidget(self.button)

        teLayout = VBoxLayout()
        teLayout.addWidget(self.textEdit)

        layout.addLayout(teLayout)
        layout.addLayout(btnleLayout)
        self.setLayout(layout)

    def __postData(self):
        text = self.lineEdit.text()
        if text in ("cls", "clear"):
            self.textEdit.clear()

        if len(text) > 0:
            self.postThread = DatabaseThread(text, self.__setTextEditData)
            self.postThread.run()
        self.lineEdit.clear()
        self.lineEdit.setFocus()

    def __setTextEditData(self, data: list):
        for x in data:
            self.textEdit.append(str(x))
