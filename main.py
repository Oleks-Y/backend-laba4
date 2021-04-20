import sqlite3
from mysql.connector import connect, Error
import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from subprocess import Popen, PIPE
from ctypes import windll


connSQL = sqlite3.connect(":memory:")
# connMYSQL = mysql.connector.connect(host = "0.0.0.0",    # your host, usually localhost
#                      port = "3307",
#                      user="root",         # your username
#                      passwd="12345678",  # your password
#                      db="mysql")        # name of the data base

with connect(
        host="localhost",
        port = "3307",
        user="root",
        password="12345678",
    ) as connection:
        print(connection)

con = psycopg2.connect(
  database = "postgres",
  user="postgres", 
  password="mysecretpassword", 
  host="localhost", 
  port="8012",
)

# conn = psycopg2.connect(dbname='postgres', user='postgres', 
#                         password='mysecretpassword', host='0.0.0.0',port = '8012')

print(connection)
print(connSQL)
print(con)

def LengthValidate(*args):
    try:
        # Якщо введений діапазон більше 7, то встановлюємо значення 7
        if int(ID.get()) > 7:
            ID.delete(0, 'end')
            ID.insert(0, 7)
        # Якщо аведений діапазон менше 0, то встановлюємо значення 0
        elif int(ID.get()) < 0:
            ID.delete(0, 'end')
            ID.insert(0, 0)
    # Якщо аведене значення викликає ексепшн, то встановлюємо значення 0
    except:
        ID.delete(0, 'end')
        ID.insert(0, 0)

def Length2Validate(*args):
    try:
        # Якщо введений діапазон більше 9999, то встановлюємо значення 9999
        if int(ID.get()) > 9999:
            ID.delete(0, 'end')
            ID.insert(0, 9999)
        # Якщо аведений діапазон менше 0, то встановлюємо значення 0
        elif int(ID.get()) < 0:
            ID.delete(0, 'end')
            ID.insert(0, 0)
    # Якщо аведене значення викликає ексепшн, то встановлюємо значення 0
    except:
        ID.delete(0, 'end')
        ID.insert(0, 0)

root = Tk()
# Встановлення параметрів, для того, щоб програма гарно виглядала на екранах із високим DPI
windll.shcore.SetProcessDpiAwareness(1)

# Встановлення підпису вікна
root.title("Система для управління базами даних")
# Встановлення розміру вікна
root.geometry('700x600')
# Заблоковуємо можливість зміни розміру вікна
root.resizable(width=FALSE, height=FALSE)

# Створюємо рамку для інструкції
GeneralInfoFrame = Frame(root)

ProgramFrame = Frame(root)
ProgramFrame.pack(side=TOP, fill=Y, expand=1, pady=10)

# generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД1 у БД2", command=PostgreSQL, width=20)
# generateNumbers.grid(row=2, column=0, columnspan=1)
# generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Змінити запис в БД", width=20)
# generateNumbers.bind("<Button-1>",lambda event: ChangeBD2(int(ID.get()),str(Name.get()),str(Date.get()),int(Number.get())))
# generateNumbers.grid(row=8, column=0, columnspan=1)
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД2 у БД3", width=20)
# generateNumbers.bind("<Button-1>",lambda event: Createmysql(int(Numb.get())))
generateNumbers.grid(row=10, column=0, columnspan=1)
# generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити запит", width=20)
# generateNumbers.bind("<Button-1>",lambda event: createsqliteCRUD(str(sql.get())))
generateNumbers.grid(row=13, column=0, columnspan=1)



# Вивід рядка "ID:"
Label(ProgramFrame, font=("Arial", 14), text="ID:") \
    .grid(row=4, column=0, sticky="E")

# Поле для вводу значень довжини списку
ID = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=1, to=8)
ID.grid(row=4, column=1, sticky="W")
# Якщо фокус на елементі був втсрачений, виконуємо перевірку введених значень
ID.bind("<FocusOut>", LengthValidate)

Label(ProgramFrame, font=("Arial", 14), text="Назва товару:") \
    .grid(row=5, column=0, sticky="E")
Name = Entry(ProgramFrame, font=("Arial", 14), width=10)
Name.grid(row=5, column=1, sticky="W")
# Якщо фокус на елементі був втсрачений, виконуємо перевірку введених значень

# Вивід рядів для ввода даних :"
Label(ProgramFrame, font=("Arial", 14), text="Строк придатності:") \
    .grid(row=6, column=0, sticky="E")
Date = Entry(ProgramFrame, font=("Arial", 14), width=10)
Date.grid(row=6, column=1, sticky="W")

Label(ProgramFrame, font=("Arial", 14), text="Кількість товару:") \
    .grid(row=7, column=0, sticky="E")
Number = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=0, to=9999)
Number.grid(row=7, column=1, sticky="W")
# Якщо фокус на елементі був втсрачений, виконуємо перевірку введених значень
Number.bind("<FocusOut>", Length2Validate)

Label(ProgramFrame, font=("Arial", 14), text="З якого Рядка почати експорт :") \
    .grid(row=9, column=0, sticky="E")
Numb = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=0, to=4)
Numb.grid(row=9, column=1, sticky="W")

Label(ProgramFrame, font=("Arial", 14), text="SQL Запити:") \
    .grid(row=11, column=0, sticky="E")
sql = Entry(ProgramFrame, font=("Arial", 14), width=50)
sql.grid(row=12, column=0, sticky="W")

root.mainloop()
