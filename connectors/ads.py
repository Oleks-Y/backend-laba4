# Імпортуємо необхідні бібліотеки
from tkinter import *
from ctypes import windll
import sqlite3
import psycopg2
from subprocess import Popen, PIPE
import tkinter as tk
import tkinter.ttk as ttk
import pymysql
import mysql.connector
# Mетод для роботи з базою даних SQLite
def createsqlite():
    # Створюємо БД в оперативній пам'яті
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # Створюємо 3 таблиці
    cursor.execute("""CREATE TABLE Product_Name
                    (Product_Id number, Poduct_Name text, Date_Id number,Available_Id number)
                """)
    conn.commit()            
    cursor.execute("""CREATE TABLE Product_Date
                    (Date_Id number, release_date text)
                """)
    conn.commit()
    cursor.execute("""CREATE TABLE Product_Availability
                    (Available_Id number, Available_count number)
                """)   
    # Зберігаємо зміни
    conn.commit()           
    
    # Вставляємо багато даних, використовуючи безпечний метод "?"
    albums1 = [(1, 'bacon',1,1),
            (2, 'peanut',2,2),
            (3, 'cherry',3,2),
            (4, 'broccoli',4,4),
            (5, 'lemon',5,5),
            (6, 'cucumber',6,6),
            (7, 'onion',7,7),
            (8, 'potato',8,8)]
    albums2 = [(1,'7/9/2025'),
            (2,'7/9/2023'),
            (3,'2/1/2022'),
            (4, '4/17/2022'),
            (5, '4/10/2021'),
            (6,  '4/17/2021'),
            (7,  '5/17/2022'),
            (8,  '6/17/2023')]  
    albums3 = [(1,0),
            (2,101),
            (3,13),
            (4, 45),
            (5, 15),
            (6,  16),
            (7,  10),
            (8,  8)]        
    
    cursor.executemany("INSERT INTO Product_Availability VALUES (?,?)", albums3)
    cursor.executemany("INSERT INTO Product_Date VALUES (?,?)", albums2)
    cursor.executemany("INSERT INTO Product_Name VALUES (?,?,?,?)", albums1)
    

    conn.commit()
    # Виводимо БД
    print("База даних SQLite\n")

    print("Таблиця з продуктами\n")
    for row in cursor.execute("SELECT * FROM Product_Name ORDER BY Product_Id"):
        print(row)
    print("\n")
    print("Таблиця з датами\n")
    for row in cursor.execute("SELECT * FROM Product_Date ORDER BY Date_Id"):
        print(row)
    print("\n")
    print("Таблиця з кількістю продуктів\n")
    for row in cursor.execute("SELECT * FROM Product_Availability ORDER BY Available_Id"):
        print(row)
    print("\n")
    return conn
# Функція для експорта БД1 в БД2 
def createsqliteCRUD(sql):
    DB = createsqlite()
    
    
    cursor = DB.cursor()
    if(sql.startswith('SELECT')):
        cursor.execute(sql)

        rows = cursor.fetchall()
        print(rows)
        out1 = Label(ProgramFrame, font=("Arial", 12), text=rows, wraplength=520)
        out1.grid(row=16, column=0, sticky="W")

    else:    
        cursor.execute(sql)
        out1 = Label(ProgramFrame, font=("Arial", 12), text='Команда виконана', wraplength=520)
        out1.grid(row=16, column=0, sticky="W")
    
    DB.commit()

    print("База даних SQLite\n")

    print("Таблиця з продуктами\n")
    for row in cursor.execute("SELECT * FROM Product_Name ORDER BY Product_Id"):
        print(row)
    print("\n")
    print("Таблиця з датами\n")
    for row in cursor.execute("SELECT * FROM Product_Date ORDER BY Date_Id"):
        print(row)
    print("\n")
    print("Таблиця з кількістю продуктів\n")
    for row in cursor.execute("SELECT * FROM Product_Availability ORDER BY Available_Id"):
        print(row)
    print("\n")
def PostgreSQL():
    # ОТримуємо БД1
    DB = createsqlite()
    # Створюємо з'єднання з базою
    conn2 = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432")
    cur = conn2.cursor()
    # Видаляємо попередньо створені таблиці
    cur.execute("DROP TABLE Product_Name;")
    cur.execute("DROP TABLE Product_Availability;")
    cur.execute("DROP TABLE Product_Date;")
    # Створюємо таблиці
    cur.execute('''CREATE TABLE Product_Availability
      (Availability_ID INT PRIMARY KEY     NOT NULL,
      Available_count           INT    NOT NULL)
      ;''')
    cur.execute('''CREATE TABLE Product_Date
      (Date_ID INT PRIMARY KEY     NOT NULL,
      release_date          TEXT     NOT NULL)
      ;''')
    cur.execute('''CREATE TABLE Product_Name
      (Product_ID INT PRIMARY KEY     NOT NULL,
      Poduct_Name           TEXT    NOT NULL,
      Prod_Date_ID          INT  REFERENCES Product_Date ,
      Product_Availability INT REFERENCES Product_Availability)
      ;''') 
    cursor = DB.cursor()
    # Переносимо дані з БД1 до БД2
    for row in cursor.execute("SELECT  * FROM Product_Date ORDER BY Date_ID"):
        row2 = 'INSERT INTO Product_Date (Date_ID,release_date) VALUES '+ str(row)
        #print(row2)
        cur.execute(row2)
    conn2.commit()
    for row in cursor.execute("SELECT  * FROM Product_Availability ORDER BY Available_Id"):
        row2 = 'INSERT INTO Product_Availability (Availability_ID,Available_count) VALUES '+ str(row)
        #print(row2)
        cur.execute(row2)
    conn2.commit()
    for row in cursor.execute("SELECT  * FROM Product_Name ORDER BY Product_Id"):
        row2 = 'INSERT INTO Product_Name (Product_ID,Poduct_Name,Prod_Date_ID, Product_Availability ) VALUES '+ str(row)
        cur.execute(row2)
    conn2.commit()
    # Виводимо базу даних
    print("База даних PostgreSQL\n")

    cur.execute("SELECT * from Product_Name")
    rows = cur.fetchall()
    print("Таблиця з продуктами\n")
    for row in rows:
        print(row)
    print("\n")

    cur.execute("SELECT * from Product_Date")
    rows = cur.fetchall()
    print("Таблиця з датами\n")
    for row in rows:
        print(row)
    print("\n")

    cur.execute("SELECT * from Product_Availability")
    rows = cur.fetchall()
    print("Таблиця з наявністю\n")
    for row in rows:
        print(row)
    print("\n")
    #print("Operation done successfully")  
    conn2.close()  
    return conn2
    # Функція для роботи з БД3
def Createmysql(numb):
    # Створюємо підключення до БД
    DB3 = mysql.connector.connect(
    host="localhost",
    user="Anton",
    password="1234",database="sklad2")
    mycursor = DB3.cursor()
    # Видаляємо попередньо створені таблиці
    mycursor.execute("DROP TABLE Product_Name")
    mycursor.execute("DROP TABLE Product_Date")
    mycursor.execute("DROP TABLE Product_Availability")
    
    DB3.commit()
    # Створюємо таблиці

    create_Date = """
CREATE TABLE Product_Date(
    ID INT PRIMARY KEY,
    Date VARCHAR(20)
)
"""
   # mycursor.execute(create_Date)
    mycursor.execute(create_Date)
    DB3.commit()
     

    create_Product_Availability = """
CREATE TABLE Product_Availability(
    ID INT PRIMARY KEY,
    Availability INT
)
"""
    mycursor.execute(create_Product_Availability)
    DB3.commit()
    create_Product_name = """
CREATE TABLE Product_Name(
    ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Product_Date_id INT,
    Availability_ID INT,
    FOREIGN KEY (Product_Date_id) REFERENCES Product_Date (ID),
    FOREIGN KEY (Availability_ID) REFERENCES Product_Availability (ID));"""
    mycursor.execute(create_Product_name)
    DB3.commit()
    conn2 = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432")
    cur = conn2.cursor()
    # Заповнюємо БД3, вибираючи 4 записи з БД2, починаючи з number
    cur.execute("SELECT * from Product_Availability")
    rows = cur.fetchall()
    sql = "INSERT INTO Product_Availability (ID, Availability) VALUES (%s, %s)"
    mycursor.executemany(sql, rows[numb:int(numb+4)])

    cur.execute("SELECT * from Product_Date")
    rows = cur.fetchall()
    sql = "INSERT INTO Product_Date (ID, Date) VALUES (%s, %s)"
    mycursor.executemany(sql, rows[numb:int(numb+4)])
    
    cur.execute("SELECT * from Product_Name")
    rows = cur.fetchall()
    sql = "INSERT INTO Product_Name (ID, Name, Product_Date_id, Availability_ID) VALUES (%s, %s, %s, %s)"
    mycursor.executemany(sql, rows[numb:int(numb+4)])
    print(mycursor.rowcount, "was inserted.")
    print("\n")
    # Вивидимо базу даних

    print("База даних MySQL\n")

    mycursor.execute("SELECT * from Product_Name")
    rows = mycursor.fetchall()
    print("Таблиця з продуктами\n")
    for row in rows:
        print(row)
    print("\n")

    mycursor.execute("SELECT * from Product_Date")
    rows = mycursor.fetchall()
    print("Таблиця з датами\n")
    for row in rows:
        print(row)
    print("\n")

    mycursor.execute("SELECT * from Product_Availability")
    rows = mycursor.fetchall()
    print("Таблиця з наявністю\n")
    for row in rows:
        print(row)
    print("\n")
    
# Функція для змінення поля в БД
def ChangeBD2(ID,Poduct_Name,Date,Available_number):
# Підключаємось до БД
    conn2 = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432")
    cur = conn2.cursor()
    kav = str("'")
    # Створюємо запис для оновлення поля
    stringUPdate = '''UPDATE Product_Name
 SET Poduct_Name = '''+kav+str(Poduct_Name)+kav+'''
 WHERE Product_ID = '''+str(ID)+''';'''
    cur.execute(stringUPdate)
    
    cur.execute('''SELECT Prod_Date_ID FROM Product_Name
 WHERE Product_ID = '''+str(ID)+''';''')
    id = cur.fetchone()
    print(id[0])


    stringUPdate = '''
    
 UPDATE Product_Date
 SET release_date = '''+kav+str(Date)+kav+'''
 WHERE Date_ID = '''+str(id[0])+''';'''
    cur.execute(stringUPdate)
    cur.execute('''SELECT Product_Availability FROM Product_Name
 WHERE Product_ID = '''+str(ID)+''';''')
    id = cur.fetchone()
    stringUPdate = '''
    
 UPDATE Product_Availability
 SET Available_count = '''+kav+str(Available_number)+kav+'''
 WHERE Availability_ID = '''+str(id[0])+''';'''
    cur.execute(stringUPdate)
    # Виводимо БД зі зміненими параметрами
    print("База даних PostgreSQL\n")

    cur.execute("SELECT * from Product_Name")
    rows = cur.fetchall()
    print("Таблиця з продуктами\n")
    for row in rows:
        print(row)
    print("\n")

    cur.execute("SELECT * from Product_Date")
    rows = cur.fetchall()
    print("Таблиця з датами\n")
    for row in rows:
        print(row)
    print("\n")

    cur.execute("SELECT * from Product_Availability")
    rows = cur.fetchall()
    print("Таблиця з наявністю\n")
    for row in rows:
        print(row)
    print("\n")
    
     
    conn2.commit()
     

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
GeneralInfoFrame.pack(side=TOP, fill=X)

# Створюємо рамку для збереження загальної функціональності програми
ProgramFrame = Frame(root)
ProgramFrame.pack(side=TOP, fill=Y, expand=1, pady=10)

# Вписуємо інструкції в рамку для інструкцій
ListLengthInstructions = Label(GeneralInfoFrame, font=("Arial", 14),
                               text='Клонування баз даних')
ListLengthInstructions.pack(side=TOP)
# Створюємо необхідні кнопки
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити БД1", command=createsqlite, width=20)
generateNumbers.grid(row=1, column=0, columnspan=1)

generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД1 у БД2", command=PostgreSQL, width=20)
generateNumbers.grid(row=2, column=0, columnspan=1)
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Змінити запис в БД", width=20)
generateNumbers.bind("<Button-1>",lambda event: ChangeBD2(int(ID.get()),str(Name.get()),str(Date.get()),int(Number.get())))
generateNumbers.grid(row=8, column=0, columnspan=1)
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД2 у БД3", width=20)
generateNumbers.bind("<Button-1>",lambda event: Createmysql(int(Numb.get())))
generateNumbers.grid(row=10, column=0, columnspan=1)
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити запит", width=20)
generateNumbers.bind("<Button-1>",lambda event: createsqliteCRUD(str(sql.get())))
generateNumbers.grid(row=13, column=0, columnspan=1)

#INSERT INTO Product_Date VALUES (9,'11/11/1111')
# Метод для валідації введених значень, які були введені користувачем для довжини списку
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




def main():
    #DB1 = createsqlite()
    
    #DB2 = PostgreSQL()
    #Createmysql()
    

    root.mainloop()



# Запуск методу main
if __name__ == '__main__':
    main()
