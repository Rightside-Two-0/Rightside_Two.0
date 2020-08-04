#!/usr/bin/env python3
import rightside_2, sys
# def test___init__():
#     '''testing main window'''
#     app = rightside_2.QtWidgets.QApplication(sys.argv)
#     rightside = rightside_2.MainWindow()
#     rightside.move(300,750)
#     rightside.show()
#     app.exec_()
#     assert rightside != None
def test_addAsset():
    '''testing asset widget'''
    app = rightside_2.QtWidgets.QApplication(sys.argv)
    rightside = rightside_2.MainWindow()
    rightside.move(300,750)
    widget = rightside_2.Asset()
    rightside.show()
    app.exec_()
    assert widget != None
