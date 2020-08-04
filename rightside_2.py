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
        # self.asset.addItems(content)
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
    def addAsset(self):
        self.asset = Asset()
        self.asset.move(675,150)
        self.asset.show()
    def sellit(self):
        self.selling = SellAsset()
        self.selling.move(675,150)
        self.selling.show()
