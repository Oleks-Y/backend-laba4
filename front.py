from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

window = Tk()

# Встановлення підпису вікна
window.title("CRUD")
# Встановлення розміру вікна
window.geometry('800x400')

#Створюємо рамку для розмітки
ProgramFrame = Frame(window)
ProgramFrame.pack(side=LEFT, fill=BOTH, expand=True)

# Створюємо кнопки для створення та експорту БД
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити БД1", width=20)
generateNumbers.grid(row=1, column=0)

generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД1 у БД2", width=20)
generateNumbers.grid(row=2, column=0)

generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Експорт БД2 у БД3", width=20)
generateNumbers.bind("<Button-1>",lambda event: Createmysql(int(startColumn.get())))
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

# Вивід рядка для вводу номера початкового рядка для експорту
Label(ProgramFrame, font=("Arial", 14), text="З якого Рядка почати експорт :").grid(row=3, column=0, sticky="E")
startColumn = Spinbox(ProgramFrame, font=("Arial", 14), width=9, from_=0, to=4)
startColumn.grid(row=3, column=1, sticky="W")

# Вивід рядка для вводу довільного SQL запиту
Label(ProgramFrame, font=("Arial", 14), text="SQL Запити:").grid(row=15, column=0, sticky="E")
sqlCommand = Entry(ProgramFrame, font=("Arial", 14), width=40)
sqlCommand.grid(row=15, column=1, sticky="W")

# Вивід кнопки для підтвердження змін в БД
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Змінити запис в БД", width=20)
generateNumbers.bind("<Button-1>",lambda event: ChangeBD2(int(teacherID.get()),int(DepartmentID.get()),str(firstName.get()),str(secondName.get()),int(fatherName.get())))
generateNumbers.grid(row=12, column=0)

# Вивід кнопки для виконання SQL запиту
generateNumbers = Button(ProgramFrame, font=("Arial", 14), text="Створити запит", width=20)
generateNumbers.bind("<Button-1>",lambda event: createsqliteCRUD(str(sqlCommand.get())))
generateNumbers.grid(row=16, column=1)

window.mainloop()
