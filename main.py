import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic


class CoffeeRead(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        res = self.connection.cursor().execute('SELECT * FROM coffee').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('ID'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('название сорта'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('степень обжарки'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('молотый/в зернах'))
        self.tableWidget.setItem(0, 4, QTableWidgetItem('описание вкуса'))
        self.tableWidget.setItem(0, 5, QTableWidgetItem('цена'))
        self.tableWidget.setItem(0, 6, QTableWidgetItem('объем упаковки'))

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i + 1, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeRead()
    ex.show()
    sys.exit(app.exec())
