from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(600, 600)
        self.centralWidget = QtGui.QTextEdit()
        self.setCentralWidget(self.centralWidget)

        # Upper table widget
        dock = QtGui.QDockWidget("Upper", self.centralWidget)
        dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.tableWidget = QtGui.QTableWidget(dock)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(7)
        for i in range(7):
            item = QtGui.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            self.tableWidget.verticalHeaderItem(i).setText("Item " + str(i + 1))
        for i in range(6):
            item = QtGui.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        dock.setWidget(self.tableWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        # Lower table widget
        dock = QtGui.QDockWidget("Lower", self.centralWidget)
        self.tableWidget_2 = QtGui.QTableWidget(dock)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setRowCount(7)
        for i in range(7):
            item = QtGui.QTableWidgetItem()
            self.tableWidget_2.setVerticalHeaderItem(i, item)
        for i in range(6):
            item = QtGui.QTableWidgetItem()
            self.tableWidget_2.setHorizontalHeaderItem(i, item)
        dock.setWidget(self.tableWidget_2);
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.listWidget = QtGui.QListWidget(self.centralWidget)
        self.listWidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.listWidget.setObjectName("listWidget")
        for i in range(10):
            item = QtGui.QListWidgetItem()
            self.listWidget.addItem(item)
            item = self.listWidget.item(i)
            item.setText("Item " + str(i + 1))
        self.listWidget.setMinimumSize(QtCore.QSize(340, 600))
        self.setWindowTitle("Dock Widgets")

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())