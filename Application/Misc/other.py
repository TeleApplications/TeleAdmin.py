from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QImage
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QLabel, QTreeWidgetItem, QStackedWidget, QWidget

from Application.Misc.layouts import VBoxLayout


class LineEdit(QLineEdit):
    def __init__(self, font_size: int = 9, place_holder_text: str = "", min_size: tuple[int, int] = None,
                 max_size: tuple[int, int] = None, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setFont(QFont("Open Sans", font_size))
        self.setPlaceholderText(place_holder_text)
        if max_size is not None:
            self.setMaximumSize(max_size[0], max_size[1])
        if min_size is not None:
            self.setMinimumSize(min_size[0], min_size[1])


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Open Sans", 12))
        self.setAcceptRichText(True)


class Label(QLabel):
    def __init__(self, text: str = "", font_size: int = 9, alignment=None, parent=None):
        super(Label, self).__init__(parent)
        self.setFont(QFont("Open Sans", font_size))
        self.setText(text)
        if alignment:
            self.setAlignment(alignment)


class Button(QPushButton):
    def __init__(self, text: str = "", font_size: int = 10, icon_name: str = "", icon_size: int = 32,
                 min_size: tuple[int, int] or None = None,
                 max_size: tuple[int, int] or None = None, parent=None):
        super(Button, self).__init__(parent)

        self.setText(text)
        if len(icon_name) > 0:
            self.setIcon(QIcon(icon_name))
            self.setIconSize(QSize(icon_size, icon_size))
        if min_size is not None:
            self.setMinimumSize(min_size[0], min_size[1])
        if max_size is not None:
            self.setMaximumSize(max_size[0], max_size[1])
        self.setFont(QFont("Open Sans", font_size))


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, text: str = "", font_size: int = 12, italic: bool = False,
                 color: QColor = QColor(0, 0, 0)):
        super(TreeWidgetItem, self).__init__(parent)
        self.setFont(0, QFont("Open Sans", font_size, italic=italic))
        self.setForeground(0, color)
        self.setText(0, text)


class StackedWidget(QStackedWidget):
    def __init__(self, *args):
        super(StackedWidget, self).__init__()
        self.classes_in_memory = list()

        for widget in args:
            self.stack_widget = QWidget()
            self.addWidget(self.stack_widget)
            class_in_memory = widget()
            self.classes_in_memory.append(class_in_memory)
            StackedWidget.stackWindows(class_in_memory, self.stack_widget)

    def changeIndex(self, index):
        if self.currentIndex() == index:
            return
        self.setCurrentIndex(index)
        try:
            self.classes_in_memory[index].loadData()
        except AttributeError:
            pass

    @staticmethod
    def stackWindows(widget, stack_widget: QWidget):
        layout = VBoxLayout(margin=(0, 10, 7, 7))
        layout.addWidget(widget)
        stack_widget.setLayout(layout)


def deleteLayout(layout) -> None:
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteLayout(item.layout())


def calculate_lines(item_number: int, width: int = 5) -> int:
    layer_number = item_number // width
    if item_number % width != 0:
        layer_number += 1

    return layer_number
