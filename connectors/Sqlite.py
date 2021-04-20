import sqlite3
from Connector import Connector

class SqliteConnector(Connector): 
    def __init__(self): 
        self.conn = sqlite3.connect(":memory:")
    def select(self, fields, table, query):
        pass 
    def insert(self, data, table):
        pass 
    def update(self, data, table, query):
        pass 
    def delete(self, table, query):
        pass
    def createDatabase(self):
        cursor = self.conn.cursor()
        cursor.execute("""create table faculties (
                        id bigint primary key ,
                        faculty_name TEXT not null ,
                        university_name TEXT not null
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
        self.conn.commit()
        # Зберігаємо зміни       
        pass
    def getCursor(self):
        return(self.conn.cursor())
    def dropAllTables(self):
        cur = self.conn.cursor()
        cur.execute("drop table subjects_to_teachers;")
        cur.execute("drop table subject;")
        cur.execute("drop table teachers;")
        cur.execute("drop table department;")
        cur.execute("drop table faculties;")
    def execute(self,text):
        cur = self.conn.cursor()
        return(cur.execute(text))

a = SqliteConnector()
a.createDatabase()
a.dropAllTables()
print(a.getCursor())