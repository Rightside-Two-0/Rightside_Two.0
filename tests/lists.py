import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import traceback

Ui_MainWindow, QtBaseClass = uic.loadUiType('financial.ui')
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
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            self.setupUi(self)
            self.income_view = ListView(self)
            self.expenses_view = ListView(self)
            self.assets_view = ListView(self)
            self.liabilities_view = ListView(self)
            self.opportunity_view = ListView(self)
            self.load('income')
        except Exception:
            traceback.print_exc()

        self.load('expenses')
        self.load('assets')
        self.load('liabilities')
        self.addButton.clicked.connect(self.addTransaction)
        self.analyzeButton.clicked.connect(self.analyze)


    def addTransaction(self):
        try:
            ledger.show()
            ledger.move(415,150)
        except Exception as e:
            traceback.print_exc()

    def analyze(self):
        try:
            analysis.show()
            analysis.move(313,150)
        except Exception as e:
            traceback.print_exc()

    def getComboSelection(self):
        text = str(self.comboBox.currentText())
        if text and text is not '':
            return text

    def load(self, data):
       try:
           if data == 'income':
                with open(f'{data}.db', 'r') as f:
                   content = json.load(f)
                   for item in content['Income']:
                       key = list(item.keys())[0]
                       if isinstance(item[key], list):
                           for i in item[key]:

                               keys = list(i.keys())[0]
                               self.income_view.addItem(keys, str(i[keys]))
                       else:
                           self.income_view.addItem(key, str(item[key]))
           elif data == 'expenses':
                with open(f'{data}.db', 'r') as f:
                   content = json.load(f)
                   for item in content['Expenses']:
                       key = list(item.keys())[0]
                       if isinstance(item[key], list):
                           for i in item[key]:
                               keys = list(i.keys())[0]
                               self.expenses_view.addItem(keys, str(i[keys]))
                       else:
                           self.expenses_view.addItem(key, str(item[key]))
           elif data == 'assets':
                with open(f'{data}.db', 'r') as f:
                   content = json.load(f)
                   for item in content['Assets']:
                       key = list(item.keys())[0]
                       if isinstance(item[key], list):
                           for i in item[key]:
                               keys = list(i.keys())[0]
                               self.assets_view.addItem(keys, str(i[keys]))
                       else:
                           self.assets_view.addItem(key, str(item[key]))
           elif data == 'liabilities':
                with open(f'{data}.db', 'r') as f:
                   content = json.load(f)
                   for item in content['Liabilities']:
                       key = list(item.keys())[0]
                       if isinstance(item[key], list):
                           for i in item[key]:
                               keys = list(i.keys())[0]
                               self.liabilities_view.addItem(keys, str(i[keys]))
                       else:
                           self.liabilities_view.addItem(key, str(item[key]))
           elif data == 'opportunities':
                pass
       except Exception:
           traceback.print_exc()
    def save(self, data):
        with open(f'{data}.db', 'w') as file:
            if data == 'income':
                content = json.dump(self.income_model.income, file)
            elif data == 'expenses':
                content = json.dump(self.expense_model.expenses, file)
            elif data == 'assets':
                content = json.dump(self.asset_model.assets, file)
            elif data == 'liabilities':
                content = json.dump(self.liability_model.liabilities, file)
            elif data == 'opportunities':
                content = json.dump(self.opps_model.opportunities, file)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.move(300,100)
window.show()
app.exec_()
