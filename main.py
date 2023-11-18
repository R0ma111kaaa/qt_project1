from datetime import datetime
import sys

from PyQt5.QtWidgets import QApplication

import requests
import geocoder

from PyQt5 import QtCore, QtWidgets, QtGui

import os.path
import sqlite3

from PyQt5.QtCore import QDate, QTimer, Qt
from PyQt5.QtGui import QFontDatabase, QFont, QTextCharFormat, QColor
from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QWidget, QTextEdit, QColorDialog, QLabel, QComboBox, \
    QTableWidget, QTableWidgetItem, QAbstractItemView, QTabWidget, QLayout, QMessageBox


def getWeather():
    api = open("resources/other/API.txt").read()

    try:
        cords = geocoder.ip('me')
    except RuntimeError:
        return None, None
    except Exception:
        return None, None
    lat, lon = cords.latlng
    city = cords.city
    try:
        curr_weather = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api)
        )
    except RuntimeError:
        return None, None
    except Exception:
        return None, None
    if curr_weather.status_code == 200:
        return curr_weather.json(), city
    else:
        return None, city


class Ui_AddCategory(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(481, 67)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 461, 53))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pickColorButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pickColorButton.setObjectName("pickColorButton")
        self.horizontalLayout.addWidget(self.pickColorButton)
        self.saveCategoryButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveCategoryButton.setObjectName("saveCategoryButton")
        self.horizontalLayout.addWidget(self.saveCategoryButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить категорию"))
        self.pickColorButton.setText(_translate("Form", "Выбрать цвет"))
        self.saveCategoryButton.setText(_translate("Form", "Сохрнанить"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(892, 455)
        MainWindow.setMinimumSize(QtCore.QSize(594, 0))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(30, 10, 271, 111))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(70)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.time.setFont(font)
        self.time.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.time.setStyleSheet("")
        self.time.setObjectName("time")
        self.calendar = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendar.setGeometry(QtCore.QRect(30, 120, 391, 291))
        self.calendar.setObjectName("calendar")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(420, 120, 451, 291))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 441, 261))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 5, 10, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.selectedDate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.selectedDate.setFont(font)
        self.selectedDate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.selectedDate.setObjectName("selectedDate")
        self.horizontalLayout_3.addWidget(self.selectedDate)
        self.deleteButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/images/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_3.addWidget(self.deleteButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.noteEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.noteEdit.setObjectName("noteEdit")
        self.verticalLayout_2.addWidget(self.noteEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addCategoryButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addCategoryButton.sizePolicy().hasHeightForWidth())
        self.addCategoryButton.setSizePolicy(sizePolicy)
        self.addCategoryButton.setObjectName("addCategoryButton")
        self.horizontalLayout_2.addWidget(self.addCategoryButton)
        self.categoryChooser = QtWidgets.QComboBox(self.layoutWidget)
        self.categoryChooser.setObjectName("categoryChooser")
        self.horizontalLayout_2.addWidget(self.categoryChooser)
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 441, 261))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.categoryChooser2 = QtWidgets.QComboBox(self.layoutWidget1)
        self.categoryChooser2.setObjectName("categoryChooser2")
        self.horizontalLayout.addWidget(self.categoryChooser2)
        self.categoryEditButton = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryEditButton.sizePolicy().hasHeightForWidth())
        self.categoryEditButton.setSizePolicy(sizePolicy)
        self.categoryEditButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/images/pencil.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.categoryEditButton.setIcon(icon1)
        self.categoryEditButton.setObjectName("categoryEditButton")
        self.horizontalLayout.addWidget(self.categoryEditButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.eventTable = QtWidgets.QTableWidget(self.layoutWidget1)
        self.eventTable.setObjectName("eventTable")
        self.eventTable.setColumnCount(0)
        self.eventTable.setRowCount(0)
        self.verticalLayout.addWidget(self.eventTable)
        self.tabWidget.addTab(self.tab_2, "")
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(310, 30, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.date.setFont(font)
        self.date.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.date.setObjectName("date")
        self.weekday = QtWidgets.QLabel(self.centralwidget)
        self.weekday.setGeometry(QtCore.QRect(310, 60, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.weekday.setFont(font)
        self.weekday.setObjectName("weekday")
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(560, 20, 291, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.weather.setFont(font)
        self.weather.setStyleSheet("* { background-color: blue; color: white }")
        self.weather.setScaledContents(False)
        self.weather.setAlignment(QtCore.Qt.AlignCenter)
        self.weather.setObjectName("weather")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Умный календарь"))
        self.time.setText(_translate("MainWindow", "TI:ME:00"))
        self.tabWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.selectedDate.setText(_translate("MainWindow", "selected date"))
        self.addCategoryButton.setText(_translate("MainWindow", "+"))
        self.saveButton.setText(_translate("MainWindow", "Сохранить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Добавить событие"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Найти событие"))
        self.date.setText(_translate("MainWindow", "date month year, weekday"))
        self.weekday.setText(_translate("MainWindow", "weekday"))
        self.weather.setText(_translate("MainWindow", "погода"))


class SmartCalendar(QMainWindow, Ui_MainWindow):
    months_rus = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    weekdays_rus = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    weather_rus = {"Clouds": "Облачно", "Clear": "Ясно", "Snow": "Идёт снег", "Rain": "Идёт дождь",
                   "Drizzle": "Дождь моросит", "Thunderstorm": "Гроза", "Mist": "Туман", "Smoke": "Смок",
                   "Haze": "Мгла", "Dust": "Пыль", "Fog": "Туман", "Sand": "Песчаная буря", "Tornado": "Торнадо",
                   "Squall": "Вихрь", "Ash": "Пепел"
                   }

    images_path = "resources/images/"

    db_name = "resources/databases/main_db.sqlite"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.calendar: QCalendarWidget
        self.noteEdit: QTextEdit
        self.categoryChooser2: QComboBox
        self.eventTable: QTableWidget

        self.setFixedSize(self.size())

        #  set actions to events
        self.calendar.selectionChanged.connect(self.dateChangeEvent)
        self.saveButton.clicked.connect(self.saveNote)
        self.addCategoryButton.clicked.connect(self.createNewCategoryWindow)
        self.categoryEditButton.clicked.connect(self.changeCategoryWindow)
        self.deleteButton.clicked.connect(self.deleteNote)
        self.categoryChooser2.currentIndexChanged.connect(self.showFoundedEvents)
        self.eventTable.cellClicked.connect(self.changeDate)

        #  setup custom font and add stylesheet
        custom_font_id = QFontDatabase().addApplicationFont("resources/fonts/comfortaa.ttf")
        custom_font_families = QFontDatabase.applicationFontFamilies(custom_font_id)
        custom_font = QFont(custom_font_families[0], 18)
        self.date.setFont(custom_font)
        self.selectedDate.setFont(custom_font)
        self.weekday.setFont(custom_font)
        self.setStyleSheet(open("resources/design/styles.css").read())

        #  create the database
        if not os.path.exists(self.db_name):
            open(self.db_name, "w")
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, "
                "note TEXT, "
                "category_id INTEGER NOT NULL, FOREIGN KEY (category_id) REFERENCES categories(id))"
            )
            cur.execute("CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        " title TEXT NOT NULL, hex TEXT NOT NULL)")
            cur.execute("INSERT INTO categories(title, hex) VALUES(?, ?)", ("Стандарт (белый)", "#ffffff"))
            con.commit()
            cur.close()
            con.close()

        #  events table
        self.eventTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #  set current date
        self.date.setText(datetime.now().strftime("%d") + " " + self.months_rus[int(datetime.now().month - 1)]
                          + " " + datetime.now().strftime("%Y") + " г.")
        self.weekday.setText(self.weekdays_rus[datetime.now().weekday()])

        #  run other methods
        self.colorCalendar()
        self.dateChangeEvent()
        self.setComboBoxesInfo()
        self.setWeatherWidgetInfo()
        self.datetime_update()

    def dateFormat(self):
        return self.calendar.selectedDate().toString("ddMMyyyy")

    def changeDate(self, row):
        """Change the current date on main QCalendarWidget automatically"""
        self.calendar: QCalendarWidget
        self.eventTable: QTableWidget
        self.tabWidget: QTabWidget

        date = self.eventTable.item(row, 0).text()
        new_date = QDate(*tuple(map(int, (date[6:], date[3:5], date[:2]))))
        self.calendar.setSelectedDate(new_date)
        self.tabWidget.setCurrentIndex(0)

    def dateChangeEvent(self):
        """Change the note field when date changed"""
        self.calendar: QCalendarWidget
        self.categoryChooser: QComboBox

        sel_date = self.calendar.selectedDate()
        self.selectedDate.setText(sel_date.toString("dd.MM.yyyy"))
        if note := sqlite3.connect(self.db_name).cursor() \
                .execute("SELECT note, categories.title FROM notes JOIN categories"
                         " ON category_id == categories.id WHERE date = ?",
                         (self.dateFormat(),)).fetchone():
            self.noteEdit.setText(note[0])
            self.categoryChooser.setCurrentText(note[1])
        else:
            self.noteEdit.setText("")
            self.categoryChooser.setCurrentIndex(0)

    def saveNote(self):
        self.calendar: QCalendarWidget

        if not self.noteEdit.toPlainText():
            msg = QMessageBox()
            msg.setIcon(1)
            msg.setText("Заполните текст заметки")
            msg.setWindowTitle("Заметка не сохранена")
            msg.exec_()
            return
        if self.categoryChooser.currentIndex() == 0:
            msg = QMessageBox()
            msg.setIcon(1)
            msg.setText("Выберите другую категорию")
            msg.setWindowTitle("Заметка не сохранена")
            msg.exec_()
            return
        self.statusBar().showMessage("")
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        if cur.execute("SELECT id FROM notes WHERE date = ?",
                       (self.dateFormat(),)).fetchone():
            con.cursor().execute("UPDATE notes SET note = ?, category_id = ? WHERE date = ?",
                                 (self.noteEdit.toPlainText(), self.categoryChooser.currentData(),
                                  self.dateFormat(),))
            con.commit()
        else:
            try:
                cur.execute("INSERT INTO notes(date, note, category_id) VALUES(?, ?, ?)",
                            (self.dateFormat(), self.noteEdit.toPlainText(),
                             self.categoryChooser.currentData()))
            except sqlite3.IntegrityError:
                self.statusBar().showMessage("Выберите категорию")
            else:
                con.commit()
        self.colorDate(self.calendar.selectedDate(), cur.execute(
            "SELECT hex FROM categories WHERE id = ?", (self.categoryChooser.currentData(),)).fetchone()[0])
        cur.close()
        con.close()
        self.showFoundedEvents()

    def deleteNote(self):
        self.calendar: QCalendarWidget

        con = sqlite3.connect(self.db_name)
        if con.cursor().execute("SELECT id FROM notes WHERE date = ?", (self.dateFormat(), )).fetchone():
            answer = QMessageBox.question(self, "", f"Удалить заметку на {self.selectedDate.text()}?",
                                          QMessageBox.Yes, QMessageBox.No)
        else:
            return
        if answer == QMessageBox.Yes:
            con.cursor().execute("DELETE FROM notes WHERE date = ?",
                                 (self.dateFormat(), ))
            con.commit()

            colored_date = QTextCharFormat()
            colored_date.setBackground(QColor("white"))
            if self.calendar.selectedDate().dayOfWeek() in (6, 7):
                colored_date.setForeground(QColor("red"))
            else:
                colored_date.setForeground(QColor("black"))
            self.calendar.setDateTextFormat(self.calendar.selectedDate(), colored_date)

            self.dateChangeEvent()
        con.close()

    def createNewCategoryWindow(self):
        self.new_category_window = NewEventWidget(self)
        self.new_category_window.show()

    def changeCategoryWindow(self):
        if self.categoryChooser2.currentData() != 1:
            self.new_category_window = NewEventWidget(self, True)
            self.new_category_window.show()

    def setComboBoxesInfo(self):
        self.categoryChooser: QComboBox

        self.categoryChooser.clear()
        self.categoryChooser2.clear()

        for category in sqlite3.connect(self.db_name).cursor() \
                .execute("SELECT title, id FROM categories").fetchall():
            self.categoryChooser.addItem(category[0], category[1])
            self.categoryChooser2.addItem(category[0], category[1])

    def colorCalendar(self):
        """Main method that updates calendar info"""
        self.calendar: QCalendarWidget

        for date, color in sqlite3.connect(self.db_name).cursor().execute(
                "SELECT notes.date, categories.hex FROM notes JOIN categories ON notes.category_id = categories.id") \
                .fetchall():
            self.colorDate(date, color)

    def colorDate(self, date, color):
        color = QColor(color)
        color_text = QColor("black") if (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000 > 128 \
            else QColor("white")

        colored_date = QTextCharFormat()
        colored_date.setBackground(color)
        colored_date.setForeground(color_text)
        if type(date) == str:
            qdate = QDate(*tuple(map(int, (date[4:], date[2:4], date[:2]))))
        else:
            qdate = date
        self.calendar.setDateTextFormat(qdate, colored_date)

    def showFoundedEvents(self):
        self.eventTable: QTableWidget
        self.categoryChooser2: QComboBox

        events = sqlite3.connect(self.db_name).cursor().execute("SELECT n.date, n.note, c.title FROM notes AS n LEFT "
                                                                "JOIN categories as c ON n.category_id = c.id WHERE "
                                                                "n.category_id = ?",
                                                                (self.categoryChooser2.currentData(),)).fetchall()
        if events:
            self.eventTable.setColumnCount(3)
            self.eventTable.setHorizontalHeaderLabels(("Дата", "Текст", "Категория"))
            for column in range(3):
                self.eventTable.setColumnWidth(column, 141)
        else:
            self.eventTable.setColumnCount(0)
            return
        self.eventTable.setRowCount(len(events))

        for i, row in enumerate(events):
            date = row[0]
            self.eventTable.setItem(i, 0, QTableWidgetItem(f"{date[:2]}.{date[2:4]}.{date[4:]}"))
            for j, elem in enumerate(row[1:]):
                j += 1
                self.eventTable.setItem(i, j, QTableWidgetItem(elem))

    def setWeatherWidgetInfo(self):
        self.weather: QLabel
        self.weather_layout: QLayout

        # main = "Rain"
        weather, city = getWeather()
        if not weather:
            return
        main = weather["weather"][0]["main"]
        degrees = weather["main"]["temp"] - 273

        self.weather.setText(f"{degrees:.1f}°C, {self.weather_rus[main]}")

    def datetime_update(self):
        self.time.setText(datetime.now().strftime("%H:%M:%S"))
        QTimer.singleShot(500, lambda: self.datetime_update())


class NewEventWidget(QWidget, Ui_AddCategory):
    def __init__(self, parentWidgetPage, from_change_button=False):
        super(NewEventWidget, self).__init__()
        self.setupUi(self)
        self.initUi()
        self.parentWidgetPage = parentWidgetPage

        self.color = None
        self.id = None

        if from_change_button:
            self.setWindowTitle("Изменить категорию")

            data = sqlite3.connect(self.parentWidgetPage.db_name).cursor().execute(
                "SELECT * FROM categories WHERE id = ?", (self.parentWidgetPage.categoryChooser2.currentData(),)
            ).fetchone()
            self.id = data[0]
            self.title = data[1]
            self.color = QColor(data[2])
            self.pickColorButton.setStyleSheet(f"background-color: {self.color.name()}")
            self.pickColorButton.setText("Изменить цвет")
            self.lineEdit.setText(self.title)

    def initUi(self):
        self.pickColorButton.clicked.connect(self.getColor)
        self.saveCategoryButton.clicked.connect(self.save)

        self.adjustSize()
        self.setFixedSize(self.size())

    def getColor(self):
        self.colorLabel: QLabel

        color = QColorDialog.getColor()
        if color.isValid() and color.name() != "#ffffff":
            self.color = color
            self.pickColorButton.setStyleSheet(f"background-color: {self.color.name()}")
            self.pickColorButton.setText("Изменить цвет")

    def save(self):
        con = sqlite3.connect(self.parentWidgetPage.db_name)
        cur = con.cursor()
        if self.id:
            cur.execute("UPDATE categories SET hex = ?, title = ? WHERE id = ?",
                        (self.color.name(), self.lineEdit.text(), self.id))
            con.commit()
            self.parentWidgetPage.colorCalendar()
        elif self.color and not cur.execute("SELECT id FROM categories WHERE hex = ?", (self.color.name(),)
                                            ).fetchone() and self.lineEdit.text():
            cur.execute("INSERT INTO categories(title, hex) VALUES(?, ?)",
                        (self.lineEdit.text(), self.color.name()))
            con.commit()
        self.parentWidgetPage.setComboBoxesInfo()
        cur.close()
        con.close()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    sc = SmartCalendar()
    sc.show()

    sys.excepthook = except_hook

    sys.exit(app.exec())
