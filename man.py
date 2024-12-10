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
  <widget class="QPushButton" name="btn">
   <property name="geometry">
    <rect>
     <x>730</x>
     <y>430</y>
     <width>211</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>изменить данные или добавить запись</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

sec_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>787</width>
    <height>412</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QTableWidget" name="tableWidget_edit">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>761</width>
     <height>192</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="btn_edit">
   <property name="geometry">
    <rect>
     <x>640</x>
     <y>200</y>
     <width>131</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>сохранить изменения</string>
   </property>
  </widget>
  <widget class="QTableWidget" name="tableWidget_add">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>280</y>
     <width>751</width>
     <height>71</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="btn_add">
   <property name="geometry">
    <rect>
     <x>640</x>
     <y>350</y>
     <width>131</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>добавить запись</string>
   </property>
  </widget>
  <widget class="QPushButton" name="btn_exit">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>370</y>
     <width>75</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>вернуться</string>
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
        self.btn.clicked.connect(self.next_form)

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

    def next_form(self):
        self.hide()
        sec_form.show()


class Form(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(sec_template)
        uic.loadUi(f, self)
        self.tableWidget_edit.setColumnCount(7)
        self.tableWidget_add.setColumnCount(6)
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упаковки']
        add_title = ['название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget_add.setHorizontalHeaderLabels(add_title)
        self.tableWidget_add.setRowCount(1)
        self.tableWidget_edit.setHorizontalHeaderLabels(title)
        self.loadTable()
        self.btn_edit.clicked.connect(self.save_changes)
        self.btn_add.clicked.connect(self.add)
        self.btn_exit.clicked.connect(self.prev_form)

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget_edit.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget_edit.setRowCount(
                self.tableWidget_edit.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_edit.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget_edit.resizeColumnsToContents()
        con.close()

    def save_changes(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        for row in range(self.tableWidget_edit.rowCount()):
            line_data = []
            for col in range(7):
                line_data.append(self.tableWidget_edit.item(row, col).text())
            cur.execute(f"""UPDATE coffee SET id = ?, sort_title = ?, degree_of_roasting = ?, ground_or_grains 
= ?, flavor_description = ?, price = ?, volume_of_packaging = ? WHERE id = {line_data[0]}""", tuple(line_data))
        con.commit()
        con.close()
        self.loadTable()

    def add(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        line_data = []
        for col in range(6):
            line_data.append(self.tableWidget_add.item(0, col).text())
        cur.execute(f"""INSERT INTO coffee (sort_title, degree_of_roasting, ground_or_grains, flavor_description, 
        price, volume_of_packaging) VALUES(?, ?, ?, ?, ?, ?)""", tuple(line_data))
        con.commit()
        con.close()
        self.loadTable()
        self.tableWidget_add.clearContents()

    def prev_form(self):
        self.hide()
        ex.show()
        ex.loadTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InteractiveReceipt()
    sec_form = Form()
    ex.show()
    sys.exit(app.exec())