from Application.Misc.thread import Thread
from Application.Widgets.Admin.edior_manager import EditorManager


class SuppliesEditor(EditorManager):
    def __init__(self):
        super(SuppliesEditor, self).__init__()

    def loadData(self):
        Thread("SELECT Name, Amount FROM PRODUCTS", self.resupply).start_()

    def postData(self):
        Thread([f"UPDATE products SET Amount={amount} WHERE Name='{name}'" for name, amount in
                zip(self.labelTextAll(), self.lineEditTextAll())], None).start_()
        self.loadData()
