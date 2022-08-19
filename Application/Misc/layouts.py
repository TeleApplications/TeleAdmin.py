from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


class HBoxLayout(QHBoxLayout):
    def __init__(self, margin: tuple[int, int, int, int] = (0, 0, 0, 0), parent=None):
        super(HBoxLayout, self).__init__(parent)
        self.setContentsMargins(margin[0], margin[1], margin[2], margin[3])


class VBoxLayout(QVBoxLayout):
    def __init__(self, margin: tuple[int, int, int, int] = (0, 0, 0, 0), parent=None):
        super(VBoxLayout, self).__init__(parent)
        self.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
