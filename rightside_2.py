import sys, os
import json, csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QShortcut, QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from tests.calc_irr import mortgage
from tests.calc_irr import calc_irr
from tests import mortgage
import traceback
import requests
import PyPDF2
url_income = 'http://two-0.org:8080/api/incomes/'
url_expeneses = 'http://two-0.org:8080/api/expenses/'
url_assets = 'http://two-0.org:8080/api/assets/'
url_liabilities = 'http://two-0.org:8080/api/liabilities/'
url_opportunities = 'http://two-0.org:8080/api/opportunities/'
url_ledger = 'http://two-0.org:8080/api/ledger/'
class ComputeThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)
    # run method gets called when we start the thread
    def run(self):
        print('testing thread # 21...')
        # git clone done, now inform the main thread with the output
        self.signal.emit('')
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
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
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
        value = float(self.sponsor_percent_deal_slider.value())
        self.sponsor_percent_deal_slider.setToolTip(str(value)+'%')
        #~~generic~data~for~testing~~~~~~~~~~~~~>
        #~~~~>
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
        self.getURLButton.clicked.connect(self.view_deal)
        self.financing_rate_lineEdit.setText('.05')
        self.financing_term_lineEdit.setText('360')
        self.seller_carry_rate_lineEdit.setText('.08')
        self.seller_carry_term_lineEdit.setText('60')
        #~~~progressbars...~~~~~~~~~~~~~~~>
        self.financing_progressBar.setValue(int(80))
        self.seller_carry_progressBar.setValue(int(10))
        self.down_progressBar.setValue(int(10))
        self.closing_costs_progressBar.setValue(int(4))
        #~~~down~slider~~~~~>
        self.down_Slider.valueChanged.connect(self.update_fields)
        self.sponsor_percent_deal_slider.valueChanged.connect(self.investors_percent)
        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.calculate_it)

        #~~~~~~>
        self.getURLButton.clicked.connect(self.view_deal)
        self.computit_thread = ComputeThread()  # This is the thread object
        # Connect the signal from the thread to the finished method
        self.computit_thread.signal.connect(self.finished)
    def calculate_it(self):
        units = float(self.units.text()) if self.units.text() != '' else 0
        ave_rent = float(self.monthly_rent.text()) if self.monthly_rent.text() != '' else 0
        vacancy = float(self.vacancy.text()) if self.vacancy.text() != '' else 0
        other_in = float(self.other_income.text()) if self.other_income.text() != '' else 0
        gross = (units * ave_rent) * (1 - vacancy) + other_in
        self.gross_income.setText('$'+'{0:,.2f}'.format(gross*12))
        #~~~~~~~~expenses~~~~~~~~>
        repairs_ = float(self.repairs.text()) if self.repairs.text() != '' else 0
        management_ = float(self.management.text()) if self.management.text() != '' else 0
        taxes_ = float(self.taxes.text()) if self.taxes.text() != '' else 0
        insurance_ = float(self.insurance.text()) if self.insurance.text() != '' else 0
        salaries_wages_ = float(self.wages.text()) if self.wages.text()!= '' else 0
        utility_ = float(self.utilities.text()) if self.utilities.text() !='' else 0
        gen_admin_ = float(self.gen_admin.text()) if self.gen_admin.text() != '' else 0
        professional_fees_ = float(self.professional_fees.text()) if self.professional_fees.text()!= '' else 0
        advertising_ = float(self.advertising.text()) if self.advertising.text() != '' else 0
        capital_reserves_ = float(self.capital_reserves.text()) if self.capital_reserves.text() != '' else 0
        other_ = float(self.other.text()) if self.other.text() != '' else 0
        total_expenses = repairs_+management_+taxes_+insurance_+salaries_wages_+utility_+gen_admin_+professional_fees_+advertising_+capital_reserves_+other_
        self.total_expense.setText('$'+'{0:,.2f}'.format(total_expenses*12))
        #~~~~~~~~NOI~~~~~~~~>
        noi_ = gross - total_expenses
        self.noi.setText('$'+'{0:,.2f}'.format(noi_*12))
        self.noi_monthly_display.setText('{0:,.2f}'.format(noi_))
        #~~~~~~~set~progressBars~~~~~~~~>
        #~~~~>
        if gross == 0:
            gross = 1
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
        self.noi_progressBar.setValue(int(noi_/gross*100))
        seller_carry = float(self.seller_carry_display.text().replace(',','')) if self.seller_carry_display.text() != '' else 0
        self.seller_carry_progressBar.setValue(int(seller_carry))
        #~~~~~>set~fields~values~~~~~~~>
        new_ask = float(self.ask_display.text()) if self.ask_display.text() != '' else 0
        self.total_purchase_display.setText('{0:,.0f}'.format(new_ask))
        self.financing_display.setText('{0:,.0f}'.format(new_ask*self.financing_progressBar.value()/100))
        self.seller_carry_display.setText('{0:,.0f}'.format(new_ask*self.seller_carry_progressBar.value()/100))
        self.down_progressBar.setValue(int(self.down_Slider.value()))
        down = new_ask*self.down_progressBar.value()/100
        closing = new_ask*self.closing_costs_progressBar.value()/100
        self.down_display.setText('{0:,.0f}'.format(down))
        self.closing_costs_display.setText('{0:,.0f}'.format(closing))
        noi_income = float(self.noi.text().replace('$','').replace(',',''))
        self.cap_rate_display.setText('{0:,.2f}'.format(noi_income/float(self.ask_display.text())*100)+'%')
        #~~~~>
        total = float(self.total_purchase_display.text().replace(',',''))
        seller_carry = float(self.seller_carry_display.text().replace(',',''))
        financing = total-(seller_carry+float(self.down_display.text().replace(',','')))
        self.financing_display.setText('{0:,.0f}'.format(financing))
        if total == 0:
            total = 1
        self.financing_progressBar.setValue(int(financing/total*100))
        self.seller_carry_progressBar.setValue(int(seller_carry/total*100))
        self.get_payment()
        sqft = float(self.sqft_display.text()) if self.sqft_display.text() != '' else 0
        self.crypto_units_display.setText('{0:,.0f}'.format(sqft))
        self.capital_required_display.setText('{0:,.0f}'.format(down+closing))
        self.investor_units_display.setText('{0:,.0f}'.format(float(self.crypto_units_display.text().replace(',',''))*self.sponsor_percent_deal_slider.value()/100))
        #~~~integrate~irr.py~calculation~~~~~~~>
        if total != 1:
            self.get_irr()
            #~~~~cash~flows~too~~~~~~~~~~>
            self.flow_1_display.setText('{0:,.2f}'.format(self.irr.investment_unit))
            self.flow_2_display.setText('{0:,.2f}'.format(self.irr.five_years_unit))
            self.flow_3_display.setText('{0:,.2f}'.format(self.irr.ten_years_unit))
            self.flow_4_display.setText('{0:,.2f}'.format(self.irr.twenty_years_unit))
            self.flow_5_display.setText('{0:,.2f}'.format(self.irr.thirty_years_unit))
            #~~~set~chart~values~~~~~~~>
            #~~~~>
            self.chart_widget.clear()
            #~~needs~updating~to~real~values~~~>
            units = int(self.investor_units_display.text().replace(',',''))
            #~~~~>
            self.capital_required_display.setText('{0:,.0f}'.format(down+closing))
            self.investment_unit_display.setText('{0:,.2f}'.format((down+closing)/units))
            self.chart_widget.plot([float(self.investment_unit_display.text().replace(',','')),self.irr.year_5_cashflow_value/units,self.irr.year_4_cashflow_value/units,self.irr.year_3_cashflow_value/units,self.irr.year_2_cashflow_value/units,self.irr.year_1_cashflow_value/units])
    def submit_it(self):
        '''adds a new property to network'''
        url = 'http://two-0.org:8080/api/opportunities/'
        ask = self.ask_display.text() if self.ask_display.text() != '' else '0'
        sqft = self.sqft_display.text() if self.sqft_display.text() != '' else '0'
        num_units = self.num_units_display.text() if self.num_units_display.text() != '' else '0'
        ave_monthly_rent = self.ave_monthly_rent_display.text() if self.ave_monthly_rent_display.text() != '' else '0'
        vacancy = self.vacancy_rate_display.text() if self.vacancy_rate_display.text() != '' else '0'
        other_income = self.other_income_display.text() if self.other_income_display.text() != '' else '0'
        gross = float(num_units)*float(ave_monthly_rent)
        income = gross-(1-float(vacancy))+float(other_income)
        #~~~~~~~~expenses~~~~~~~>
        repairs_ = self.repairs_display.text() if self.repairs_display.text() != '' else '0'
        management_ = self.management_display.text() if self.management_display.text() != '' else '0'
        taxes_ = self.taxes_display.text() if self.taxes_display.text() != '' else '0'
        insurance_ = self.insurance_display.text() if self.insurance_display.text() != '' else '0'
        wages_  = self.wages_display.text() if self.wages_display.text() != '' else '0'
        utilities_ = self.utilities_display.text() if self.utilities_display.text() != '' else '0'
        gen_admin_ = self.gen_admin_display.text() if self.gen_admin_display.text() != '' else '0'
        professional_fees_ = self.professional_fees_display.text() if self.professional_fees_display.text() != '' else '0'
        advertising_ = self.advertising_display.text() if self.advertising_display.text() != '' else '0'
        cap_x_ = self.cap_x_display.text() if self.cap_x_display.text() != '' else '0'
        other_ = self.other_expense_display.text() if self.other_expense_display.text() != '' else '0'
        expenses_ = float(repairs_)+float(management_)+float(taxes_)+float(insurance_)+float(wages_)+float(utilities_)+float(gen_admin_)+float(professional_fees_)+float(advertising_)+float(cap_x_)+float(other_)
        #~~~~~~~~~~~>
        heading, ok = QInputDialog.getText(self, 'Heading', 'Enter a heading for property:')
        description, ok = QInputDialog.getText(self, 'Description', 'Enter description or summary:')
        url_ = self.url_OM.text()
        cost = float(ask)
        down = ''
        mortgage_ = ''
        down = '{0:,.2f}'.format(float(self.down_display.text().replace(',','')))
        mortgage_ = '{0:,.2f}'.format(float(self.financing_display.text().replace(',','')))
        #~~~~need~to~get~a~debt~payment~~~~~~~~~~~~~~~~>
        #~~~~~>
        pymt = mortgage.Mortgage(interest=0.05,  amount=float(mortgage_.replace(',','')), months=360)
        debt_service = float(pymt.monthly_payment())
        cashflow = income-expenses_-debt_service
        cash_flow = '{0:.2f}'.format(cashflow)
        if down == '0.00':
            down = '1'
        coc = '{0:,.2f}'.format(cashflow*12/float(down.replace(',','')))
        irr = '{0:,.2f}'.format(15.0)
        costs_ = str(cost)
        if url_ != '':
            headers = {"content-type": "application/json"}
            data_dict = {
                'heading': heading,
                'description': description,
                'url': url_,
                'cost': costs_,
                'down': down,
                'mortgage': mortgage_,
                'cash_flow': cash_flow,
                'coc': coc,
                'irr': irr,
                'ask': ask,
                'sqft': sqft,
                'units': num_units,
                'ave_rent': ave_monthly_rent,
                'vacancy_rate': vacancy,
                'other_income': other_income,
                'repairs': repairs_,
                'management': management_,
                'taxes': taxes_,
                'insurance': insurance_,
                'wages': wages_,
                'utilities': utilities_,
                'gen_admin': gen_admin_,
                'professional_fees': professional_fees_,
                'advertising': advertising_,
                'cap_x': cap_x_,
                'other': other_
            }
            data = json.dumps(data_dict)
            response = requests.post(url, data=data, headers=headers)
            analysis.hide()
            #~~~~reload~opportunity~table~~~~>
            #~~~>
            window.reload_small_opps()
            window.reload_big_opps()
    def verify_it(self):
        print('hi from 227')
    def sponsor_opp(self):
        print('hi from 229')
    def join_opp(self):
        print('hi from 231')
    def view_deal(self):
        '''the idea here is to load an image of the logo (lions head)
            maybe flashing until the webview loads with page data'''
        try:
            self.computit_thread.start()
            # self.webView.load(QUrl(self.urlBox.text()))
            # QWebEngineViewによるWebページ表示
            browser = QWebEngineView()
            browser.load(QUrl(self.urlBox.text()))
            browser.show()
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
    def get_payment(self):
        rate = float(self.financing_rate_lineEdit.text())
        principle = float(self.financing_display.text().replace(',',''))
        term = int(self.financing_term_lineEdit.text())
        pymt = mortgage.Mortgage(interest=rate, amount=principle, months=term)
        self.financing_payment_display.setText('{0:,.2f}'.format(pymt.monthly_payment()))
        #~~~~~~set~seller~financing~~~~~~~~~~~>
        carry_amount = float(self.seller_carry_display.text().replace(',',''))
        carry_rate = float(self.seller_carry_rate_lineEdit.text())
        interest_only = carry_amount*carry_rate
        self.seller_carry_payment_display.setText('{0:,.2f}'.format(interest_only/12))
    def get_irr(self):
        #~~~IRR~~~~~~>
        repairs_ = float(self.repairs_display.text())*12 if self.repairs_display.text() != '' else 0.0
        management_ = float(self.management_display.text())*12 if self.management_display.text() != '' else 0.0
        taxes_ = float(self.taxes_display.text())*12 if self.taxes_display.text() != '' else 0.0
        insurance_ = float(self.insurance_display.text())*12 if self.insurance_display.text() != '' else 0.0
        wages_ = float(self.wages_display.text())*12 if self.wages_display.text() != '' else 0.0
        utilities_  = float(self.utilities_display.text())*12 if self.utilities_display.text() != '' else 0.0
        gen_admin_ = float(self.gen_admin_display.text())*12 if self.gen_admin_display.text() != '' else 0.0
        professional_fees_ = float(self.professional_fees_display.text())*12 if self.professional_fees_display.text() != '' else 0.0
        advertising_ = float(self.advertising_display.text())*12 if self.advertising_display.text() != '' else 0.0
        cap_x_ = float(self.cap_x_display.text())*12 if self.cap_x_display.text() != '' else 0.0
        other_ = float(self.other_expense_display.text())*12 if self.other_expense_display.text() != '' else 0.0
        improvements_ = float(self.improvements_display.text()) if self.improvements_display.text() != '' else 0.0
        #~~~~error~somewhere~~~~~~~~>
        #~~~>
        try:
            self.irr = calc_irr()
            print('Testing in progress...~~~~~~~~~~~~~~~~>')
            print('asking',self.asking.text())
            print('improvements',improvements_)
            print('units',self.units.text())
            print('ave_monthly rent',self.monthly_rent.text())
            print('Sqft',self.sqft.text())
            print('down %',self.down_progressBar.value()/100)
            print('carry %',self.seller_carry_progressBar.value()/100)
            print('financing rate',float(self.financing_rate_lineEdit.text())*100)
            print('seller carry rate',float(self.seller_carry_rate_lineEdit.text())*100)
            print('seller carry term',self.seller_carry_term_lineEdit.text())
            print('vacancy rate',float(self.vacancy_rate_display.text())*100)
            print('other income',self.other_income_display.text())
            print('',repairs_)
            print('',management_)
            print('',taxes_)
            print('',insurance_)
            print('',wages_)
            print('',gen_admin_)
            print('',professional_fees_)
            print('',advertising_)
            print('',cap_x_)
            print('',other_)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
            #~~this~one~works~~~>
            self.irr.cost_rev(asking=149900,improvements=0,units=3,average_rent=750,sqft=10000)
            self.irr.financing_assumptions(equity_per=0.03,seller_carry_per=0,interest_rate=5.0,amort_period=30,seller_carry_rate=8.0,seller_carry_term=60)
            self.irr.revenues(rent_increase=0.02,expense_increase=0.025,vac_rate=10.0,extra_income=0)
            self.irr.expenses(repairs=60,management=0,tax=0,insure=0,payroll=0,utils=0,gen_admin=0,pro_fees=0,ads=0,cap_x=1850,other_x=8000)
            interest = self.irr.calc_interest(start=12, end=0)
            self.irr.deal(percent_rightside=0.45)
            self.irr.offer()
            print(self.irr.irr)
            #~~~but~this~one~does~not~~~~~~~>
            # self.irr.cost_rev(asking=float(self.asking.text()),improvements=improvements_,units=float(self.units.text()),average_rent=float(self.monthly_rent.text()),sqft=float(self.sqft.text()))
            # self.irr.financing_assumptions(equity_per=float(self.down_progressBar.value()/100),seller_carry_per=float(self.seller_carry_progressBar.value()/100),interest_rate=float(self.financing_rate_lineEdit.text())*100,amort_period=30,seller_carry_rate=float(self.seller_carry_rate_lineEdit.text())*100,seller_carry_term=float(self.seller_carry_term_lineEdit.text()))
            # self.irr.revenues(rent_increase=0.02,expense_increase=0.025,vac_rate=float(self.vacancy_rate_display.text())*100,extra_income=float(self.other_income_display.text()))
            # self.irr.expenses(repairs=repairs_,management=management_,tax=taxes_,insure=insurance_,payroll=wages_,utils=utilities_,gen_admin=gen_admin_,pro_fees=professional_fees_,ads=advertising_,cap_x=cap_x_,other_x=other_)
            # interest_loan = self.irr.calc_interest(start=12, end=0)
            # self.irr.deal(percent_rightside=float(self.sponsor_percent_deal_slider.value()/100))
            # self.irr.offer()
            # self.irr.key_ratios()
            # self.irr_display.setText('IRR: '+'{0:,.2f}'.format(self.irr.irr)+'%')

        except:
            traceback.print_exc()

        #~~~cash~on~cash~~~~~>
        needed = float(self.capital_required_display.text().replace(',','').replace('$',''))
        before_tax = float(self.noi.text().replace(',','').replace('$',''))-(float(self.financing_payment_display.text().replace(',',''))*12)
        coc = before_tax/needed*100
        self.coc_display.setText('{0:,.2f}'.format(coc))
    def update_fields(self):
        '''get value from down_slider and set down_progressBar & down_display with value'''
        slider_value = self.down_Slider.value()
        self.total_purchase_display.setText('{0:,.0f}'.format(float(self.ask_display.text())))
        total_price = float(self.total_purchase_display.text().replace(',',''))
        down_amount = total_price * float(slider_value)/100
        self.down_progressBar.setValue(int(down_amount/total_price*100))
        self.down_display.setText('{0:,.0f}'.format(down_amount))
        #~~~~~the~remaining~financing~fields~should~be~updated~~~~~>
        #~~~~~>
        seller_financing_amount = float(self.seller_carry_display.text().replace(',',''))
        financing_amount = total_price-(down_amount+seller_financing_amount)#-float(self.closing_costs_display.text().replace(',',''))
        self.financing_display.setText('{0:,.0f}'.format(financing_amount))
        #~~~progressbar~~~~~~~>
        ratio = financing_amount/total_price*100
        self.financing_progressBar.setValue(int(ratio))
        carry_ratio = seller_financing_amount/total_price*100
        self.seller_carry_progressBar.setValue(int(carry_ratio))
        #~~~update~required~capital~~~~~~~>
        #~~>
        required = float(self.down.text().replace(',',''))+float(self.closing_costs.text().replace(',',''))
        self.capital_required_display.setText('{0:,.2f}'.format(required))
        #~~~per~unit~~~>
        if self.investor_units_display.text() == '':
            self.investor_units_display.setText('1')
        investor_units = float(self.investor_units_display.text().replace(',',''))
        per_unit = required/investor_units
        self.investment_unit_display.setText('{0:,.2f}'.format(per_unit))
        #~~~update~payment~with~new~values~~~~>
        #~~>
        self.get_payment()
        self.calculate_it()
        #~~~~update~chart~as~well~~~~~~>
        self.chart_widget.clear()
        self.chart_widget.plot([float(self.investment_unit_display.text().replace(',','')),self.irr.year_5_cashflow_value/float(self.sqft.text()),self.irr.year_4_cashflow_value/float(self.sqft.text()),self.irr.year_3_cashflow_value/float(self.sqft.text()),self.irr.year_2_cashflow_value/float(self.sqft.text()),self.irr.year_1_cashflow_value/float(self.sqft.text())])
        #~~~~cash~flows~too~~~~~~~~~~>
        self.flow_1_display.setText('{0:,.2f}'.format(self.irr.year_1_cashflow_value))
        self.flow_2_display.setText('{0:,.2f}'.format(self.irr.year_2_cashflow_value))
        self.flow_3_display.setText('{0:,.2f}'.format(self.irr.year_3_cashflow_value))
        self.flow_4_display.setText('{0:,.2f}'.format(self.irr.year_4_cashflow_value))
        self.flow_5_display.setText('{0:,.2f}'.format(self.irr.year_5_cashflow_value))
    def investors_percent(self):
        value = float(self.sponsor_percent_deal_slider.value())
        equity_units = int(self.crypto_units_display.text().replace(',',''))
        investors_portion = float(equity_units*value/100)
        self.investor_units_display.setText('{0:,.0f}'.format(investors_portion))
        #~~~update~cost/unit~~~~~~~~>
        #~~~>
        if investors_portion == 0:
            investors_portion = 1
        per_unit = float(self.capital_required.text().replace(',','').replace('$',''))/investors_portion
        self.investment_unit_display.setText('{0:,.2f}'.format(per_unit))
        self.sponsor_percent_deal_slider.setToolTip(str(value)+'%')
        self.get_irr()
        #~~~cash~flows~too~~~~~~~~>
        #~~>
        self.flow_1_display.setText('{0:,.2f}'.format(self.irr.year_1_cashflow_value))
        self.flow_2_display.setText('{0:,.2f}'.format(self.irr.year_2_cashflow_value))
        self.flow_3_display.setText('{0:,.2f}'.format(self.irr.year_3_cashflow_value))
        self.flow_4_display.setText('{0:,.2f}'.format(self.irr.year_4_cashflow_value))
        self.flow_5_display.setText('{0:,.2f}'.format(self.irr.year_5_cashflow_value))
        #~~~~update~chart~~~~~~~~~~>
        #~~~>
        self.chart_widget.clear()
        self.chart_widget.plot([float(self.investment_unit_display.text().replace(',','')),self.irr.year_5_cashflow_value/float(self.sqft.text()),self.irr.year_4_cashflow_value/float(self.sqft.text()),self.irr.year_3_cashflow_value/float(self.sqft.text()),self.irr.year_2_cashflow_value/float(self.sqft.text()),self.irr.year_1_cashflow_value/float(self.sqft.text())])
    def finished(self):
        pass
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
                "cost" : f'{cost}',
                "down" : f'{down}',
                "notes" : f'{note}'
            }
            data = json.dumps(dict)
            url = 'http://two-0.org:8080/api/assets/'
            response = requests.post(url, data=data, headers=headers)
            #~~~~~~update~income~as~well~~~~~>
            url2 = 'http://two-0.org:8080/api/incomes/'
            dict2 = {
                "source": f'{type}',
                "amount": f'{cash_flow}',
                "notes": f'{note}',
            }
            data2 = json.dumps(dict2)
            response2 = requests.post(url2, data=data2, headers=headers)
            #~~~~~~~~~~~~~liability~~~~~~~~~~~>
            #~~~~~~~~>
            url3 = 'http://two-0.org:8080/api/liabilities/'
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
            url4 = 'http://two-0.org:8080/api/expenses/'
            response_get = requests.get(url4).json()
            prev_amount = 0.0
            for item in list(response_get):
                if item['source'] == 'RE Debt Service':
                     id = item['id']
                     prev_amount = item['amount']
            updated = float(pymt) + float(prev_amount)
            dict4 = {
                "source" : 'RE Debt Service',
                "amount" : f'{updated}',
                "notes": f'{note}'
            }
            if id != 0:
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
        self.sell_button.clicked.connect(self.sell)
        self.cancel_button.clicked.connect(self.cancel)
        response = requests.get('http://two-0.org:8080/api/assets/')
        content = []
        for item in list(response.json()):
            content.append(item['notes'])
        self.asset_combobox.addItems(content)
    def sell(self):
        asset_note = self.asset_combobox.currentText()
        price = self.price_sold.text()
        self.remove('incomes', asset_note)
        # self.remove('expenses', '')
        self.remove('assets', asset_note)
        self.remove('liabilities', asset_note)
        #~~~~~>
        # window.reload_income()
        # window.reload_assets()
        # # window.reload_expenses()
        # window.reload_liabilities()
        # window.update_display()
        #~~~~~~~~~~clean~up~fields~~~~~>
        self.price_sold.setText('')
        self.close()
    def cancel(self):
        self.hide()
    def remove(self, account, notes):
        url = 'http://two-0.org:8080/api/'+account+'/'
        response = requests.get(url)
        id = ''
        for item in list(response.json()):
            if item['notes'] == notes:
                id = str(item['id'])
        response_del = requests.delete(url+id)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('guis/financial.ui', self)
        self.savings = 0.0
        self.add_asset.clicked.connect(self.addAsset)
        self.liquidate_asset.clicked.connect(self.sellit)
        self.add_liability.clicked.connect(self.add_debt)
        self.remove_liability.clicked.connect(self.remove_debt)
        self.paycheck_button.clicked.connect(self.add_pay)
        self.analyze_button.clicked.connect(self.analyze)
    def update_display(self):
        self.total_expenses.setText('{0:,.2f}'.format(self.get_total_expenses()))
        self.total_cashflow.setText('{0:,.2f}'.format(self.get_total_income()[0]-self.get_total_expenses()))
        self.total_passive.setText('{0:,.2f}'.format(self.get_total_income()[1]))
        self.total_income.setText('{0:,.2f}'.format(self.get_total_income()[0]))
        self.percent = self.get_total_income()[1]/self.get_total_expenses()*100
        if self.percent >= 100:
            self.goal_percent.setValue(int(100))
            self.statusBar().showMessage('YOU ARE FREE! FINANCIALLY FREE! GREAT JOB!!')
        else:
            self.goal_percent.setValue(int(self.percent))
        self.worth.setText(' $'+'{0:,.0f}'.format(self.get_total_assets()-self.get_total_liabilities()))
    def addAsset(self):
        self.asset = Asset()
        self.asset.move(675,150)
        self.asset.show()
    def add_pay(self):
        pay, ok = QInputDialog.getText(self, 'Paycheck', 'Enter the Gross Amount: ')
        if ok:
            headers = {"content-type": "application/json"}
            response = requests.get(url_income)
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
                    response_put = requests.put(url_income+str(id), data=data, headers=headers)
            if id == 0:
                data = json.dumps(data_dict)
                response_post = requests.post(url_income, data=data, headers=headers)
            #~~~add~income~to~checking~account~~~~~~~~>
            #~~~~~~>
            response_asset = requests.get(url_assets)
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
                    response_put = requests.put(url_assets+str(id_checking), data=data, headers=headers)
            self.reload_income()
            self.reload_assets()
            self.update_display()
    def sellit(self):
        self.selling = SellAsset()
        self.selling.move(675,150)
        self.selling.show()
    def add_debt(self):
        debt, ok = QInputDialog.getText(self, 'Debts - (use a comma(,) to seperate)', 'Enter the Account, Remaing Balance Amount: ')
        if ok:
            parts = debt.split(',')
            account = parts[0]
            amount = parts[1]
            headers = {"content-type": "application/json"}
            data_dict = {
                "source": account,
                "amount": amount,
                "notes": 'Debts - Initially'
            }
            data = json.dumps(data_dict)
            response = requests.post(url_liabilities, data=data, headers=headers)
            print(response.json())
            self.reload_liabilities()
            self.update_display()
    def remove_debt(self):
        account, ok = QInputDialog.getText(self, 'Debts', 'Enter the Account: ')
        if ok:
            response = requests.get(url_liabilities)
            id = 0
            for item in list(response.json()):
                if item['source'] == account:
                    id = item['id']
                    res_remove = requests.delete(url+str(id))
                    self.reload_liabilities()
                    self.update_display()
    def load_debts(self):
        try:
            response = requests.get(url_liabilities)
            for item in list(response.json()):
                self.addItem_Liabilities(item['source']+' - '+item['notes'],  '{0:,.0f}'.format(float(item['amount'])))
                self.sum_debts += float(item['amount'])
        except Exception:
            traceback.print_exc()
    def reload_liabilities(self):
        self.liabilities.model().removeRows(0, self.liabilities.model().rowCount())
        self.load_debts()
    def analyze(self):
        try:
            analysis.show()
            analysis.move(313,150)
            sender = self.sender()
            if sender.objectName() == 'add_property_button':
                self.clear_all()
                analysis.view_deal()
            else:
                analysis.view_deal()
        except Exception as e:
            traceback.print_exc()
