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
        cur.execute("create sequence faculties_seq;")
        cur.execute("create table faculties (\
                    id bigint primary key  default nextval ('faculties_seq') ,\
                    faculty_name varchar(20) not null ,\
                    university_name varchar(50) not null\
                    );")
        cur.execute("create sequence department_seq;")
        cur.execute("create table department (\
                     id bigint primary key  default nextval ('department_seq'),\
                     department_index varchar(20),\
                     faculty_id bigint not null ,\
                     foreign key ( faculty_id) references  faculties (id)\
                     );")
        cur.execute("create sequence teachers_seq;")
        cur.execute("create table teachers (\
                    id bigint primary key  default nextval ('teachers_seq'),\
                    department_id bigint,\
                    foreign key  (department_id) references  department (id),\
                    firstname varchar(50),\
                    lastname varchar(50),\
                    fathername varchar(50)\
                    );")
        cur.execute("create sequence subject_seq;")
        cur.execute("create table subject(\
                     id bigint primary key default nextval ('subject_seq'),\
                     name varchar(20)\
                     );")
        cur.execute("create sequence subjects_to_teachers_seq;")
        cur.execute("create table subjects_to_teachers(\
                     id bigint primary key default nextval ('subjects_to_teachers_seq'),\
                     teacher_id bigint ,\
                     subject_id bigint,\
                     foreign key  (teacher_id) references teachers (id),\
                     foreign key  (subject_id) references  subject (id)\
                     );")
        pass


a = PostgresConnector()
print("Done")
