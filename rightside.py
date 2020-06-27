import sys, os
import json, csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QUrl
import traceback
import requests
# import PyPDF2

class Ledger(QtWidgets.QWidget):
    def __init__(self):
        super(Ledger, self).__init__()
        uic.loadUi('guis/ledger.ui', self)
        #set from_accounts = list of expenses read in
        self.date = self.findChild(QtWidgets.QDateEdit, 'date_box')
        self.to_account = self.findChild(QtWidgets.QComboBox, 'to_account')
        self.from_account = self.findChild(QtWidgets.QComboBox, 'from_account')
        self.amount = self.findChild(QtWidgets.QLineEdit, 'amount_box')
        self.notes = self.findChild(QtWidgets.QLineEdit, 'notes_box')
        self.display_table = self.findChild(QtWidgets.QTableView, 'transaction_view')
        self.add_button = self.findChild(QtWidgets.QPushButton, 'add_button')
        self.add_button.clicked.connect(self.addItem)
        self.set_table_model()
        self.read_in_table()
        self.hide()
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
        #~~~~POST~~~~~
        date_ = self.date.date().toPyDate()
        from_ = self.from_account.currentText()
        to_ = self.to_account.currentText()
        amount_ = self.amount.text()
        notes_ = self.notes.text()
        try:
            headers = {"content-type": "application/json"}
            dict = {
                "date": f'{date_}',
                "from_account": f'{from_}',
                "to_account": f'{to_}',
                "amount": f'{amount_}',
                "notes": f'{notes_}'
            }
            data = json.dumps(dict)
            url = 'http://localhost:8000/api/ledger/'
            response = requests.post(url, data=data, headers=headers)
            #~~~~~GET~~~~~
            response2 = requests.get(url)
            json_response = list(response2.json())
            for item in json_response:
                date_of = item['date']
                from_ = item['from_account']
                to_ = item['to_account']
                amount_ = item['amount']
                notes_ = item['notes']
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
            #~~~~~update~expense~~~~~>
            #~~~~> 2 accounts from_ & to_
            url_from = 'http://localhost:8000/api/asset/'
            url_to = 'http://localhost:8000/api/expense/'
            response_from = requests.get(url_from)
            response_to = requests.get(url_to)
            for item in list(response_from.json()):
                if item['source'] == from_:
                    id = item['id']
                    prev_amount = item['cost']
                    old_note = item['notes']
                    update = str(float(prev_amount) - float(amount_))
                    dict_from_post = {
                        "source": from_,
                        "down": update,
                        "cost": update,
                        "notes": old_note
                    }
                    data_post = json.dumps(dict_from_post)
                    response_post = requests.put(url_from+str(id), data=data_post, headers=headers)
            for item in list(response_to.json()):
                if item['source'] == to_:
                    id = item['id']
                    prev_amount = item['amount']
                    update = str(float(prev_amount) + float(amount_))
                    dict_to_post = {
                        "source": to_,
                        "amount" : update
                    }
                    data_post = json.dumps(dict_to_post)
                    response_post = requests.put(url_to+str(id), data=data_post, headers=headers)
            window.sum_exp_accounts()
            window.reload_expenses()
            window.update_display()
        except Exception:
            traceback.print_exc()
        # # self.date.setDate()
        # # self.from_account.setItemText('')
        # # self.to_account.setItemText('')
        self.amount.setText('')
        self.notes.setText('')
    def set_table_model(self):
        self.display_table.setColumnCount(5)
        self.display_table.setHorizontalHeaderLabels(['Date','From','To','Amount','Notes'])
        self.display_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    def read_in_table(self):
        try:
            date_, to_, from_, amount_, notes_ = '', '', '', '', ''
            url = 'http://localhost:8000/api/ledger/'
            response = requests.get(url)
            for item in list(response.json()):
                date_ = item['date']
                from_ = item['from_account']
                to_ = item['to_account']
                amount_ = item['amount']
                notes_ = item['notes']
                self.addItem_parms(date_, from_, to_, amount_, notes_)
        except Exception:
            traceback.print_exc()
class Analysis(QtWidgets.QWidget):
    def __init__(self):
        super(Analysis, self).__init__()
        uic.loadUi('guis/analysis.ui', self)
        self.current_tab = self.findChild(QtWidgets.QTableWidget, 'table_current')
        self.rightside_tab = self.findChild(QtWidgets.QTableWidget, 'table_rightside')
        self.url_OM = self.findChild(QtWidgets.QLineEdit, 'urlBox')
        self.current_tab.check_change = True
        self.rightside_tab.check_change = True
        self.current_tab.cellChanged.connect(self.c_current)
        self.rightside_tab.cellChanged.connect(self.c_rightside)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.open_sheet()
        self.open_rightside()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.hide()
        self.getURLButton.clicked.connect(self.view_deal)
    def view_deal(self):
        try:
            self.webView.load(QUrl(self.urlBox.text()))
            #~~~~~~~~~~start~~analysis~~~~~~~~~~~~
            self.find_data()
        except Exception as e:
            traceback.print_exc()
    def c_rightside(self):
        if self.current_tab.check_change:
            row = self.rightside_tab.currentRow()
            col = self.rightside_tab.currentColumn()
            value = self.rightside_tab.item(row, col)
            # value = value.text()
            # print("The current cell is ", row, ", ", col)
            # print("In this cell we have: ", value)
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
        url = '/home/tetrapro/projects/python/Rightside_Two.0/deals/rightside.csv'
        with open(url, newline='') as csv_file:
            self.rightside_tab.setRowCount(0)
            self.rightside_tab.setColumnCount(10)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.rightside_tab.rowCount()
                self.rightside_tab.insertRow(row)
                if len(row_data) > 10:
                    self.rightside_tab.setColumnCount(len(row_data))
                for column, content in enumerate(row_data):
                    item = QTableWidgetItem(content)
                    self.rightside_tab.setItem(row, column, item)
        self.rightside_tab.check_change = True
    def open_sheet(self):
        self.current_tab.check_change = False
        url = '/home/tetrapro/projects/python/Rightside_Two.0/deals/current.csv'
        with open(url, newline='') as csv_file:
            self.current_tab.setRowCount(0)
            self.current_tab.setColumnCount(10)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.current_tab.rowCount()
                self.current_tab.insertRow(row)
                if len(row_data) > 10:
                    self.current_tab.setColumnCount(len(row_data))
                for column, content in enumerate(row_data):
                    item = QTableWidgetItem(content)
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
    def find_data(self):
        #~~~TASK~~TWO~~2)~~~~~~~~~~~~~~~~~~~>
        #~~bs4~~download~OM~~~~~~~~>
        url = self.urlBox.geext()
        response = requests.get(url)
        with open('pdf_OM.pdf', 'wr') as pdf:
            pdf.write(response.content)
        #~~~scan~~for~text~~~~~~~~~>
        pdf_name = ''
        pdf_file = open(pdf_name, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for i in range(pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            print(page.extractText())
class Asset(QtWidgets.QWidget):
    def __init__(self):
        super(Asset, self).__init__()
        uic.loadUi('guis/asset.ui', self)
        self.type_in = self.findChild(QtWidgets.QComboBox, 'type_input')
        self.down_in = self.findChild(QtWidgets.QLineEdit, 'down_input')
        self.cost_in = self.findChild(QtWidgets.QLineEdit, 'cost_input')
        self.pymt = self.findChild(QtWidgets.QLineEdit, 'payment_input')
        self.notes = self.findChild(QtWidgets.QLineEdit, 'notes_input')
        self.cash_flow_in = self.findChild(QtWidgets.QLineEdit, 'cashflow_input')
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'ok_button')
        self.cancel_button = self.findChild(QtWidgets.QPushButton, 'cancel_button')
        self.ok_button.clicked.connect(self.ok)
        self.cancel_button.clicked.connect(self.cancel)
    def ok(self):
        type = self.type_in.currentText()
        down = self.down_in.text()
        cost = self.cost_in.text()
        pymt= self.pymt.text()
        note = self.notes.text()
        cash_flow = self.cash_flow_in.text()
        mortgage = float(cost) - float(down)
        #~~~~~~~save~to~~database~~~~~~>
        try:
            headers = {"content-type": "application/json"}
            dict = {
                "source" : f'{type}',
                "down" : f'{down}',
                "cost" : f'{cost}',
                "notes" : f'{note}'
            }
            data = json.dumps(dict)
            url = 'http://localhost:8000/api/asset/'
            response = requests.post(url, data=data, headers=headers)
            #~~~~~~update~income~as~well~~~~~>
            url2 = 'http://localhost:8000/api/income/'
            dict2 = {
                "source": f'{type}',
                "amount": f'{cash_flow}',
                "notes": f'{note}',
            }
            data2 = json.dumps(dict2)
            response2 = requests.post(url2, data=data2, headers=headers)
            #~~~~~~~~~~~~~liability~~~~~~~~~~~>
            #~~~~~~~~>
            url3 = 'http://localhost:8000/api/liability/'
            if type == 'Real Estate':
                type = 'RE Mortgages'
            elif type =='Business':
                type = 'Business Debts'
            dict3 = {
                "source" : f'{type}',
                "amount" : f'{mortgage}',
                "notes" : f'{note}'
            }
            data3 = json.dumps(dict3)
            response3 = requests.post(url3, data=data3, headers=headers)
            #~~~~~~~~~~~~~~~~expense~~~~~~~~~~>
            #~~~~~~~~>
            id = 0
            url4 = 'http://localhost:8000/api/expense/'
            response_get = requests.get(url4).json()
            prev_amount = 0.0
            for item in list(response_get):
                if item['source'] == 'RE Debt Service':
                     id = item['id']
                     prev_amount = item['amount']
            updated = float(pymt) + float(prev_amount)
            dict4 = {
                "source" : 'RE Debt Service',
                "amount" : f'{updated}'
            }
            data4 = json.dumps(dict4)
            response4 = requests.put(url4+str(id), data=data4, headers=headers)
            #~~~~~~~~~~~~why~not~just~get(url)~~~~~>
            #~~~~~~~~~>I think this is not best...
            #should call post api then get all
            window.reload_income()
            window.reload_expenses()
            window.reload_assets()
            window.reload_liabilities()
            window.update_display()
        except Exception:
            traceback.print_exc()
        #~~~~~~~~~~clean~up~fields~~~~~>
        down = self.down_in.setText('')
        cost = self.cost_in.setText('')
        cash_flow = self.cash_flow_in.setText('')
        self.hide()
    def cancel(self):
        self.hide()
class SellAsset(QtWidgets.QWidget):
    def __init__(self):
        super(SellAsset, self).__init__()
        uic.loadUi('guis/sell_asset.ui', self)
        self.asset = self.findChild(QtWidgets.QComboBox, 'asset_combobox')
        self.price = self.findChild(QtWidgets.QLineEdit, 'price_sold')
        self.sell_button = self.findChild(QtWidgets.QPushButton, 'sell_button')
        self.cancel_button = self.findChild(QtWidgets.QPushButton, 'cancel_button')
        self.sell_button.clicked.connect(self.sell)
        self.cancel_button.clicked.connect(self.cancel)
        response = requests.get('http://localhost:8000/api/asset/')
        content = []
        for item in list(response.json()):
            content.append(item['notes'])
        self.asset.addItems(content)
    def sell(self):
        asset_note = self.asset.currentText()
        price = self.price.text()
        self.remove('income', asset_note)
        # self.remove('expense', '')
        self.remove('asset', asset_note)
        self.remove('liability', asset_note)
        #~~~~~>
        window.reload_income()
        window.reload_assets()
        # window.reload_expenses()
        window.reload_liabilities()
        window.update_display()
        #~~~~~~~~~~clean~up~fields~~~~~>
        self.price_sold.setText('')
        self.hide()
    def cancel(self):
        self.hide()
    def remove(self, account, notes):
        url = 'http://localhost:8000/api/'+account+'/'
        response = requests.get(url)
        id = ''
        for item in list(response.json()):
            if item['notes'] == notes:
                id = str(item['id'])
        response_del = requests.delete(url+id)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            uic.loadUi('guis/financial.ui', self)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.sum_passive = 0.0
            self.sum_salaries = 0.0
            self.sum_expenses = 1.0
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
            self.sum_exp_accounts()
            self.load()
            self.load_exp()
            self.load_assets()
            self.load_debts()
            self.load_small_opps()
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #connect button actions
            self.asset = self.findChild(QtWidgets.QPushButton, 'add_asset')
            self.asset.clicked.connect(self.addAsset)
            self.sell_a_asset = self.findChild(QtWidgets.QPushButton, 'liquidate_asset')
            self.sell_a_asset.clicked.connect(self.sellit)
            self.analyze_it = self.findChild(QtWidgets.QPushButton, 'analyze_button')
            self.analyze_it.clicked.connect(self.analyze)
            self.add_transaction = self.findChild(QtWidgets.QPushButton, 'add_transaction')
            self.add_transaction.clicked.connect(self.addTransaction)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #add up passive incomes
            self.total_passive = self.findChild(QtWidgets.QLabel, 'total_passive')
            self.total_income = self.findChild(QtWidgets.QLabel, 'total_income')
            self.total_expenses = self.findChild(QtWidgets.QLabel, 'total_expenses')
            self.total_cashflow = self.findChild(QtWidgets.QLabel, 'total_cashflow')
            self.goal_percent = self.findChild(QtWidgets.QProgressBar, 'goal_percent')
            self.worth = self.findChild(QtWidgets.QLabel, 'networth_label')
            self.total_passive.setText('{0:,.2f}'.format(self.sum_passive))
            self.total_expenses.setText('{0:,.2f}'.format(self.sum_expenses))
            self.total_cashflow.setText('{0:,.2f}'.format((self.sum_salaries+self.sum_passive)-self.sum_expenses))
            self.percent = self.sum_passive/self.sum_expenses*100
            if self.percent >= 100:
                self.goal_percent.setValue(int(100))
                self.statusBar().showMessage('YOU ARE FREE! FINANCIALLY FREE! GREAT JOB!!')
            else:
                self.goal_percent.setValue(int(self.percent))
            self.worth.setText(' $'+'{0:,.0f}'.format(self.sum_assets-self.sum_debts))
            #~~~~~~set~deal~details on click~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.opp_small.clicked.connect(self.see_details)
            self.opp_big.clicked.connect(self.see_details)
            self.opp_title = self.findChild(QtWidgets.QLabel, 'label')
            self.opp_body = self.findChild(QtWidgets.QTextEdit, 'card_details')
            self.opp_buy = self.findChild(QtWidgets.QPushButton, 'buy_button')
            self.opp_assign = self.findChild(QtWidgets.QPushButton, 'assign_button')
            self.opp_cost = self.findChild(QtWidgets.QLabel, 'cost_value')
            self.opp_down = self.findChild(QtWidgets.QLabel, 'down_display')
            self.opp_mortgage = self.findChild(QtWidgets.QLabel, 'mortgage_value')
            self.opp_cash_flow = self.findChild(QtWidgets.QLabel, 'cashflow_display')
            self.opp_coc = self.findChild(QtWidgets.QLabel, 'coc_display')
            self.opp_irr = self.findChild(QtWidgets.QLabel, 'irr_display')
        except Exception:
            traceback.print_exc()
    def update_display(self):
        #clear all first...~~~~>
        #reload~~~~~~>
        self.total_passive.setText('{0:,.2f}'.format(self.get_total_passive()))
        self.total_expenses.setText('{0:,.2f}'.format(self.get_total_expense()))
        self.total_cashflow.setText('{0:,.2f}'.format(self.get_total_income()[0]-self.get_total_expense()))
        self.total_passive.setText('{0:,.2f}'.format(self.get_total_income()[1]))
        self.total_income.setText('{0:,.2f}'.format(self.get_total_income()[0]))
        self.total_expenses.setText('{0:,.2f}'.format(self.get_total_expenses()))
        self.total_cashflow.setText('{0:,.2f}'.format(self.get_total_income()[0]-self.get_total_expenses()))
        self.percent = self.sum_passive/self.sum_expenses*100
        if self.percent >= 100:
            self.goal_percent.setValue(int(100))
            self.statusBar().showMessage('YOU ARE FREE! FINANCIALLY FREE! GREAT JOB!!')
        else:
            self.goal_percent.setValue(int(self.percent))
        self.worth.setText(' $'+'{0:,.0f}'.format(self.sum_assets-self.sum_debts))

        self.worth.setText(' $'+'{0:,.0f}'.format(self.get_total_assets()-self.get_total_liabilities()))
    def addAsset(self):
        self.asset = Asset()
        self.asset.move(675,150)
        self.asset.show()
    def sellit(self):
        self.selling = SellAsset()
        self.selling.move(675,150)
        self.selling.show()
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
    def reload_income(self):
        self.income.model().removeRows(0, self.income.model().rowCount())
        self.load()
    def reload_expenses(self) :
        self.expenses.model().removeRows(0, self.expenses.model().rowCount())
        self.load_exp()
    def reload_assets(self):
        self.assets.model().removeRows(0, self.assets.model().rowCount())
        self.load_assets()
    def reload_liabilities(self):
        self.liabilities.model().removeRows(0, self.liabilities.model().rowCount())
        self.load_debts()
    def load_small_opps(self):
        try:
            url = 'http://localhost:8000/api/opportunity/'
            response = requests.get(url)
            for item in list(response.json()):
                self.addItem_Opps(item['heading'], item['description'])
        except Exception:
            traceback.print_exc()
    def load_debts(self):
        try:
            url = 'http://localhost:8000/api/liability/'
            response = requests.get(url)
            for item in list(response.json()):
                self.addItem_Liabilities(item['source']+' - '+item['notes'],  '{0:,.0f}'.format(float(item['amount'])))
                self.sum_debts += float(item['amount'])
        except Exception:
            traceback.print_exc()
    def load_assets(self):
        try:
            url = 'http://localhost:8000/api/asset/'
            response = requests.get(url)
            for item in list(response.json()):
                self.addItem_Assets(item['source']+' - '+item['notes'], '{0:,.0f}'.format(float(item['cost'])))
                self.sum_assets += float(item['cost'])
        except Exception:
            traceback.print_exc()
    def load_exp(self):
        try:
            url = 'http://localhost:8000/api/expense/'
            response = requests.get(url)
            for item in list(response.json()):
                self.addItem_Expenses(item['source'], '{0:,.0f}'.format(float(item['amount'])))
                self.sum_expenses += float(item['amount'])
        except Exception:
            traceback.print_exc()
    def load(self):
       try:
           url = 'http://localhost:8000/api/income/'
           response = requests.get(url)
           for item in list(response.json()):
               self.addItem_income(item['source']+' - '+item['notes'],  '{0:,.0f}'.format(float(item['amount'])))
               if item['source'] == 'Salary/Wages':
                   self.sum_salaries += float(item['amount'])
               if item['source'] != 'Salary/Wages':
                   self.sum_passive += float(item['amount'])
           self.total_income.setText('{0:,.2f}'.format(self.sum_salaries+self.sum_passive))
       except Exception:
           traceback.print_exc()
    def see_details(self):
        content = []
        for ix in self.opp_small.selectedIndexes():
            content.append(ix.data()) # or ix.data()
        url = 'http://localhost:8000/api/opportunity/'
        response = requests.get(url)
        res_details = []
        for item in list(response.json()):
            if item['heading'] == content[0] and item['description'] == content[1]:
                res_details = requests.get(url+str(item['id']))
        self.opp_title.setText(res_details.json()['heading'])
        self.opp_body.setText(res_details.json()['description'])
        self.opp_cost.setText('{0:,.0f}'.format(float(res_details.json()['cost'])))
        self.opp_down.setText('{0:,.0f}'.format(float(res_details.json()['down'])))
        self.opp_mortgage.setText('{0:,.0f}'.format(float(res_details.json()['mortgage'])))
        self.opp_cash_flow.setText('{0:,.0f}'.format(float(res_details.json()['cash_flow'])))
        self.opp_coc.setText(res_details.json()['coc'])
        self.opp_irr.setText(res_details.json()['irr'])
    def get_new_account(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter Account:')
        if text and text != '':
            return text
    def add_account(self):
        #Asset or Expense Account?
        account, ok = QInputDialog.getText(self, 'Add New Account', 'Enter the name of new Account: ')
        if ok:
            print(account)
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
    def get_total_income(self):
        url = 'http://localhost:8000/api/income/'
        response = requests.get(url)
        total = 0.0
        for item in list(response.json()):
            total += float(item['amount'])
        return total
    def get_total_passive(self):
        total = self.get_total_income()
        url = 'http://localhost:8000/api/income/'
        response = requests.get(url)
        wages = 0.0
        for item in list(response.json()):
            if item['source'] == 'Salary/Wages':
                clock_time += float(item['amount'])
        passive = float(total[0]) - wages
        return passive
    def get_total_expense(self):
        url = 'http://localhost:8000/api/expense/'
        response = requests.get(url)
        total = 0.0
        for item in list(response.json()):
            total += float(item['amount'])
        return total
    def get_total_asset(self):
        url = 'http://localhost:8000/api/asset/'
        response = requests.get(url)
        total = 0.0
        for item in list(response.json()):
            total += float(item['cost'])
        return total
    def get_total_liability(self):
        url = 'http://localhost:8000/api/liability/'
        response = requests.get(url)
        total = 0.0
        for item in list(response.json()):
            total += float(item['amount'])
        return total
    def get_total_income(self):
        '''returns a tuple with total income & passive'''
        income = 0
        passive = 0
        url = 'http://localhost:8000/api/income/'
        response = requests.get(url)
        for item in list(response.json()):
            income += int(item['amount'])
            if item['source'] == 'Salary/Wages':
                passive += int(item['amount'])
        return (income, passive)
    def get_total_expenses(self):
        '''returns an int value of the sum total of expenses'''
        expense = 0
        url = 'http://localhost:8000/api/expense/'
        response = requests.get(url)
        for item in list(response.json()):
            expense += int(float(item['amount']))
        return expense
    def get_total_assets(self):
        '''returns an int value of the sum total of assets'''
        assets = 0.0
        url = 'http://localhost:8000/api/asset/'
        response = requests.get(url)
        for item in list(response.json()):
            assets += float(item['cost'])
        return assets
    def get_total_liabilities(self):
        '''returns an int value of the sum total of liabilities'''
        liabilities = 0.0
        url = 'http://localhost:8000/api/liability/'
        response = requests.get(url)
        for item in list(response.json()):
            liabilities += float(item['amount'])
        return liabilities
    def get_exp_id(self, exp_account):
        #~~~~~~need~the~id~~~~~~>
        url_put = 'http://localhost:8000/api/expense/'
        response_id = requests.get(url_put)
        id = 0
        for item_ in list(response_id.json()):
            if item_['source'] == exp_account:
                id = item_['id']
                return id
        return id
    def sum_exp_accounts(self):
        data_dict = {
            "Mortgage/Rent" : 0,
            "Utilities" : 0,
            "Insurance" : 0,
            "Health/Wellness" : 0,
            "Food/Groceries" : 0,
            "Vehicle(s)" : 0,
            "Entertainment" : 0,
            "Clothing" : 0,
            "Furniture" : 0,
            "Donations/Charity" : 0,
            "Taxes" : 0,
            "Fees/Fines" : 0,
            "Other" : 0,
            "RE Debt Service": 0
        }
        url = 'http://localhost:8000/api/ledger/'
        response = requests.get(url)
        for item in list(response.json()):
            if item['to_account'] == 'Mortgage/Rent':
                data_dict['Mortgage/Rent'] += float(item['amount'])
            elif item['to_account'] == 'Utilities':
                data_dict['Utilities'] += float(item['amount'])
            elif item['to_account'] == 'Insurance':
                data_dict['Insurance'] += float(item['amount'])
            elif item['to_account'] == 'Health/Wellness':
                data_dict['Health/Wellness'] += float(item['amount'])
            elif item['to_account'] == 'Vehicle(s)':
                data_dict['Vehicle(s)'] += float(item['amount'])
            elif item['to_account'] == 'Food/Groceries':
                data_dict['Food/Groceries'] += float(item['amount'])
            elif item['to_account'] == 'Entertainment':
                data_dict['Entertainment'] += float(item['amount'])
            elif item['to_account'] == 'Clothing':
                data_dict['Clothing'] += float(item['amount'])
            elif item['to_account'] == 'Furniture':
                data_dict['Furniture'] += float(item['amount'])
            elif item['to_account'] == 'Donations/Charity':
                data_dict['Donations/Charity'] += float(item['amount'])
            elif item['to_account'] == 'Taxes':
                data_dict['Taxes'] += float(item['amount'])
            elif item['to_account'] == 'Fees/Fines':
                data_dict['Fees/Fines'] += float(item['amount'])
            elif item['to_account'] == 'Other':
                data_dict['Other'] += float(item['amount'])
            elif item['to_account'] == 'RE Debt Service':
                data_dict['RE Debt Service'] += float(item['amount'])
        for key, value in enumerate(list(data_dict)):
            data_dict[value] = str(data_dict[value])
        #~~need~a~for-loop~then~put~each~one~in~expense~~~>
        put_data = {
            "source": '',
            "amount": ''
        }
        data = ''
        id = 0
        # print(data_dict)
        #~~~~~~~~~~~~~~~~~~~~~~~>
        url_put = 'http://localhost:8000/api/expense/'
        for item in data_dict:
            put_data['source'] = item
            put_data['amount'] = data_dict[item]
            data = json.dumps(put_data)
            id = self.get_exp_id(item)
            print(id, data)
            #~~~~~~~~~this~is~not~working~~~~~~~~~>
            #~~~~~>
            if id != 0:
                headers = {"content-type": "application/json"}
                response_post = requests.put(url_put+str(id), data=data, headers=headers)
                if response_post.status_code == 405 or 404:
                    print('problem here:...#:832')
                    # response_post = requests.post(url_put, data=data, headers=headers)
            else:
                response_post = requests.post(url_put, data=data, headers=headers)
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
ledger = Ledger()
analysis = Analysis()
window.move(300,50)
window.move(300,75)
window.show()
app.exec_()
