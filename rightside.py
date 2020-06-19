import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import traceback

analysis_view, QtBaseClass = uic.loadUiType('guis/analysis.ui')
class Ledger(QtWidgets.QWidget):
    def __init__(self):
        super(Ledger, self).__init__()
        uic.loadUi('guis/ledger.ui', self)
        #set from_accounts = list of expenses read in
        self.date = self.findChild(QtWidgets.QDateEdit, 'date_box')
        self.to_accounts = self.load_to_accounts()
        self.from_accounts = self.load_from_accounts()
        self.to_account = self.findChild(QtWidgets.QComboBox, 'to_account')
        self.from_account = self.findChild(QtWidgets.QComboBox, 'from_account')
        self.to_account.addItems(self.to_accounts)
        self.from_account.addItems(self.from_accounts)
        self.amount = self.findChild(QtWidgets.QLineEdit, 'amount_box')
        self.notes = self.findChild(QtWidgets.QLineEdit, 'notes_box')
        self.display_table = self.findChild(QtWidgets.QTableView, 'transaction_view')
        self.add_button = self.findChild(QtWidgets.QPushButton, 'add_button')
        self.add_button.clicked.connect(self.add)
        self.set_table_model()
        self.read_in_table()
        self.hide()
    def add(self):
        tmp = self.date.date()
        date_ = tmp.toPyDate()
        from_ = self.from_account.getComboSelection()
        to_ = self.to_account.getComboSelection()
        amount_ = self.amount.getText()
        notes_ = self.notes.getText()
        
        self.addItem(date, from_, to_, amount_, notes_)
    def addItem(self, date, from_a, to_a, amount, notes):
        date_ = QtGui.QStandardItem(date)
        from_ = QtGui.QStandardItem(from_a)
        to_ = QtGui.QStandardItem(to_a)
        amount_ = QtGui.QStandardItem(amount)
        notes_ = QtGui.QStandardItem(notes)
        date_.setTextAlignment(QtCore.Qt.AlignRight)
        from_.setTextAlignment(QtCore.Qt.AlignRight)
        to_.setTextAlignment(QtCore.Qt.AlignRight)
        amount_.setTextAlignment(QtCore.Qt.AlignRight)
        notes_.setTextAlignment(QtCore.Qt.AlignRight)
        self.display_table.model().appendRow([date_, from_, to_, amount_, notes_])
    def set_table_model(self):
        self.display_table.setModel(QtGui.QStandardItemModel(self))
        self.display_table.model().setColumnCount(5)
        self.display_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    def read_in_table(self):
        try:
            content = []
            date_, to_, from_, amount_, notes_ = '', '', '', '', ''
            with open('data/ledger.db', 'r') as ledger:
                content = json.load(ledger)
                details = []
                for item in content['Ledger']:
                    key = list(item.keys())[0]
                    details.append(key)
                    details.append(item[key])
                    accounts = []
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            accounts.append(keys)
                            accounts.append(i[keys])
                        date_ = accounts[1]
                        from_ = accounts[3]
                        to_ = accounts[5]
                        amount_ = str(accounts[7])
                        notes_ = accounts[9]
                    self.addItem(date_, from_, to_, amount_, notes_)
        except Exception:
            traceback.print_exc()
    def load_to_accounts(self):
        try:
            with open('data/expenses.db', 'r') as f:
                content = json.load(f)
                accounts = []
                for item in content['Expenses']:
                    key = list(item.keys())[0]
                    accounts.append(key)
                return accounts
        except Exception:
            traceback.print_exc()
    def load_from_accounts(self):
        try:
            with open('data/assets.db', 'r') as f:
                content = json.load(f)
                accounts = []
                for item in content['Assets']:
                    key = list(item.keys())[0]
                    accounts.append(key)
                return accounts
        except Exception:
            traceback.print_exc()
class Analysis(QtWidgets.QWidget, analysis_view):
    def __init__(self):
        super(Analysis, self).__init__()
        self.setupUi(self)
        self.hide()
        self.getURLButton.clicked.connect(self.add)
    def add(self):
        try:
            self.webView.load(QUrl(self.urlBox.text()))
        except Exception as e:
            traceback.print_exc()
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            uic.loadUi('guis/financial.ui', self)
            self.sum_passive = 0.0
            self.sum_salaries = 0.0
            self.sum_expenses = 0.0
            self.sum_assets = 0.0
            self.sum_debts = 0.0
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #setting popup action to add new account to ledger to or from accoutns
            self.new_account = self.findChild(QtWidgets.QAction, 'account_mentu_item')
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
            self.analyze_it = self.findChild(QtWidgets.QPushButton, 'analyze_button')
            self.analyze_it.clicked.connect(self.analyze)
            self.add_transaction = self.findChild(QtWidgets.QPushButton, 'add_transaction')
            self.add_transaction.clicked.connect(self.addTransaction)
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
            self.goal_percent = self.findChild(QtWidgets.QProgressBar, 'goal_percent')
            self.percent = self.sum_passive/self.sum_expenses*100
            self.goal_percent.setValue(int(self.percent))
        except Exception:
            traceback.print_exc()

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
            with open('data/liabilities.db', 'r') as f:
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
            with open('data/assets.db', 'r') as f:
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
            with open('data/expenses.db', 'r') as f:
                content = json.load(f)
                for item in content['Expenses']:
                    key = list(item.keys())[0]
                    self.addItem_Expenses(key, str(item[key]))
                    self.sum_expenses += float(item[key])
        except Exception:
            traceback.print_exc()
    def load(self):
       try:
           with open('data/income.db', 'r') as f:
               content = json.load(f)
               for item in content['Income']:
                   key = list(item.keys())[0]
                   if key == 'Salary/Wages':
                       self.sum_salaries += float(item[key])
                       self.addItem_income(key, str(item[key]))
                       if isinstance(item[key], list):
                           for i in item[key]:
                               keys = list(i.keys())[0]
                               self.addItem_income(keys, str(i[keys]))
                   if key != 'Salary/Wages':
                       keys = list(item.keys())[0]
                       if not isinstance(item[keys], list):
                           self.addItem_income(keys, str(item[keys]))
                       if isinstance(item[key], list):
                            for i in item[key]:
                                keys = list(i.keys())[0]
                                self.addItem_income(keys, str(i[keys]))
                                if keys != 'Salary/Wages':
                                    self.sum_passive += float(i[keys])

       except Exception:
           traceback.print_exc()
    def get_new_account(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter Account:')
        if text and text != '':
            return text

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
    def save(self, data):
        with open(f'data/{data}.db', 'w') as file:
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
            elif data == 'ledger':
                content = json.dump(self.opps_model.opportunities, file)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
ledger = Ledger()
analysis = Analysis()
window.move(300,100)
window.show()
app.exec_()
