# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from time import time

import RecommendationSystem

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(400, 400)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.userLabel = QtWidgets.QLabel(self.centralwidget)
        self.userLabel.setGeometry(QtCore.QRect(90, 30, 60, 21))
        self.userLabel.setObjectName("userLabel")

        self.recomendationLabel = QtWidgets.QLabel(self.centralwidget)
        self.recomendationLabel.setGeometry(QtCore.QRect(60, 60, 91, 21))
        self.recomendationLabel.setObjectName("recomendationLabel")

        self.userEditText = QtWidgets.QLineEdit(self.centralwidget)
        self.userEditText.setGeometry(QtCore.QRect(180, 30, 181, 20))
        self.userEditText.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[1-9]\d{3}$')))
        self.userEditText.setObjectName("userEditText")
        self.userEditText.setText("1")

        self.recomendationEditText = QtWidgets.QSpinBox(self.centralwidget)
        self.recomendationEditText.setGeometry(QtCore.QRect(180, 60, 181, 22))
        self.recomendationEditText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.recomendationEditText.setMinimum(1)
        self.recomendationEditText.setMaximum(20)
        self.recomendationEditText.setProperty("value", 10)
        self.recomendationEditText.setObjectName("recomendationEditText")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 130, 380, 240))
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnWidth(0, 269)
        self.tableWidget.setColumnWidth(1, 75)

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(10, 110, 131, 16))
        self.title.setObjectName("title")

        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(315, 100, 75, 23))
        self.button.setObjectName("button")
        self.button.clicked.connect(lambda:self.getRecommendations())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Basado en contenido"))
        self.userLabel.setText(_translate("MainWindow", "Usuario ID"))
        self.recomendationLabel.setText(_translate("MainWindow", "Recomendaciones"))
        self.title.setText(_translate("MainWindow", "Peliculas recomendadas"))
        self.button.setText(_translate("MainWindow", "Buscar"))

    def getRecommendations(self):
        try:
            user = int(self.userEditText.text())
            count = self.recomendationEditText.value()
            movies = RecommendationSystem.recommend(user, count)

            self.clearTable()

            rowPosition = 0
            for m in movies:
                self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(m[0]))
                self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("{0:.4f}".format(m[1])))
                rowPosition += 1
        except ValueError:
            QtWidgets.QMessageBox.about(MainWindow, "Error", "Usuario no valido")

    def clearTable(self):
        for pos in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(pos, 0, QtWidgets.QTableWidgetItem(""))
            self.tableWidget.setItem(pos, 1, QtWidgets.QTableWidgetItem(""))

if __name__ == "__main__":
    # Start counting.
    start_time = time()
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # Calculate the elapsed time.
    elapsed_time = time() - start_time

    print("Elapsed time: %0.10f seconds." % elapsed_time)
