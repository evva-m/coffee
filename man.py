from PyQt6 import uic
import sys
import io
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem


template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>970</width>
    <height>475</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QTableWidget" name="tableWidget">
   <property name="geometry">
    <rect>
     <x>5</x>
     <y>11</y>
     <width>951</width>
     <height>411</height>
    </rect>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class InteractiveReceipt(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.tableWidget.setColumnCount(7)
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.loadTable()

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InteractiveReceipt()
    ex.show()
    sys.exit(app.exec())