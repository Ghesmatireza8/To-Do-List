from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QLineEdit, QListWidget
from PyQt5 import uic
import sys
import sqlite3
import res


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("To Do List.ui", self)

        # Define Our Widgets
        self.task_le = self.findChild(QLineEdit, "task_le")

        self.listWidget = self.findChild(QListWidget, "listWidget")

        self.add_task_bt = self.findChild(QPushButton, "add_task_bt")
        self.remove_task_bt = self.findChild(QPushButton, "remove_task_bt")
        self.done_bt = self.findChild(QPushButton, "done_bt")
        self.notdone_bt = self.findChild(QPushButton, "notdone_bt")
        self.save_db_bt = self.findChild(QPushButton, "save_db_bt")
        self.clear_list_bt = self.findChild(QPushButton, "clear_list_bt")



        # Do something
        self.add_task_bt.clicked.connect(self.add_task)
        self.remove_task_bt.clicked.connect(self.remove_task)
        self.done_bt.clicked.connect(self.done)
        self.notdone_bt.clicked.connect(self.notdone)
        self.save_db_bt.clicked.connect(self.save_db)
        self.clear_list_bt.clicked.connect(self.clear_list)

        self.set_data()

        # Show The App
        self.show()


    def set_data(self):
        conn = sqlite3.connect("list.db")
        cursor = conn.cursor()
        cursor.execute("select * from list")
        data = cursor.fetchall()
        conn.commit()
        conn.close()


        for row in data:
            self.listWidget.addItem(str(row[0]))



    def add_task(self):
        if self.task_le.text() == '':
            pass
        else:
            item = self.task_le.text()
            item = f"{item} _ Not Done"
            self.listWidget.addItem(item)
            self.task_le.setText("")


    def remove_task(self):
        clicked = self.listWidget.currentRow()
        self.listWidget.takeItem(clicked)


    def done(self):
        current = self.listWidget.currentItem()
        cr = current.text().split("_")
        current.setText(f"{cr[0]}_ Done")



    def notdone(self):
        current = self.listWidget.currentItem()
        cr = current.text().split("_")
        current.setText(f"{cr[0]}_ Not Done")


    def save_db(self):
        # Create a database or connect to one
        conn = sqlite3.connect('list.db')
        # Create a cursor
        c = conn.cursor()

        # Delete everything in the database table
        c.execute('DELETE FROM list')

        # Create Blank List To Hold Todo Items
        items = []
        # Loop through the listWidget and pull out each item
        for index in range(self.listWidget.count()):
            items.append(self.listWidget.item(index))

        for item in items:
            # print(item.text())
            # Add stuff to the table
            c.execute("INSERT INTO list VALUES (:item)",
                      {
                          'item': item.text(),
                      })

        # Commit the changes
        conn.commit()

        # Close our connection
        conn.close()


    def clear_list(self):
        self.listWidget.clear()


# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
