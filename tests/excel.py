#!/usr/bin/env python3
import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem
from PyQt5.QtCore import Qt, QUrl
import traceback

class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r,c)
        self.init_ui()
    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()
    def c_current(self):
        row = self.currentRow()
        col = self.currentColumn()
        value = self.item(row,col)
        value = value.text()
        print("The current cell is ", row, ", ", col)
        print("In this cell we have: ", value)

    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                my_file = csv.reader(csv_file, delimiter=',', qoutechar='|')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, content in enumerate(row_data):
                        item = QTableWidget(content)
                        self.setItem(row, column, item)
class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = MyTable(10,10)
        self.setCentralWidget(self.form_widget)
        self.form_widget.open_sheet()
        self.show()
