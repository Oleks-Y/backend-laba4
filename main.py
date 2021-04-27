import sqlite3
from mysql.connector import connect, Error
import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from subprocess import Popen, PIPE
from ctypes import windll
from connectors.MySqlConnector import MySqlConnector
from connectors.PostgresConnector import PostgresConnector
from connectors.Sqlite import SqliteConnector
from connectors.Connector import Connector



MySql = MySqlConnector()
MySql.createDatabase()

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


def createDB():
    MySql.executemany("INSERT INTO faculties VALUES (?,?)", faculties)
    MySql.executemany("INSERT INTO department VALUES (?,?,?)", departments)
    MySql.executemany("INSERT INTO teachers VALUES (?,?,?,?,?)", teachers)
    MySql.executemany("INSERT INTO subject VALUES (?,?)", subjects)
    MySql.executemany("INSERT INTO subjects_to_teachers VALUES (?,?,?)", subjects_to_teachers)