import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QDialog

from addEditCoffeeForm import Ui_E
from main_UI import Ui_Form


class Dialog(QDialog, Ui_E):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CoffeeRead(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.is_incorrectID = False
        self.setupUi(self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.editButton.clicked.connect(self.open_dialog)
        self.dlg = Dialog()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('ID'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('название сорта'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('степень обжарки'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('молотый/в зернах'))
        self.tableWidget.setItem(0, 4, QTableWidgetItem('описание вкуса'))
        self.tableWidget.setItem(0, 5, QTableWidgetItem('цена'))
        self.tableWidget.setItem(0, 6, QTableWidgetItem('объем упаковки'))
        self.table_update()

    def open_dialog(self):
        self.dlg.show()
        self.dlg.tableWidget.setRowCount(2)
        self.dlg.radioButtonedit.setChecked(True)
        self.dlg.coffeeID.setValue(1)
        self.dlg.radioButtonedit.toggled.connect(self.check_state)
        self.dlg.coffeeID.valueChanged.connect(self.check_state)
        self.dlg.buttonBox.accepted.connect(self.save_changes)
        self.dlg.tableWidget.setColumnCount(7)
        self.dlg.tableWidget.setItem(0, 0, QTableWidgetItem('ID'))
        self.dlg.tableWidget.setItem(0, 1, QTableWidgetItem('название сорта'))
        self.dlg.tableWidget.setItem(0, 2, QTableWidgetItem('степень обжарки'))
        self.dlg.tableWidget.setItem(0, 3, QTableWidgetItem('молотый/в зернах'))
        self.dlg.tableWidget.setItem(0, 4, QTableWidgetItem('описание вкуса'))
        self.dlg.tableWidget.setItem(0, 5, QTableWidgetItem('цена'))
        self.dlg.tableWidget.setItem(0, 6, QTableWidgetItem('объем упаковки'))
        self.check_state()

    def check_state(self):
        if self.dlg.radioButtonadd.isChecked():
            self.dlg.tableWidget.setItem(1, 0, QTableWidgetItem('Auto Increment'))
            for i in range(1, 7):
                self.dlg.tableWidget.setItem(1, i, None)
            self.is_incorrectID = False
            self.dlg.coffeeID.setDisabled(True)
        else:
            try:
                if self.dlg.coffeeID.value() == 0:
                    raise AttributeError
                self.dlg.coffeeID.setDisabled(False)
                for i in range(7):
                    self.dlg.tableWidget.setItem(1, i, QTableWidgetItem(self.tableWidget.item(
                        self.dlg.coffeeID.value(), i).text()))
                    self.is_incorrectID = False
            except AttributeError:
                self.dlg.tableWidget.setItem(1, 0, QTableWidgetItem('Incorrect ID Value'))
                self.is_incorrectID = True
                for i in range(1, 7):
                    self.dlg.tableWidget.setItem(1, i, None)
        self.table_update()

    def table_update(self):
        self.tableWidget.setRowCount(1)
        res = self.connection.cursor().execute('SELECT * FROM coffee').fetchall()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i + 1, j, QTableWidgetItem(str(elem)))

    def save_changes(self):
        try:
            if not self.is_incorrectID:
                if self.dlg.radioButtonadd.isChecked():
                    que = '''INSERT INTO coffee ('название сорта', 'степень обжарки', 'молотый/в зернах', 
                    'описание вкуса', 'цена', 'объем упаковки') VALUES(?, ?, ?, ?, ?, ?)'''
                    changed = []
                    for i in range(1, 7):
                        changed.append(self.dlg.tableWidget.item(1, i).text())
                else:
                    que = '''UPDATE coffee SET ID = ?, 'название сорта' = ?, 'степень обжарки' = ?, 
                    'молотый/в зернах' = ?, 'описание вкуса' = ?, 'цена' = ?, 'объем упаковки' = ? WHERE ID = ?'''
                    changed = []
                    for i in range(7):
                        changed.append(self.dlg.tableWidget.item(1, i).text())
                    changed.append(self.dlg.coffeeID.value())

                self.connection.cursor().execute(que, tuple(changed))
                self.connection.commit()
                self.table_update()
        except AttributeError:
            pass

    def closeEvent(self, a0):
        self.dlg.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeRead()
    ex.show()
    sys.exit(app.exec())
