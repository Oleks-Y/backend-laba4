import pymysql
from pymysql.cursors import DictCursor
from Connector import Connector
import configparser


class MySqlConnector(Connector):
    def __init__(self):
        super().__init__()
        self.conn = pymysql.connect(user='blyat',
                                    password='12345678',
                                    host='0.0.0.0',
                                    db='univercity',
                                    port=3307,
                                    charset='utf8mb4',
                                    # cursorclass=DictCursor,
                                    )
        pass

    def createDatabase(self):
        cur = self.conn.cursor()
        cur.execute("create table faculties (\
                     id bigint primary key  auto_increment ,\
                     faculty_name varchar(20) not null ,\
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

    def execute(self, text: str):
        cur = self.conn.cursor()
        return(cur.execute(text))

    def exportTo(self, connector: Connector):
        cur = self.conn.cursor()
        data = self._getAllTablesData(cur)
        connector.importData(data)

    def importData(self, data: dict):
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
    def _getAllTablesData(self, cur):
        cur.execute("SHOW TABLES;")
        tables = cur.fetchall()
        print(tables)
        data = {}
        for table in tables:
            tableName = table[0]
            cur.execute(f"select * from {tableName}")
            raws = cur.fetchall()
            data[tableName] = raws
        return data


if __name__=="main":
    a = MySqlConnector()
    # a.createDatabase()
    # a.dropAllTables()
    # print(a.execute("SELECT * FROM teachers;"))
    cur = a.getCursor()
    data = a._getAllTablesData(cur)
    a.importData(data)
