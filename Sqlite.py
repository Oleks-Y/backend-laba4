import sqlite3
from Connector import Connector


class SqliteConnector(Connector):
    def __init__(self):
        try:
            self.conn = sqlite3.connect(":memory:")
        except Exception as ex:
            print(ex)

    tablesInDB = ['faculties','department','teachers','subject','subjects_to_teachers']

    def createDatabase(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""create table faculties (
                            id bigint primary key ,
                            faculty_name TEXT not null
                            );
                        """)
            self.conn.commit()
            cursor.execute("""create table department (
                            id bigint primary key,
                            department_index TEXT,
                            faculty_id bigint not null ,
                            foreign key ( faculty_id) references  faculties (id)
                            );
                        """)
            self.conn.commit()
            cursor.execute("""create table teachers (
                            id bigint primary key,
                            department_id bigint,
                            firstname TEXT,
                            lastname TEXT,
                            fathername TEXT,
                            foreign key  (department_id) references  department (id)
                            );
                        """)
            self.conn.commit()
            cursor.execute("""create table subject(
                            id bigint primary key,
                            name TEXT
                            );
                        """)
            self.conn.commit()
            cursor.execute("""create table subjects_to_teachers(
                            id bigint primary key,
                            teacher_id bigint ,
                            subject_id bigint,
                            foreign key  (teacher_id) references teachers (id),
                            foreign key  (subject_id) references  subject (id)
                            );
                        """)
            print("SQLite база данных успешно создана")
            self.conn.commit()
        except Exception as ex:
            print(ex)

    def getCursor(self):
        try:
            return(self.conn.cursor())
        except Exception as ex:
            print(ex)

    def dropAllTables(self):
        try:
            cur = self.conn.cursor()
            cur.execute("drop table IF EXISTS subjects_to_teachers;")
            cur.execute("drop table IF EXISTS subject;")
            cur.execute("drop table IF EXISTS teachers;")
            cur.execute("drop table IF EXISTS department;")
            cur.execute("drop table IF EXISTS faculties;")
            print("SQLite база данных успешно очищена")
        except Exception as ex:
            print(ex)

    def execute(self, text):
        try:
            cur = self.conn.cursor()
            return(cur.execute(text))
        except Exception as ex:
            print(ex)
    
    def executemany(self, text,table: str):
        try:
            cur = self.conn.cursor()
            return(cur.executemany(text,table))
        except Exception as ex:
            print(ex)

    def exportTo(self, connector):
        pass
    def importData(self, data):
        try:
            cur = self.getCursor()
            for table in self.tablesInDB:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                rawCount = cur.fetchone()[0]
                if data[table] == []:
                    continue
                string = "(" + ",".join(["?" for value in data[table][0]]) + ")"
                query = f"INSERT INTO {table} VALUES {string};"
                a = []
                cur.executemany(query,data[table])
                self.conn.commit()
            cur.execute("select * from faculties;")
            rows = cur.fetchall()
            print("Успешно импортированы данные с иной БД в SQLite")
        except Exception as ex:
            print(ex)

    def changeRaw():
        pass
