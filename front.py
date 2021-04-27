from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from mysql.connector import connect, Error
import psycopg2
from MySqlConnector import MySqlConnector
from PostgresConnector import PostgresConnector
from Sqlite import SqliteConnector


#Дані для занесення в бд
faculties = [(1, 'Faculty of Informatics and Computer Science'),
            (2, 'Faculty of Applied Mathematics'),
            (3, 'Faculty of Biomedical Engineering'),
            (4, 'Faculty of Chemical Engineering'),
            (5, 'Faculty of Electronics'),
            (6, 'Faculty of heat power engineering'),
            (7, 'Faculty of Instrumentation Engineering'),
            (8, 'Faculty of Linguistics'),
            (9, 'Faculty of Management and Marketing'),
            (10, 'Faculty of Sociology and Law')]

#Дані для занесення в бд
departments = [(1,'КТК',1 ),
            (2,'PZKS',2 ),
            (3,'DBC',3 ),
            (4,'TPZA',4 ),
            (5,'МЕ',5 ),
            (6,'AESIITF',6 ),
            (7,'VP',7 ),
            (8,'KTPPAM',8 ),
            (9,'KEP',9 ),
            (10,'KGAP',10 ),
            (11,'OT',1 ),
            (12,'PMA',2 ),
            (13,'DBE',3 ),
            (14,'ERP',4 ),
            (15,'EDS',5 ),
            (16,'ATEP',6 ),
            (17,'OOEP',7 ),
            (18,'KTPPNM',8 ),
            (19,'KM',9 ),
            (20,'KS',10 )]

#Дані для занесення в бд
teachers = [(1,1,'Serhij','Andrijovych','Zozulya' ),
            (2,2,'Danylo','Herasymenko','Illich' ),
            (3,3,'Ivan','Stetsyuk','Kostyantynovych' ),
            (4,4,'Vadym','Kolesnyk','Heorhijovych' ),
            (5,5,'Mykyta','Honcharuk','Kuzmych' ),
            (6,6,'Bohdan','Palamarchuk','Tarasovych' ),
            (7,7,'Yurij','Yanchuk','Romanovych' ),
            (8,8,'Fedir','Levchuk','Vyacheslavovych' ),
            (9,9,'Bronislav','Solovej','Kazymyrovych' ),
            (10,10,'Henadij','Romanovych','Morhun' ), 
            (11,11,'Serhij','Demchuk','Yaroslavovych' ), 
            (12,12,'Vadym','Skrypnyk','Heorhijovych' ), 
            (13,13,'Viktor','Bondarenko','Olehovych' ),
            (14,14,'Oleh','Sushko','Danylovych' ), 
            (15,15,'Volodymyr','Honcharuk','Ruslanovych' ), 
            (16,16,'Pylyp','Yashchenko','Yurijovych' ),
            (17,17,'Zynovij','Khomenko','Borysovych' ), 
            (18,18,'Ihor','Palamarchuk','Oleksandrovych' ),
            (19,19,'Kuzma','Yakymenko','Vasylovych' ),
            (20,20,'Bohdan','Bilyk','Feodosijovych' )]

#Дані для занесення в бд
subjects = [(1, 'Accounting & Finance'),
            (2, 'Art & Design'),
            (3, 'Architecture'),
            (4, 'Manufacturing Engineering'),
            (5, 'Law'),
            (6, 'Economics & Econometrics'),
            (7, 'Medicine'),
            (8, 'Business & Management Studies'),
            (9, 'Engineering & Technology'),
            (10,'Computer Science' )] 

#Дані для занесення в бд
subjects_to_teachers = [(1,1,1 ),
            (2,2,2 ),
            (3,3,3 ),
            (4,4,4 ),
            (5,5,5 ),
            (6,6,6 ),
            (7,7,7 ),
            (8,8,8 ),
            (9,9,9 ),
            (10,10,10 ),
            (11,11,1 ),
            (12,12,2 ),
            (13,13,3 ),
            (14,14,4 ),
            (15,15,5 ),
            (16,16,6 ),
            (17,17,7 ),
            (18,18,8 ),
            (19,19,9 ),
            (20,20,10 )]

#Під'єднання до БД
sqlite = SqliteConnector()
Postgres = PostgresConnector()
MySql = MySqlConnector()

# Функція для створення БД1
def createDB():
    MySql.dropAllTables()
    MySql.createDatabase()
    MySql.executemany("INSERT INTO faculties VALUES (%s,%s)", faculties)
    MySql.executemany("INSERT INTO department VALUES (%s,%s,%s)", departments)
    MySql.executemany("INSERT INTO teachers VALUES (%s,%s,%s,%s,%s)", teachers)
    MySql.executemany("INSERT INTO subject VALUES (%s,%s)", subjects)
    MySql.executemany("INSERT INTO subjects_to_teachers VALUES (%s,%s,%s)", subjects_to_teachers)

# Функція для переносу БД1 в БД2
def mySqlToPostgres():
    Postgres.dropAllTables()
    Postgres.createDatabase()
    cur = MySql.getCursor()
    data = MySql._getAllTablesData(cur)
    Postgres.importData(data)

# Функція для переносу БД2 в БД3
def myPostgresToSQLite():
    sqlite.dropAllTables()
    sqlite.createDatabase()
    cur = Postgres.getCursor()
    data = Postgres._getAllTablesData(cur)
    sqlite.importData(data)

# Функція для зміни таблиці з вчителями в бд2(можна замінити Postgress на іншу бд)
def ChangePostgrTable(teachID,depID,fname,sname,fathname):
    try:
        print(Postgres.execute(f"UPDATE teachers set firstname = \'{fname}\',lastname = \'{sname}\',fathername = \'{fathname}\',department_id = {depID} where id = {teachID}"))
        print("Данные успешно обновлены")
    except Exception as ex:
            print(ex)

# Функція для виклику довільного sql запиту
def executepostr(text):
    try:
        return(Postgres.execute(text))
        print("SQL запрос успешно обработан")
    except Exception as ex:
        print("Ошибка при исполнении SQL запроса: \n")
        print(ex)

window = Tk()

# Встановлення підпису вікна
window.title("CRUD")
# Встановлення розміру вікна
window.geometry('800x400')

#Створюємо рамку для розмітки
ProgramFrame = Frame(window)
ProgramFrame.pack(side=LEFT, fill=BOTH, expand=True)

# Створюємо кнопки для створення та експорту БД
generateNumbers = Button(ProgramFrame, font=("Arial", 14), command = createDB, text="Створити БД1", width=20)
generateNumbers.grid(row=1, column=0)

generateNumbers = Button(ProgramFrame, font=("Arial", 14),command = mySqlToPostgres, text="Експорт БД1 у БД2", width=20)
generateNumbers.grid(row=2, column=0)

generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД2 у БД3", width=20, command = myPostgresToSQLite)
generateNumbers.grid(row=4, column=0)

#Перевірка правильності введення ID вчителя
def IdCheck(*args):
    try:
        pass
    #Якщо введено некоректні дані
    except:
        ID.delete(0, 'end')
        ID.insert(0, 0)

# Вивід рядка ID вчителя
Label(ProgramFrame, font=("Arial", 14), text="ID Вчителя:").grid(row=6, column=0, sticky="E")
teacherID = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=1, to=100)
teacherID.grid(row=6, column=1, sticky="W")
# перевірка корректності даних
teacherID.bind("<FocusOut>", IdCheck)

# Вивід рядка ID Кафедри
Label(ProgramFrame, font=("Arial", 14), text="ID Кафедри:").grid(row=7, column=0, sticky="E")
DepartmentID = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=1, to=100)
DepartmentID.grid(row=7, column=1, sticky="W")
# перевірка корректності даних
DepartmentID.bind("<FocusOut>", IdCheck)

# Вивід рядка для вводу Ім'я вчителя
Label(ProgramFrame, font=("Arial", 14), text="Ім'я:").grid(row=8, column=0, sticky="E")
firstName = Entry(ProgramFrame, font=("Arial", 14), width=10)
firstName.grid(row=8, column=1, sticky="W")

# Вивід рядка для вводу Прізвища вчителя
Label(ProgramFrame, font=("Arial", 14), text="Прізвище:").grid(row=9, column=0, sticky="E")
secondName = Entry(ProgramFrame, font=("Arial", 14), width=10)
secondName.grid(row=9, column=1, sticky="W")

# Вивід рядка для вводу По батькові вчителя
Label(ProgramFrame, font=("Arial", 14), text="По батькові:").grid(row=10, column=0, sticky="E")
fatherName = Entry(ProgramFrame, font=("Arial", 14), width=10)
fatherName.grid(row=10, column=1, sticky="W")


# Вивід рядка для вводу довільного SQL запиту
Label(ProgramFrame, font=("Arial", 14), text="SQL Запити:").grid(row=15, column=0, sticky="E")
sqlCommand = Entry(ProgramFrame, font=("Arial", 14), width=40)
sqlCommand.grid(row=15, column=1, sticky="W")

# Вивід кнопки для підтвердження змін в БД
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Змінити запис в БД", width=20)
generateNumbers.bind("<Button-1>",lambda event: ChangePostgrTable(int(teacherID.get()),int(DepartmentID.get()),str(firstName.get()),str(secondName.get()),str(fatherName.get())))
generateNumbers.grid(row=12, column=0)

# Вивід кнопки для виконання SQL запиту
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити запит", width=20)
generateNumbers.bind("<Button-1>",lambda event: executepostr(str(sqlCommand.get())))
generateNumbers.grid(row=16, column=1)

window.mainloop()
