from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtWidgets import QPushButton, QTextEdit, QTreeWidgetItem, QStackedWidget, QWidget

from Application.Misc.layouts import VBoxLayout


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAcceptRichText(True)
        self.setReadOnly(True)


class Button(QPushButton):
    def __init__(self, text: str = "", object_name: str = None, icon_name: str = "",
                 icon_size: int = 32,
                 min_size: tuple[int, int] or None = None,
                 max_size: tuple[int, int] or None = None, parent=None):
        super(Button, self).__init__(parent)

        self.setText(text)
        if object_name:
            self.setObjectName(object_name)
        if len(icon_name) > 0:
            self.setIcon(QIcon(icon_name))
            self.setIconSize(QSize(icon_size, icon_size))
        if min_size is not None:
            self.setMinimumSize(min_size[0], min_size[1])
        if max_size is not None:
            self.setMaximumSize(max_size[0], max_size[1])


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, text: str = "", font_size: int = 12, italic: bool = False,
                 color: QColor = QColor(0, 0, 0)):
        super(TreeWidgetItem, self).__init__(parent)
        self.setFont(0, QFont("Open Sans", font_size, italic=italic))
        self.setForeground(0, color)
        self.setText(0, text)


class StackedWidget(QStackedWidget):
    def __init__(self, *args, size: tuple[int, int, int, int] = (0, 7, 7, 7)):
        super(StackedWidget, self).__init__()
        self.classes_in_memory = list()
        self.size = size

        for widget in args:
            self.stack_widget = QWidget()
            self.addWidget(self.stack_widget)
            class_in_memory = widget()
            self.classes_in_memory.append(class_in_memory)
            self.stackWindows(class_in_memory, self.stack_widget)

    def changeIndex(self, index):
        if self.currentIndex() == index:
            return
        self.setCurrentIndex(index)
        try:
            self.classes_in_memory[index].loadData()
        except AttributeError:
            pass

    def stackWindows(self, widget, stack_widget: QWidget):
        layout = VBoxLayout(margin=(self.size[0], self.size[1], self.size[2], self.size[3]))
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
