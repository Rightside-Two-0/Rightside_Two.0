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
        self.sum_passive = 0.0
        self.sum_salaries = 0.0
        self.sum_expenses = 0.0
        self.sum_assets = 0.0
        self.sum_debts = 0.0
        self.income = self.findChild(QtWidgets.QTreeView, 'income_view')
        self.expenses = self.findChild(QtWidgets.QTreeView, 'expenses_view')
        self.assets = self.findChild(QtWidgets.QTreeView, 'assets_view')
        self.liabilities = self.findChild(QtWidgets.QTreeView, 'liabilities_view')
        self.opportunities = self.findChild(QtWidgets.QTreeView, 'opportunity_view')
        self.set_model_income()
        self.set_model_expenses()
        self.set_model_assets()
        self.set_model_liabilities()
        self.set_model_opportunities()
        self.load()
        self.load_exp()
        self.load_assets()
        self.load_debts()
        self.load_opps()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #connect button actions
        self.analyze = self.findChild(QtWidgets.QPushButton, 'analyze_button')
        self.analyze.clicked.connect(self.analyze_it)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #add up passive incomes
        self.total_passive = self.findChild(QtWidgets.QLabel, 'total_passive')
        self.total_passive.setText(str(self.sum_passive))
        self.total_income = self.findChild(QtWidgets.QLabel, 'total_income')
        self.total_income.setText(str(self.sum_salaries+self.sum_passive))
        self.total_expenses = self.findChild(QtWidgets.QLabel, 'total_expenses')
        self.total_expenses.setText(str(self.sum_expenses))
        self.total_cashflow = self.findChild(QtWidgets.QLabel, 'total_cashflow')
        self.total_cashflow.setText(str((self.sum_salaries+self.sum_passive)-self.sum_expenses))



    def set_model_income(self):
        self.income.setModel(QtGui.QStandardItemModel(self))
        self.income.model().setColumnCount(2)
        self.income.setRootIsDecorated(False)
        self.income.setAllColumnsShowFocus(True)
        self.income.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.income.setHeaderHidden(True)
        self.income.header().setStretchLastSection(False)
        self.income.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.income.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
    def set_model_expenses(self):
        self.expenses.setModel(QtGui.QStandardItemModel(self))
        self.expenses.model().setColumnCount(2)
        self.expenses.setRootIsDecorated(False)
        self.expenses.setAllColumnsShowFocus(True)
        self.expenses.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.expenses.setHeaderHidden(True)
        self.expenses.header().setStretchLastSection(False)
        self.expenses.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.expenses.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
    def set_model_assets(self):
        self.assets.setModel(QtGui.QStandardItemModel(self))
        self.assets.model().setColumnCount(2)
        self.assets.setRootIsDecorated(False)
        self.assets.setAllColumnsShowFocus(True)
        self.assets.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.assets.setHeaderHidden(True)
        self.assets.header().setStretchLastSection(False)
        self.assets.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.assets.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
    def set_model_liabilities(self):
        self.liabilities.setModel(QtGui.QStandardItemModel(self))
        self.liabilities.model().setColumnCount(2)
        self.liabilities.setRootIsDecorated(False)
        self.liabilities.setAllColumnsShowFocus(True)
        self.liabilities.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.liabilities.setHeaderHidden(True)
        self.liabilities.header().setStretchLastSection(False)
        self.liabilities.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.liabilities.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
    def set_model_opportunities(self):
        self.opportunities.setModel(QtGui.QStandardItemModel(self))
        self.opportunities.model().setColumnCount(2)
        self.opportunities.setRootIsDecorated(False)
        self.opportunities.setAllColumnsShowFocus(True)
        self.opportunities.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.opportunities.setHeaderHidden(True)
        self.opportunities.header().setStretchLastSection(False)
        self.opportunities.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.opportunities.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
    def addItem_income(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.income.model().appendRow([first, second])
    def addItem_Expenses(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.expenses.model().appendRow([first, second])
    def addItem_Assets(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.assets.model().appendRow([first, second])
    def addItem_Liabilities(self,key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.liabilities.model().appendRow([first, second])
    def load_opps(self):
        pass
    def load_debts(self):
        try:
            with open('liabilities.db', 'r') as f:
                content = json.load(f)
                for item in content['Liabilities']:
                    key = list(item.keys())[0]
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            self.addItem_Liabilities(keys, str(i[keys]))
                    else:
                        self.addItem_Liabilities(key, str(item[key]))
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
                            self.addItem_Assets(keys, str(i[keys]))
                    else:
                        self.addItem_Assets(key, str(item[key]))
        except Exception:
            traceback.print_exc()
    def load_exp(self):
        try:
            with open('expenses.db', 'r') as f:
                content = json.load(f)
                for item in content['Expenses']:
                    key = list(item.keys())[0]
                    self.addItem_Expenses(key, str(item[key]))
                    self.sum_expenses += float(item[key])
        except Exception:
            traceback.print_exc()
    def load(self):
       try:
           with open('income.db', 'r') as f:
               content = json.load(f)
               for item in content['Income']:
                   key = list(item.keys())[0]
                   if key == 'Salary/Wages':
                       self.sum_salaries += float(item[key])
                   if isinstance(item[key], list):
                       for i in item[key]:
                           keys = list(i.keys())[0]
                           self.addItem_income(keys, str(i[keys]))
                           if keys != 'Salary/Wages':
                               self.sum_passive += float(i[keys])
       except Exception:
           traceback.print_exc()
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
