#!/usr/bin/env python3
import rightside_2, sys, json, requests
# def test___init__():
#     '''testing main window'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     rightside.show()
#     app.exec_()
#     assert rightside != None
# def test_addAsset():
#     '''testing addAsset function'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     widget = rightside_2.Asset()
#     rightside.show()
#     app.exec_()
#     assert widget != None
# def test_sellit():
#     '''testing sell-it widget'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     widget = rightside_2.SellAsset()
#     rightside.show()
#     app.exec_()
#     assert widget != None
# def test_remove():
#     '''testing remove function'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     widget = rightside_2.SellAsset()
#     rightside.show()
#     app.exec_()
#     widget.sell()
#     assert widget.price_sold.text() == ''
# def test_add_liability():
#     '''testing add liability function'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     rightside.show()
#     app.exec_()
#     url = 'http://two-0.org:8080/api/liabilities/'
#     response = requests.get(url)
#     for item in response.json():
#         if item['notes'] == 'Debts - Initially':
#             assert item['notes'] == 'Debts - Initially'
# def test_remove_liability():
#     '''testing remove liability function'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     rightside.show()
#     app.exec_()
#     url = 'http://two-0.org:8080/api/liabilities/'
#     response = requests.get(url)
#     for item in response.json():
#         if item['notes'] == 'Debts - Initially':
#             assert item['notes'] != 'Debts - Initially'
# def test_add_pay():
#     '''testing add pay function'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     rightside.show()
#     app.exec_()
#     url = 'http://two-0.org:8080/api/incomes/'
#     response = requests.get(url)
#     for item in response.json():
#         if item['notes'] != 'Paycheck':
#             assert item['notes'] == 'Paycheck' or 'paycheck'
def test_analyze():
        '''testing add pay function'''
        app = rightside_2.QtWidgets.QApplication(sys.argv)
        rightside = rightside_2.MainWindow()
        rightside.move(300,750)
        rightside.show()
        app.exec_()
        widget = rightside_2.Analysis()
        assert widget != None
