from Application.Misc.thread import Thread
from Application.Widgets.Admin.edior_manager import EditorManager


class PriceEditor(EditorManager):
    def __init__(self):
        super(PriceEditor, self).__init__()

    def loadData(self):
        Thread("SELECT Name, Price FROM products", self.resupply).start_()

    def postData(self):
        Thread([f"UPDATE products SET Price={amount} WHERE Name='{name}'" for name, amount in
                zip(self.labelTextAll(), self.lineEditTextAll())], None).start_()
        self.loadData()
