import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class ListView(QtWidgets.QTreeView):
    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        self.setModel(QtGui.QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.setHeaderHidden(True)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)

    def addItem(self, key, value):
        first = QtGui.QStandardItem(key)
        second = QtGui.QStandardItem(value)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.model().appendRow([first, second])

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = ListView(self)
        for text in 'Aquamarine Red Green Purple Blue Yellow '.split():
            self.view.addItem(text, "Hi")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 300, 200)
    window.show()
    sys.exit(app.exec_())
