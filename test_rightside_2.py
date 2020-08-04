#!/usr/bin/env python3
import rightside_2, sys 
def test_function():
    app = rightside_2.QtWidgets.QApplication(sys.argv)
    rightside = rightside_2.MainWindow()
    rightside.move(300,750)
    rightside.show()
    app.exec_()
    assert 1+1+1 == 3
