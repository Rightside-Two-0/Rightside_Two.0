import sys, os
import json, csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import Qt, QUrl
from tests.calc_irr import mortgage
from tests.calc_irr import calc_irr

import traceback
import requests

# import PyPDF4

class Ledger(QtWidgets.QWidget):
    def __init__(self):
        super(Ledger, self).__init__()
        uic.loadUi('guis/ledger.ui', self)
        self.base_url = 'http://localhost:8000/api/ledger/'
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
            response = requests.post(self.base_url, data=data, headers=headers)
            # #~~~~~GET~~~~~
            response2 = requests.get(self.base_url)
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
            window.reload_expenses()
            window.reload_assets()
            window.update_display()
            self.hide()
        except Exception:
            traceback.print_exc()
        # # self.date.setDate()
        # # self.from_account.setItemText('')
        # # self.to_account.setItemText('')
        self.amount.setText('')
        self.notes.setText('')
    def set_table_model(self):
        self.display_table.setColumnCount(5)
        header = self.display_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
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
        self.irr = None
        self.current_tab = self.findChild(QtWidgets.QTableWidget, 'table_current')
        self.rightside_tab = self.findChild(QtWidgets.QTableWidget, 'table_rightside')
        self.url_OM = self.findChild(QtWidgets.QLineEdit, 'urlBox')
        #~~~~~income~~~~~~~~~~~~~~~~~~~~~>
        #~~~~~>
        self.asking = self.findChild(QtWidgets.QLineEdit, 'ask_display')
        self.sqft = self.findChild(QtWidgets.QLineEdit, 'sqft_display')
        self.units = self.findChild(QtWidgets.QLineEdit, 'num_units_display')
        self.monthly_rent = self.findChild(QtWidgets.QLineEdit, 'ave_monthly_rent_display')
        self.vacancy = self.findChild(QtWidgets.QLineEdit, 'vacancy_rate_display')
        self.other_income = self.findChild(QtWidgets.QLineEdit, 'other_income_display')
        self.gross_income = self.findChild(QtWidgets.QLabel, 'gross_income_display')
        #~~~~~expenses~~~~~~~~~~~~~~~~~~~~>
        #~~~~~>
        self.repairs = self.findChild(QtWidgets.QLineEdit, 'repairs_display')
        self.management = self.findChild(QtWidgets.QLineEdit, 'management_display')
        self.taxes = self.findChild(QtWidgets.QLineEdit, 'taxes_display')
        self.insurance = self.findChild(QtWidgets.QLineEdit, 'insurance_display')
        self.wages = self.findChild(QtWidgets.QLineEdit, 'wages_display')
        self.utilities = self.findChild(QtWidgets.QLineEdit, 'utilities_display')
        self.gen_admin = self.findChild(QtWidgets.QLineEdit, 'gen_admin_display')
        self.professional_fees = self.findChild(QtWidgets.QLineEdit, 'professional_fees_display')
        self.advertising = self.findChild(QtWidgets.QLineEdit, 'advertising_display')
        self.capital_reserves = self.findChild(QtWidgets.QLineEdit, 'cap_x_display')
        self.other = self.findChild(QtWidgets.QLineEdit, 'other_expense_display')
        self.total_expense = self.findChild(QtWidgets.QLabel, 'total_expense_display')
        #~~~~~>progressbars...
        self.repairsProgress = self.findChild(QtWidgets.QProgressBar, 'repairs_progressBar')
        self.managementProgress = self.findChild(QtWidgets.QProgressBar, 'management_progressBar')
        self.taxesProgress = self.findChild(QtWidgets.QProgressBar, 'taxes_progressBar')
        self.insuranceProgress = self.findChild(QtWidgets.QProgressBar, 'insurance_progressBar')
        self.wagesProgress = self.findChild(QtWidgets.QProgressBar, 'wages_progressBar')
        self.utilitiesProgress = self.findChild(QtWidgets.QProgressBar, 'utilities_progressBar')
        self.gen_adminProgress = self.findChild(QtWidgets.QProgressBar, 'gen_admin_progressBar')
        self.professional_feesProgress = self.findChild(QtWidgets.QProgressBar, 'professional_fees_progressBar')
        self.advertisingProgress = self.findChild(QtWidgets.QProgressBar, 'advertising_progressBar')
        self.capital_reservesProgress = self.findChild(QtWidgets.QProgressBar, 'cap_x_progressBar')
        self.otherProgress = self.findChild(QtWidgets.QProgressBar, 'other_progressBar')
        #~~~noi~~~~~~~>
        self.noi = self.findChild(QtWidgets.QLabel, 'noi_display')
        #~~~~~financing~~~~~~~~~~~~~~~~~~~~>
        #~~~~~>
        self.total_purhcase = self.findChild(QtWidgets.QLineEdit, 'total_purchase_display')
        self.financing = self.findChild(QtWidgets.QLineEdit, 'financing_display')
        self.seller_carry = self.findChild(QtWidgets.QLineEdit, 'seller_carry_display')
        self.down = self.findChild(QtWidgets.QLineEdit, 'down_display')
        self.closing_costs = self.findChild(QtWidgets.QLineEdit, 'closing_costs_display')
        self.financing_rate = self.findChild(QtWidgets.QLineEdit, 'financing_rate_lineEdit')
        self.financing_term = self.findChild(QtWidgets.QLineEdit, 'financing_term_lineEdit')
        self.seller_carry_rate = self.findChild(QtWidgets.QLineEdit, 'seller_carray_rate_lineEdit')
        self.seller_carry_term = self.findChild(QtWidgets.QLineEdit, 'seller_carry_term_lineEdit')
        self.financing_payment = self.findChild(QtWidgets.QLabel, 'financing_payment_display')
        self.seller_carry_payment = self.findChild(QtWidgets.QLabel, 'seller_carray_display')
        self.financing_progressBar = self.findChild(QtWidgets.QProgressBar, 'financing_progressBar')
        self.seller_carray_progressBar = self.findChild(QtWidgets.QProgressBar, 'seller_carray_progressBar')
        self.down_progressBar = self.findChild(QtWidgets.QProgressBar, 'down_progressBar')
        self.closing_costs_progressBar = self.findChild(QtWidgets.QProgressBar, 'closing_costs_progressBar')
        #~~~~~contributions~~~~~~~~~~~~~~~~~~~>
        #~~~~~>
        self.capital_required = self.findChild(QtWidgets.QLabel, 'capital_required_display')
        self.crypto_units = self.findChild(QtWidgets.QLabel, 'crypto_units_display')
        self.sponsor = self.findChild(QtWidgets.QLabel, 'sponsor_display')
        # self.chart = self.findChild(QtWidgets.QWidget, 'chart_widget')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.submit = self.findChild(QtWidgets.QPushButton, 'submit_button')
        self.verify = self.findChild(QtWidgets.QPushButton, 'verify_button')
        self.calc_it = self.findChild(QtWidgets.QPushButton, 'calculate_button')
        self.submit.clicked.connect(self.submit_it)
        self.verify.clicked.connect(self.verify_it)
        self.calc_it.clicked.connect(self.calculate_it)
        self.join_opp_button = self.findChild(QtWidgets.QCommandLinkButton, 'join_commandLinkButton')
        self.sponsor_opp_button = self.findChild(QtWidgets.QCommandLinkButton, 'sponsor_commandLinkButton')
        self.join_opp_button.clicked.connect(self.join_opp)
        self.sponsor_opp_button.clicked.connect(self.sponsor_opp)
        # scan_for_data ()
        # poulate_fields()
        #~~generic~data~for~testing~~~~~~~~~~~~~>
        #~~~~>
        self.chart_widget.plot([9.01,35.16,42.74,61.41,86.55])
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.getURLButton.clicked.connect(self.view_deal)
        self.financing_rate_lineEdit.setText('.05')
        self.financing_term_lineEdit.setText('360')
        self.seller_carry_rate_lineEdit.setText('.08')
        self.seller_carry_term_lineEdit.setText('60')
        self.financing_progressBar.setValue(int(80))
        self.seller_carry_progressBar.setValue(int(10))
        self.down_progressBar.setValue(int(10))
        self.closing_costs_progressBar.setValue(int(4))
        # self.total_purchase_display.setText(str(float(self.ask_display.text())+(.035*float(self.ask_display.text()))))
        # self.down_display.setText(str(float(self.ask_display.text())*.3))
        # self.seller_carry_display.setText('0')
        # self.closing_costs_display.setText(str(float(self.ask_display.text())*.035))
        # self.financing_display.setText(str(float(self.total_purhcase.text())-float(self.seller_carry_display.text()))-float(self.down_display.text(())))
    def calculate_it(self):
        gross = (float(self.units.text()) * float(self.monthly_rent.text())) * (1 - float(self.vacancy.text())) + float(self.other_income.text())
        self.gross_income.setText('$'+'{0:,.2f}'.format(gross))
        #~~~~~~~~expenses~~~~~~~~>
        repairs_ = float(self.repairs.text())
        management_ = float(self.management.text())
        taxes_ = float(self.taxes.text())
        insurance_ = float(self.insurance.text())
        salaries_wages_ = float(self.wages.text())
        utility_ = float(self.utilities.text())
        gen_admin_ = float(self.gen_admin.text())
        professional_fees_ = float(self.professional_fees.text())
        advertising_ = float(self.advertising.text())
        capital_reserves_ = float(self.capital_reserves.text())
        other_ = float(self.other.text())
        total_expenses = repairs_+management_+taxes_+insurance_+salaries_wages_+utility_+gen_admin_+professional_fees_+advertising_+capital_reserves_+other_
        self.total_expense.setText('$'+'{0:,.2f}'.format(total_expenses))
        #~~~~~~~~NOI~~~~~~~~>
        noi = gross - total_expenses
        self.noi.setText('$'+'{0:,.2f}'.format(noi))
        #~~~~~~~set~progressBars~~~~~~~~>
        #~~~~>
        self.repairsProgress.setValue(int(repairs_ / gross*100))
        self.managementProgress.setValue(int(management_/gross*100))
        self.taxesProgress.setValue(int(taxes_/gross*100))
        self.insuranceProgress.setValue(int(insurance_/gross*100))
        self.wagesProgress.setValue(int(salaries_wages_/gross*100))
        self.utilitiesProgress.setValue(int(utility_/gross*100))
        self.gen_adminProgress.setValue(int(gen_admin_/gross*100))
        self.professional_feesProgress.setValue(int(professional_fees_/gross*100))
        self.advertisingProgress.setValue(int(advertising_/gross*100))
        self.capital_reservesProgress.setValue(int(capital_reserves_/gross*100))
        self.otherProgress.setValue(int(other_/gross*100))
        self.total_expenses_progressBar.setValue(int(total_expenses/gross*100))
        self.noi_progressBar.setValue(int(noi/gross*100))
        #~~~integrate~irr.py~calculation~~~~~~~>
        self.irr = calc_irr()
        self.irr.cost_rev(asking=float(self.asking.text()),units=float(self.units.text()),average_rent=float(self.monthly_rent.text()),sqft=float(self.sqft.text()))
        self.irr.financing_assumptions(equity_per=float(self.down_progressBar.value()),seller_carry_per=float(self.seller_carry_progressBar.value()),interest_rate=float(self.financing_rate_lineEdit.text()),amort_period=30,seller_carry_rate=float(self.seller_carry_rate_lineEdit.text()),seller_carry_term=float(self.seller_carry_term_lineEdit.text()))
        self.irr.revenues(rent_increase=0.02,expense_increase=0.025,vac_rate=float(self.vacancy_rate_display.text()),extra_income=float(self.other_income_display.text()))
        self.irr.expenses(repairs=float(self.repairs_display.text()),management=float(self.management_display.text()),tax=float(self.taxes_display.text()),insure=float(self.insurance_display.text()),payroll=float(self.wages_display.text()),utils=float(self.utilities_display.text()),gen_admin=float(self.gen_admin_display.text()),pro_fees=float(self.professional_fees_display.text()),ads=float(self.advertising_display.text()),cap_x=float(self.cap_x_display.text()),other_x=float(self.other_expense_display.text()))
        interest_loan = self.irr.calc_interest(start=12, end=0)
        self.irr.deal(percent_rightside=float(self.sponsor_percent_deal_slider.value()))
        self.irr.offer()
        self.irr.key_ratios()
        self.investment_display.setText(str(float(self.asking.text())+float(self.closing_costs.text().replace(',',''))))
        self.irr_display.setText('IRR: '+'{0:,.2f}'.format(self.irr.irr)+'%')
        #~~~set~chart~values~~~~~~~>
        #~~~~>
        self.chart_widget.clear()
        #~~needs~updating~to~real~values~~~>
        self.chart_widget.plot([9.01,35.16,42.74,61.41,86.55])
    def submit_it(self):
        url = 'http://localhost:8000/api/opportunity/'
        response = requests.get(url)
        for item in list(response.json()):
            if item['url'] == self.url_OM.text():
                print(item['id'])
    def verify_it(self):
        print('hi from 227')
    def sponsor_opp(self):
        print('hi from 229')
    def join_opp(self):
        print('hi from 231')
    def view_deal(self):
        try:
            self.webView.load(QUrl(self.urlBox.text()))
            #~~~~~~~~~~start~~analysis~~~~~~~~~~~~
            # self.find_data()
        except Exception as e:
            traceback.print_exc()
    def find_data(self):
        pass
        #~~~TASK~~TWO~~2)~~~~~~~~~~~~~~~~~~~>
        #~~bs4~~download~OM~~~~~~~~>
        # url = self.urlBox.text()
        # response = requests.get(url)
        # with open('pdf_OM.pdf', 'wb') as pdf:
        #     pdf.write(response.content)
        # #~~~scan~~for~text~~~~~~~~~>
        # pdf_name = 'pdf_OM.pdf'
        # pdf_file = open(pdf_name, 'rb')
        # pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        # for i in range(pdf_reader.numPages):
        #     page = pdf_reader.getPage(i)
        #     print(page.extractText())
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
            self.savings = 0.0           
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #setting popup action to add new account to ledger to or from accoutns
            self.new_account = self.findChild(QtWidgets.QAction, 'account_mentu_item')
            self.income = self.findChild(QtWidgets.QTreeView, 'income_view')
            self.expenses = self.findChild(QtWidgets.QTreeView, 'expenses_view')
            self.assets = self.findChild(QtWidgets.QTreeView, 'assets_view')
            self.liabilities = self.findChild(QtWidgets.QTreeView, 'liabilities_view')
            self.opp_small = self.findChild(QtWidgets.QTreeView, 'opportunity_small')
            self.opp_big = self.findChild(QtWidgets.QTreeView, 'opportunity_big')
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #connect button actions
            self.asset = self.findChild(QtWidgets.QPushButton, 'add_asset')
            self.asset.clicked.connect(self.addAsset)
            self.sell_a_asset = self.findChild(QtWidgets.QPushButton, 'liquidate_asset')
            self.sell_a_asset.clicked.connect(self.sellit)
            self.debt = self.findChild(QtWidgets.QPushButton, 'add_liability')
            self.debt.clicked.connect(self.add_debt)
            self.remove_debts = self.findChild(QtWidgets.QPushButton, 'remove_liability')
            self.remove_debts.clicked.connect(self.remove_debt)
            self.paycheck = self.findChild(QtWidgets.QPushButton, 'paycheck_button')
            self.paycheck.clicked.connect(self.add_pay)
            self.analyze_it_ = self.findChild(QtWidgets.QPushButton, 'analyze_button')
            self.analyze_it_.clicked.connect(self.analyze)
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
            self.total_passive.setText('{0:,.2f}'.format(self.get_total_income()[1]))
            self.total_expenses.setText('{0:,.2f}'.format(self.get_total_expenses()))
            self.total_cashflow.setText('{0:,.2f}'.format(self.get_total_income()[0]-self.get_total_expenses()))
            self.percent = self.sum_passive/self.sum_expenses*100
            if self.percent >= 100:
                self.goal_percent.setValue(int(100))
                self.statusBar().showMessage('YOU ARE FREE! FINANCIALLY FREE! GREAT JOB!!')
            else:
                self.goal_percent.setValue(int(self.percent))
            self.worth.setText(' $'+'{0:,.0f}'.format(self.get_total_assets()-self.get_total_liabilities()))
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
            self.commitments = self.findChild(QtWidgets.QProgressBar, 'commitment_progress')
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
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
        except Exception:
            traceback.print_exc()
    def update_display(self):
        #clear all first...~~~~>
        #reload~~~~~~>
        self.total_expenses.setText('{0:,.2f}'.format(self.get_total_expenses()))
        self.total_cashflow.setText('{0:,.2f}'.format(self.get_total_income()[0]-self.get_total_expenses()))
        self.total_passive.setText('{0:,.2f}'.format(self.get_total_income()[1]))
        self.total_income.setText('{0:,.2f}'.format(self.get_total_income()[0]))
        self.percent = self.sum_passive/self.sum_expenses*100
        if self.percent >= 100:
            self.goal_percent.setValue(int(100))
            self.statusBar().showMessage('YOU ARE FREE! FINANCIALLY FREE! GREAT JOB!!')
        else:
            self.goal_percent.setValue(int(self.percent))
        self.worth.setText(' $'+'{0:,.0f}'.format(self.get_total_assets()-self.get_total_liabilities()))
    def add_pay(self):
        pay, ok = QInputDialog.getText(self, 'Paycheck', 'Enter the Gross Amount: ')
        if ok:
            headers = {"content-type": "application/json"}
            url = 'http://localhost:8000/api/income/'
            response = requests.get(url)
            data_dict = {
                "source": 'Salary/Wages',
                "amount": pay,
                "notes": 'paycheck'
            }
            id = 0
            updated = 0.0
            for item in list(response.json()):
                if item ['source'] == 'Salary/Wages':
                    id = item['id']
                    prev_amount = float(item['amount'])
                    updated = float(pay) + prev_amount
                    data_dict['amount'] = str(updated)
                    data = json.dumps(data_dict)
                    response_put = requests.put(url+str(id), data=data, headers=headers)
            if id == 0:
                data = json.dumps(data_dict)
                response_post = requests.post(url, data=data, headers=headers)
            #~~~add~income~to~checking~account~~~~~~~~>
            #~~~~~~>
            url_asset = 'http://localhost:8000/api/asset/'
            response_asset = requests.get(url_asset)
            data_asset = {
                "source": 'Checking',
                "down": '',
                "cost": '',
                "notes": 'Paycheck'
            }
            for item in list(response_asset.json()):
                if item['source'] == 'Checking':
                    id_checking = item['id']
                    prev_amount = float(item['cost'])
                    updated = prev_amount + float(pay)
                    data_asset['down'] = updated
                    data_asset['cost'] = updated
                    data = json.dumps(data_asset)
                    response_put = requests.put(url_asset+str(id_checking), data=data, headers=headers)
            self.reload_income()
            self.reload_assets()
            self.update_display()
    def addAsset(self):
        self.asset = Asset()
        self.asset.move(675,150)
        self.asset.show()
    def add_debt(self):
        debt, ok = QInputDialog.getText(self, 'Debts - (use a comma(,) to seperate)', 'Enter the Account, Remaing Balance Amount: ')
        if ok:
            parts = debt.split(',')
            account = parts[0]
            amount = parts[1]
            url = 'http://localhost:8000/api/liability/'
            headers = {"content-type": "application/json"}
            data_dict = {
                "source": account,
                "amount": amount,
                "notes": 'Debts - Initially'
            }
            data = json.dumps(data_dict)
            response = requests.post(url, data=data, headers=headers)
            self.reload_liabilities()
            self.update_display()
    def remove_debt(self):
        account, ok = QInputDialog.getText(self, 'Debts', 'Enter the Account: ')
        if ok:
            url = 'http://localhost:8000/api/liability/'
            response = requests.get(url)
            id = 0
            for item in list(response.json()):
                if item['source'] == account:
                    id = item['id']
                    res_remove = requests.delete(url+str(id))
                    self.reload_liabilities()
                    self.update_display()
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
                if item['source'] == 'Savings':
                    self.savings += float(item['cost'])
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
           self.total_income.setText('{0:,.2f}'.format(float(self.get_total_income()[0])))
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
        analysis.url_OM.setText(res_details.json()['url'])
        #~~~~set~numbers~of~property~~~~~~>
        #~~~~>
        analysis.ask_display.setText(res_details.json()['ask'])
        analysis.sqft_display.setText(res_details.json()['sqft'])
        analysis.num_units_display.setText(res_details.json()['units'])
        analysis.ave_monthly_rent_display.setText(res_details.json()['ave_rent'])
        analysis.vacancy_rate_display.setText(res_details.json()['vacancy_rate'])
        analysis.other_income_display.setText(res_details.json()['other_income'])
        #~~~~expenses~~~~~~~~~~~~~>
        analysis.repairs_display.setText(res_details.json()['repairs'])
        analysis.management_display.setText(res_details.json()['management'])
        analysis.taxes_display.setText(res_details.json()['taxes'])
        analysis.insurance_display.setText(res_details.json()['insurance'])
        analysis.wages_display.setText(res_details.json()['wages'])
        analysis.utilities_display.setText(res_details.json()['utilities'])
        analysis.gen_admin_display.setText(res_details.json()['gen_admin'])
        analysis.professional_fees_display.setText(res_details.json()['professional_fees'])
        analysis.advertising_display.setText(res_details.json()['advertising'])
        analysis.cap_x_display.setText(res_details.json()['cap_x'])
        analysis.other_expense_display.setText(res_details.json()['other'])
        #~~~~~~calculate~totals~~~~~~~~~~~~~~~~~>
        #~~~>
        scheduled = float(res_details.json()['units'])*int(res_details.json()['ave_rent'])
        gross_income = scheduled-(float(res_details.json()['vacancy_rate'])*scheduled)+float(res_details.json()['other_income'])
        analysis.gross_income_display.setText('{0:,.2f}'.format(gross_income))
        total_expenses = float(res_details.json()['repairs'])+float(res_details.json()['management'])+float(res_details.json()['taxes'])+float(res_details.json()['insurance'])+float(res_details.json()['wages'])+float(res_details.json()['utilities'])+float(res_details.json()['gen_admin'])+float(res_details.json()['professional_fees'])+float(res_details.json()['advertising'])+float(res_details.json()['cap_x'])+float(res_details.json()['other'])
        analysis.total_expense_display.setText('{0:,.2f}'.format(total_expenses))
        noi = gross_income - total_expenses
        analysis.noi_display.setText('{0:,.2f}'.format(noi))
        #~~~~set~progressbars...~~~~~~~~~~~~~~~~~~~~~>
        analysis.repairsProgress.setValue(int(float(res_details.json()['repairs']) / gross_income*100))
        analysis.managementProgress.setValue(int(float(res_details.json()['management'])/gross_income*100))
        analysis.taxesProgress.setValue(int(float(res_details.json()['taxes'])/gross_income*100))
        analysis.insuranceProgress.setValue(int(float(res_details.json()['insurance'])/gross_income*100))
        analysis.wagesProgress.setValue(int(float(res_details.json()['wages'])/gross_income*100))
        analysis.utilitiesProgress.setValue(int(float(res_details.json()['utilities'])/gross_income*100))
        analysis.gen_adminProgress.setValue(int(float(res_details.json()['gen_admin'])/gross_income*100))
        analysis.professional_feesProgress.setValue(int(float(res_details.json()['professional_fees'])/total_expenses*100))
        analysis.advertisingProgress.setValue(int(float(res_details.json()['advertising'])/gross_income*100))
        analysis.capital_reservesProgress.setValue(int(float(res_details.json()['cap_x'])/gross_income*100))
        analysis.otherProgress.setValue(int(float(res_details.json()['other'])/gross_income*100))
        analysis.total_expenses_progressBar.setValue(int(total_expenses/gross_income*100))
        analysis.noi_progressBar.setValue(int(noi/gross_income*100))
        #~~~~financing~~~~~~~~~~~~~~~>
        purchase_price = float(res_details.json()['ask'].replace(',',''))
        analysis.total_purchase_display.setText('{0:,.0f}'.format(purchase_price))
        analysis.financing_display.setText('{0:,.0f}'.format(purchase_price*.7))
        analysis.seller_carry_display.setText('{0:,.0f}'.format(purchase_price*.1))
        #~~~~financing~progressbars~~~~~~~~~~~~>
        #~~~~~Task~1)~~~~~~~~~~~~~~~~~~>
        #~~~>
        down = purchase_price*.035#FHA
        closing_costs = purchase_price*.035
        analysis.down_display.setText('{0:,.0f}'.format(down))
        analysis.closing_costs_display.setText('{0:,.0f}'.format(closing_costs))
        down_pymt_percent = int(float(analysis.down_display.text().replace(',',''))/purchase_price*100)
        analysis.down_progressBar.setValue(down_pymt_percent)
        analysis.down_Slider.setValue(down_pymt_percent)        
        
        # carry_amount = 
        # analysis.seller_carry_progressBar.setValue(int(float(res_details.json()[''])/float(res_details.json()['ask'])))
        # analysis.financing_progressBar.setValue(int())
        #~~~~~~key~numbers~~~~~~~~~~~~~~~>
        #~~~>        
        #~~~~>Task~2)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~>
        #~~~~~~~~~~~~~~~>
        #~~~~~>
        #~>
        analysis.capital_required_display.setText('$'+'{0:,.2f}'.format(down+closing_costs))
        analysis.crypto_units_display.setText('{0:,.0f}'.format(float(res_details.json()['sqft'])))
        analysis.sponsoring_units_display.setText('{0:,.0f}'.format(float(res_details.json()['sqft'])*(1-float(analysis.sponsor_percent_deal_slider.value())/100)))
        analysis.investment_display.setText('{0:,.2f}'.format(int(down)+int(closing_costs)))
        per_unit_cost = float((down+closing_costs) / int(res_details.json()['sqft']))
        analysis.investment_unit_display.setText('{0:,.2f}'.format(per_unit_cost))
        analysis.calculate_it()
        analysis.flow_1_display.setText('{0:,.2f}'.format(analysis.irr.year_1_cashflow_value))
        analysis.flow_2_display.setText('{0:,.2f}'.format(analysis.irr.year_2_cashflow_value))
        analysis.flow_3_display.setText('{0:,.2f}'.format(analysis.irr.year_3_cashflow_value))
        analysis.flow_4_display.setText('{0:,.2f}'.format(analysis.irr.year_4_cashflow_value))
        analysis.flow_5_display.setText('{0:,.2f}'.format(analysis.irr.year_5_cashflow_value))
        # analysis..setText(res_details.json()[])
        #~~~~~savings/down~~~~~~~~~~>
        qoutient = self.savings/float(res_details.json()['down'])
        if qoutient >= 1:
            qoutient = 100
        self.commitments.setValue(int(qoutient))
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
            analysis.view_deal()
        except Exception as e:
            traceback.print_exc()
    def getComboSelection(self):
        text = str(self.comboBox.currentText())
        if text and text is not '':
            return text
    def get_total_passive(self):
        total = self.get_total_income()
        url = 'http://localhost:8000/api/income/'
        response = requests.get(url)
        wages = 0.0
        for item in list(response.json()):
            if item['source'] == 'Salary/Wages':
                wages += float(item['amount'])
        passive = float(total[0]) - wages
        return passive
    def get_total_income(self):
        '''returns a tuple with total income & passive'''
        income = 0.0
        passive = 0.0
        url = 'http://localhost:8000/api/income/'
        response = requests.get(url)
        for item in list(response.json()):
            income += float(item['amount'])
            if item['source'] != 'Salary/Wages':
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
            "Vehicle" : 0,
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
            elif item['to_account'] == 'Vehicle':
                data_dict['Vehicle'] += float(item['amount'])
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
        response_post = ''
        #~~~~~~~~~~~~~~~~~~~~~~~>
        url_put = 'http://localhost:8000/api/expense/'
        headers = {"content-type": "application/json"}
        for item in data_dict:
            put_data['source'] = item
            put_data['amount'] = str(data_dict[item])
            data = json.dumps(put_data)
            id = self.get_exp_id(item)
            #~~~~~~~~~~~~~~~~~~>
            #~~~~~>
            if id == 0:
                response_post = requests.post(url_put, data=data, headers=headers)
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
analysis = Analysis()
ledger = Ledger()
window.move(300,75)
window.show()
app.exec_()
