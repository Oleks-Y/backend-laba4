import pymysql
from pymysql.cursors import DictCursor
from Connector import Connector
import configparser


class MySqlConnector(Connector):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read_file(open("conf.ini", "r"))
        if not 'MySql' in config:
           raise Exception("Please specify Postgres config")
        dbConf = config["MySql"]
        self.conn = pymysql.connect(user='root',
                                    database=dbConf["database"],
                                    password='12345678',
                                    host=dbConf["host"],
                                    port=int(dbConf["port"]),
                                    charset='utf8mb4',
                                    cursorclass=DictCursor,
                                    )
        pass

    def select(self, fields, table, query):
        pass

    def insert(self, data, table):
        pass

    def update(self, data, table, query):
        pass

    def delete(self, table, query):
        pass

    def createDatabase(self):
        cur = self.conn.cursor()
        cur.execute("create table faculties (\
                     id bigint primary key  auto_increment ,\
                     faculty_name varchar(20) not null ,\
                     university_name varchar(50) not null\
                     );")
        cur.execute("create table department (\
                     id bigint primary key  auto_increment,\
                     department_index varchar(20),\
                     faculty_id bigint not null ,\
                     foreign key ( faculty_id) references  faculties (id)\
                     );")
        cur.execute("create table teachers ( \
                      id bigint primary key  auto_increment,\
                      department_id bigint,\
                      foreign key  (department_id) references  department (id),\
                      firstname varchar(50),\
                      lastname varchar(50),\
                      fathername varchar(50)\
                      );")
        cur.execute("create table subject( \
                      id bigint primary key auto_increment,\
                      name varchar(20)  \
                      );")
        cur.execute("create table subjects_to_teachers( \
                     id bigint primary key auto_increment,\
                     teacher_id bigint ,\
                     subject_id bigint,\
                     foreign key  (teacher_id) references teachers (id),\
                     foreign key  (subject_id) references  subject (id) \
                     )")
        pass
    def getCursor(self):
        return(self.conn.cursor())
    def dropAllTables(self):
        cur = self.conn.cursor()
        cur.execute("drop table subjects_to_teachers")
        cur.execute("drop table subject")
        cur.execute("drop table teachers")
        cur.execute("drop table department")
        cur.execute("drop table faculties")
    def execute(self,text):
        cur = self.conn.cursor()
        return(cur.execute(text))

        


a = MySqlConnector()
#a.createDatabase()
a.dropAllTables()
print(a.execute("SELECT * FROM teachers;"))
