import psycopg2
from Connector import Connector
import configparser


class PostgresConnector(Connector):
    def __init__(self):
        try:
            super().__init__()
            config = configparser.ConfigParser()
            config.read_file(open("conf.ini", "r"))
            if not "Postgres" in config:
                raise Exception("Please specify Postgres config")
            dbConf = config["Postgres"]
            # dsn = 'host={dbConf["Host"]} dbname={dbConf["Database"]} user={dbConf["User"]} password={dbConf["Password"]}'
            dsn = "host={} dbname={} user={} password={}".format(dbConf["Host"], dbConf["Database"], dbConf["User"],dbConf["Password"])
            self.conn = psycopg2.connect(
                                          database = dbConf["Database"],
                                          user=dbConf["User"], 
                                          password=dbConf["Password"], 
                                          host=dbConf["Host"], 
                                          port=dbConf["Port"],
                                        )
            cur = self.conn.cursor()
        except Exception as ex:
            print(ex)

    tablesInDB = ['faculties','department','teachers','subject','subjects_to_teachers']

    def createDatabase(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""create table faculties (
                        id bigint primary key NOT NULL,
                        faculty_name varchar(100) NOT NULL
                        );""")
            #cur.execute("create sequence department_seq;")
            cur.execute("""create table department (
                         id bigint primary key NOT NULL,
                         department_index varchar(100) NOT NULL,
                         faculty_id bigint NOT NULL ,
                         foreign key ( faculty_id) references  faculties (id)
                         );""")
            #cur.execute("create sequence teachers_seq;")
            cur.execute("""create table teachers (
                        id bigint primary key NOT NULL,
                        department_id bigint NOT NULL,
                        foreign key  (department_id) references  department (id),
                        firstname varchar(50) NOT NULL,
                        lastname varchar(50) NOT NULL ,
                        fathername varchar(50) NOT NULL
                        );""")
            #cur.execute("create sequence subject_seq;")
            cur.execute("""create table subject(
                         id bigint primary key NOT NULL,
                         name varchar(100) NOT NULL
                         );""")
            #cur.execute("create sequence subjects_to_teachers_seq;")
            cur.execute("""create table subjects_to_teachers(
                         id bigint primary key NOT NULL,
                         teacher_id bigint NOT NULL,
                         subject_id bigint NOT NULL,
                         foreign key  (teacher_id) references teachers (id),
                         foreign key  (subject_id) references  subject (id)
                         );""")
            self.conn.commit()
            print("Postgress база данных успешно создана")
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
            self.conn.commit()
            print("Postgress база данных успешно очищена")
        except Exception as ex:
            print(ex)

    def execute(self, text):
        try:
            cur = self.conn.cursor()
            cur.execute(text)
            self.conn.commit()
            return(cur.fetchall())
        except Exception as ex:
            print(ex)
    def executemany(self, text,list: str):
        try:
            cur = self.conn.cursor()
            cur.executemany(text,list)
            return(self.conn.commit())
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
            for table in self.tablesInDB:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                rawCount = cur.fetchone()[0]
                if data[table] == []:
                    continue
                string = "(" + ",".join(["%s" for value in data[table][0]]) + ")"
                query = f"INSERT INTO {table} VALUES {string};"
                a = []
                for i in data[table]:
                    a.append(tuple(i.values()))
                cur.executemany(query,a)
                self.conn.commit()
            print("Успешно импортированы данные с иной БД в Postgres")
        except Exception as ex:
            print(ex)

    def _getAllTablesData(self, cur):
        try:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
            # cur.execute("Select * from faculties")
            tables = cur.fetchall()
            data = {}
            for table in tables:
                tableName = table[0]
                cur.execute(f"select * from {tableName}")
                raws = cur.fetchall()
                data[tableName] = raws
            #print(data)
            return data
        except Exception as ex:
            print(ex)