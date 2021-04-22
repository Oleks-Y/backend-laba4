import psycopg2
from Connector import Connector
import configparser

class PostgresConnector(Connector):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read_file(open("conf.ini", "r"))
        if not "Postgres" in config:
            raise Exception("Please specify Postgres config")
        dbConf = config["Postgres"]
        # dsn = 'host={dbConf["Host"]} dbname={dbConf["Database"]} user={dbConf["User"]} password={dbConf["Password"]}'
        dsn = "host={} dbname={} user={} password={}".format(dbConf["Host"], dbConf["Database"], dbConf["User"],dbConf["Password"])
        print(dbConf["User"])
        self.conn = psycopg2.connect(
                                      database = dbConf["Database"],
                                      user=dbConf["User"], 
                                      password=dbConf["Password"], 
                                      host=dbConf["Host"], 
                                      port=dbConf["Port"],
                                    )
        cur = self.conn.cursor()

        #cur.execute("create sequence faculties_seq;")

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

        #cur.execute("create sequence faculties_seq;")
        cur.execute("""create table faculties (
                    id bigint primary key NOT NULL,
                    faculty_name varchar(20) NOT NULL,
                    );""")
        #cur.execute("create sequence department_seq;")
        cur.execute("""create table department (
                     id bigint primary key NOT NULL,
                     department_index varchar(20) NOT NULL,
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
                     name varchar(20) NOT NULL
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
    def getCursor(self):
        return(self.conn.cursor())
    def dropAllTables(self):
        cur = self.conn.cursor()
        print(cur)
        cur.execute("drop table subjects_to_teachers;")
        cur.execute("drop table subject;")
        cur.execute("drop table teachers;")
        cur.execute("drop table department;")
        cur.execute("drop table faculties;")
        self.conn.commit()
    def execute(self,text):
        cur = self.conn.cursor()
        return(cur.execute(text))
        self.conn.commit()
        

a = PostgresConnector()
#a.createDatabase()
a.dropAllTables()
#print(a.execute('select * from department;'))
