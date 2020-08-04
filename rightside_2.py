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
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('guis/financial.ui', self)
