import pymysql
from pymysql.cursors import DictCursor
from Connector import Connector
import configparser

class MySqlConnector(Connector):
    def __init__(self):
        try:
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
        except Exception as ex:
            print(ex)
    
    tablesInDB = ['faculties','department','teachers','subject','subjects_to_teachers']

    def createDatabase(self):
        try:
            cur = self.conn.cursor()
            cur.execute("create table IF NOT EXISTS faculties (\
                         id INT primary key  auto_increment ,\
                         faculty_name varchar(100) not null\
                         );")
            cur.execute("create table IF NOT EXISTS department (\
                         id INT primary key  auto_increment,\
                         department_index varchar(100),\
                         faculty_id INT not null ,\
                         foreign key ( faculty_id) references  faculties (id)\
                         );")
            cur.execute("create table IF NOT EXISTS teachers ( \
                          id INT primary key  auto_increment,\
                          department_id INT,\
                          foreign key  (department_id) references  department (id),\
                          firstname varchar(50),\
                          lastname varchar(50),\
                          fathername varchar(50)\
                          );")
            cur.execute("create table IF NOT EXISTS subject( \
                          id INT primary key auto_increment,\
                          name varchar(100)  \
                          );")
            cur.execute("create table IF NOT EXISTS subjects_to_teachers( \
                         id INT primary key auto_increment,\
                         teacher_id INT ,\
                         subject_id INT,\
                         foreign key  (teacher_id) references teachers (id),\
                         foreign key  (subject_id) references  subject (id) \
                         )")
            print("MySQL база данных успешно создана")
        except Exception as ex:
            print(ex)

    def getCursor(self):
        return(self.conn.cursor())

    def dropAllTables(self):
        try:
            cur = self.conn.cursor()
            cur.execute("drop table IF EXISTS subjects_to_teachers")
            cur.execute("drop table IF EXISTS subject")
            cur.execute("drop table IF EXISTS teachers")
            cur.execute("drop table IF EXISTS department")
            cur.execute("drop table IF EXISTS faculties")
            print("MySQL база данных успешно очищена")
        except Exception as ex:
            print(ex)

    def execute(self, text: str):
        try:
            cur = self.conn.cursor()
            return(cur.execute(text))
            self.conn.commit()
        except Exception as ex:
            print(ex)

    def executemany(self, text,table):
        try:  
            cur = self.conn.cursor()
            cur.executemany(text,table)
            self.conn.commit()
        except Exception as ex:
            print(ex)

    def exportTo(self, connector: Connector):
        try:
            cur = self.conn.cursor()
            data = self._getAllTablesData(cur)
            connector.importData(data)
        except Exception as ex:
            print(ex)

    def importData(self, data: dict):
        try:
            cur = self.getCursor()
            for table in data.keys():
                print(f'Inserting into table {table} values {data[table]}')
                rawCount = cur.execute(f"SELECT * FROM {table}")
                if data[table] == ():
                    continue
                string = "(" + ",".join(["%s" for value in data[table][0]]) + ")"
                query = f"INSERT INTO {table} VALUES {string}"
                for raw in data[table]:
                    rawCount+=1
                    rawList = list(raw)
                    rawList[0]=rawCount
                    cur.execute(query,rawList)  # data[table])
            print("Успешно импортированы данные с иной БД в MYSQL БД")
        except Exception as ex:
            print(ex)
    def _getAllTablesData(self, cur):
        try: 
            cur = self.getCursor()
            cur.execute("SHOW TABLES;")
            tables = cur.fetchall()
            data = {}
            for table in tables:
                tableName = table['Tables_in_mysql']
                if tableName in self.tablesInDB:
                    cur.execute(f"select * from {tableName}")
                    raws = cur.fetchall()
                    data[tableName] = raws
            return data
        except Exception as ex:
            print(ex)
