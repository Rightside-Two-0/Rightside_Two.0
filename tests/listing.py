import sys, json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import traceback
# Ui_MainWindow, QtBaseClass = uic.loadUiType('tree_view.ui')
class ListView(QtWidgets.QTreeView):
    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        self.setModel(QtGui.QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.setHeaderHidden(True)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)

    def addItem(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.model().appendRow([first, second])
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setupUi(self)
        uic.loadUi('financial.ui', self)
        # self.income = self.findChild(QtWidget.ListView, 'income_view')
        # self.expenses = self.findChild(QtWidget.ListView, 'expenses_view')
        # # self.assets = ListView(self)
        # # self.liabilities = ListView(self)
        # # self.opportunities = ListView(self)
        # self.load()
        # self.load_exp()
        # self.load_assets()
        # self.load_debts()
        # layout_left = QtWidgets.QVBoxLayout(self)
        # layout_right = QtWidgets.QVBoxLayout(self)
        # horizontal = QtWidgets.QHBoxLayout(self)
        # horizontal_2 = QtWidgets.QHBoxLayout(self)
        # horizontal_3 = QtWidgets.QHBoxLayout(self)
        # horizontal.addWidget(self.income)
        # horizontal.addWidget(self.opportunities)
        # horizontal_2.addWidget(self.expenses)
        # horizontal_2.addWidget(self.opportunities)
        # horizontal_3.addWidget(self.assets)
        # horizontal_3.addWidget(self.liabilities)
        # layout_left.addLayout(horizontal)
        # layout_left.addLayout(horizontal_2)
        # layout_left.addLayout(horizontal_3)

    def addItem(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.income.model().appendRow([first, second])
    def load_debts(self):
        try:
            with open('liabilities.db', 'r') as f:
                content = json.load(f)
                for item in content['Liabilities']:
                    key = list(item.keys())[0]
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            self.liabilities.addItem(keys, str(i[keys]))
                    else:
                        self.liabilities.addItem(key, str(item[key]))
        except Exception:
            traceback.print_exc()
    def load_assets(self):
        try:
            with open('assets.db', 'r') as f:
                content = json.load(f)
                for item in content['Assets']:
                    key = list(item.keys())[0]
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            self.assets.addItem(keys, str(i[keys]))
                            if isinstance(i, list):
                                keys = list(i[keys], list)
                    else:
                        self.assets.addItem(key, str(item[key]))
        except Exception:
            traceback.print_exc()
    def load_exp(self):
        try:
            with open('expenses.db', 'r') as f:
                content = json.load(f)
                for item in content['Expenses']:
                    key = list(item.keys())[0]
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            self.expenses.addItem(keys, str(i[keys]))
                    else:
                        self.expenses.addItem(key, str(item[key]))
        except Exception:
            traceback.print_exc()
    def load(self):
       try:
           with open('data.db', 'r') as f:
               content = json.load(f)
               for item in content['Income']:
                   key = list(item.keys())[0]
                   if isinstance(item[key], list):
                       for i in item[key]:
                           keys = list(i.keys())[0]
                           self.income.addItem(keys, str(i[keys]))
                   else:
                       self.income.addItem(key, str(item[key]))
       except Exception:
           traceback.print_exc()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
