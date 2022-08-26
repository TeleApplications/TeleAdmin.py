from PyQt5.QtWidgets import QWidget

from Application.Misc.layouts import VBoxLayout, HBoxLayout
from Application.Misc.other import LineEdit, Button
from Application.Misc.thread import DatabaseThread
from Application.Misc.other import TextEdit


class CommandWidget(QWidget):
    def __init__(self, parent=None):
        super(CommandWidget, self).__init__(parent)
        self.textEdit = TextEdit()

        self.lineEdit = LineEdit(
            place_holder_text="Enter a SQL command! (Do not touch if you don't know how to work with it!)",
            font_size=10, min_size=(100, 30))
        self.button = Button(text="Send", min_size=(100, 30))
        self.button.clicked.connect(self.buttonClicked)
        layout = VBoxLayout()

        btnleLayout = HBoxLayout()
        btnleLayout.addWidget(self.lineEdit)
        btnleLayout.addWidget(self.button)

        teLayout = VBoxLayout()
        teLayout.addWidget(self.textEdit)

        layout.addLayout(teLayout)
        layout.addLayout(btnleLayout)
        self.setLayout(layout)

    def buttonClicked(self):
        text = self.lineEdit.text()
        if text in ("cls", "clear"):
            self.textEdit.clear()

        if len(text) > 0:
            DatabaseThread(text, self.setTextEditData).run()

        self.lineEdit.clear()
        self.lineEdit.setFocus()

    def setTextEditData(self, data: list):
        for x in data:
            self.textEdit.append(str(x))
