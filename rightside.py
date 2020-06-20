import sys, os
import json, csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QUrl
import traceback

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
        self.add_button.clicked.connect(self.addItem)
        self.set_table_model()
        self.read_in_table()
        self.hide()
    # def add(self):
    #     tmp = self.date.date()
    #     date_ = tmp.toPyDate()
    #     from_ = self.from_account.getComboSelection()
    #     to_ = self.to_account.getComboSelection()
    #     amount_ = self.amount.getText()
    #     notes_ = self.notes.getText()
    #     row = self.display_table.rowCount()
    #     self.display_table.setRowCount(row+1)
    #     row_data = [date_, from_, to_, amount_, notes_]
    #     col = 0
    #     for item in row_data:
    #         cell = QTableWidgetIttem(str(item))
    #         self.display_table.setItem(row, col, cell)
    #         col += 1
    #     self.addItem(date, from_, to_, amount_, notes_)
    def addItem_parms(self, date_of, from_, to_, amount_, notes_):
        row = self.display_table.rowCount()
        self.display_table.setRowCount(row+1)
        row_data = []
        row_data.append(date_of)
        row_data.append(from_)
        row_data.append(to_)
        row_data.append(amount_)
        row_data.append(notes_)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            self.display_table.setItem(row, col, cell)
            col += 1
    def addItem(self):
        date_ = self.date.date().toPyDate()
        from_ = self.from_account.currentText()
        to_ = self.to_account.currentText()
        amount_ = self.amount.text()
        notes_ = self.notes.text()
        row = self.display_table.rowCount()
        self.display_table.setRowCount(row+1)
        row_data = []
        row_data.append(date_)
        row_data.append(from_)
        row_data.append(to_)
        row_data.append(amount_)
        row_data.append(notes_)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            self.display_table.setItem(row, col, cell)
            col += 1
        # self.date.setDate()
        # self.from_account.setItemText('')
        # self.to_account.setItemText('')
        self.amount.setText('')
        self.notes.setText('')
        # self.save()
    def set_table_model(self):
        self.display_table.setColumnCount(5)
        self.display_table.setHorizontalHeaderLabels(['Date','From','To','Amount','Notes'])
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
                    if key != 'Details':
                        details.append(item[key])
                    accounts = []
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            details.append(i[keys])
                    else:
                        if key == 'Notes':
                            details.append(item[key])
                date_ = details[0]
                from_ = details[1]
                to_ = details[2]
                amount_ = details[3]
                notes_ = details[4]
            self.addItem_parms(date_, from_, to_, amount_, notes_)
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
    def save(self):
        pass
        # with open('data/ledger.db', 'w') as file:
            # content = json.dump(self.ledger, file)
class Analysis(QtWidgets.QWidget):
    def __init__(self):
        super(Analysis, self).__init__()
        uic.loadUi('guis/analysis.ui', self)
        self.current_tab = self.findChild(QtWidgets.QTableWidget, 'table_current')
        self.rightside_tab = self.findChild(QtWidgets.QTableWidget, 'table_rightside')
        self.current_tab.check_change = True
        self.rightside_tab.check_change = True
        self.current_tab.cellChanged.connect(self.c_current)
        self.rightside_tab.cellChanged.connect(self.c_rightside)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.open_sheet()
        self.open_rightside()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.hide()
        self.getURLButton.clicked.connect(self.add)
    def add(self):
        try:
            self.webView.load(QUrl(self.urlBox.text()))
        except Exception as e:
            traceback.print_exc()
    def c_rightside(self):
        if self.current_tab.check_change:
            row = self.rightside_tab.currentRow()
            col = self.rightside_tab.currentColumn()
            value = self.rightside_tab.item(row, col)
            value = value.text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)
    def c_current(self):
        if self.current_tab.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)
    def open_rightside(self):
        self.rightside_tab.check_change = False
        url = '/home/tetrapro/projects/python/Rightside_Two.0/rightside.csv'
        with open(url, newline='') as csv_file:
            self.rightside_tab.setRowCount(0)
            self.rightside_tab.setColumnCount(10)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.rightside_tab.rowCount()
                self.rightside_tab.insertRow(row)
                if len(row_data) > 10:
                    self.rightside_tab.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.rightside_tab.setItem(row, column, item)
        self.rightside_tab.check_change = True
    def open_sheet(self):
        self.current_tab.check_change = False
        url = '/home/tetrapro/projects/python/Rightside_Two.0/current.csv'
        with open(url, newline='') as csv_file:
            self.current_tab.setRowCount(0)
            self.current_tab.setColumnCount(10)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.current_tab.rowCount()
                self.current_tab.insertRow(row)
                if len(row_data) > 10:
                    self.current_tab.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.current_tab.setItem(row, column, item)
        self.current_tab.check_change = True
    def save_sheet(self):
        path = QFileDialog.getOpenFileName(self, 'Save CSV', os.getenv('/home/tetrapro/projects/python/Rightside_Two.0'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.current_tab.rowCount()):
                    row_data = []
                    for column in range(self.current_tab.columnCount()):
                        item = self.current_tab.item(row, column)
                        if item is not None:
                            row_data.append(item.next())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            uic.loadUi('guis/financial.ui', self)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            self.opp_small = self.findChild(QtWidgets.QTreeView, 'opportunity_small')
            self.opp_big = self.findChild(QtWidgets.QTreeView, 'opportunity_big')
            self.set_model_income()
            self.set_model_expenses()
            self.set_model_assets()
            self.set_model_liabilities()
            self.set_model_opportunities()
            self.load()
            self.load_exp()
            self.load_assets()
            self.load_debts()
            self.load_small_opps()
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
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        self.opp_small.setModel(QtGui.QStandardItemModel(self))
        self.opp_small.model().setColumnCount(2)
        self.opp_small.setRootIsDecorated(False)
        self.opp_small.setAllColumnsShowFocus(True)
        self.opp_small.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.opp_small.setHeaderHidden(True)
        self.opp_small.header().setStretchLastSection(False)
        self.opp_small.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.opp_small.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.opp_big.setModel(QtGui.QStandardItemModel(self))
        self.opp_big.model().setColumnCount(2)
        self.opp_big.setRootIsDecorated(False)
        self.opp_big.setAllColumnsShowFocus(True)
        self.opp_big.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.opp_big.setHeaderHidden(True)
        self.opp_big.header().setStretchLastSection(False)
        self.opp_big.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.opp_big.header().setSectionResizeMode(
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
    def addItem_Liabilities(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.liabilities.model().appendRow([first, second])
    def addItem_Opps(self, key , value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.opp_small.model().appendRow([first, second])
    def load_small_opps(self):
        try:
            with open('data/small_opps.db', 'r') as f:
                content = json.load(f)
                head_cost = []
                for item in content['Opportunities']:
                    key = list(item.keys())[0]
                    if isinstance(item[key], list):
                        for i in item[key]:
                            keys = list(i.keys())[0]
                            head_cost.append(keys)
                            self.addItem_Opps(keys, str(i[keys]))
                    else:
                        if key != 'Notes':
                            self.addItem_Opps(key, str(item[key]))
                            head_cost.append(key)
        except Exception:
            traceback.print_exc()
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
    def add_account(self):
        account, ok = QInputDialog.getText(self, 'Add New Account', 'Enter the name of new Account: ')
        if ok:
            #~~~~write~~~to~~~file
            with open('data/opportunities.db', 'w') as file:
                json.dump(account, file)
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
