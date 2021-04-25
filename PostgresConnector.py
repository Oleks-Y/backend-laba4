import psycopg2
from Connector import Connector
import configparser


class PostgresConnector(Connector):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            database="university",
            user="prepod",
            password="12345678",
            host="0.0.0.0",
            port=8012
                    )
        cur = self.conn.cursor()

        #cur.execute("create sequence faculties_seq;")

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

    def execute(self, text):
        cur = self.conn.cursor()
        return(cur.execute(text))
        self.conn.commit()
    def exportTo(self, connector: Connector):
        cur = self.conn.cursor()
        data = self._getAllTablesData(cur)
        connector.importData(data)

    def importData(self, data: dict):
        cur = self.getCursor()
        for table in data.keys():
            print(f'Inserting into table {table} values {data[table]}')
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            rawCount = cur.fetchone()[0]
            if data[table] == []:
                continue
            string = "(" + ",".join(["%s" for value in data[table][0]]) + ")"
            query = f"INSERT INTO {table} VALUES {string}"
            for raw in data[table]:
                rawCount+=1
                rawList = list(raw)
                rawList[0]=rawCount
                cur.execute(query,rawList)
            print(f"Insert Into {table} Done ")
            self.conn.commit()
    def _getAllTablesData(self, cur):
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        # cur.execute("Select * from faculties")
        tables = cur.fetchall()
        print("Tables :",tables)
        data = {}
        for table in tables:
            tableName = table[0]
            cur.execute(f"select * from {tableName}")
            raws = cur.fetchall()
            data[tableName] = raws
        return data


if __name__=="__main__":
    a = PostgresConnector()
    # a.createDatabase()
    # a.dropAllTables()
    # print(a.execute("SELECT * FROM teachers;"))
    cur = a.getCursor()
    data = a._getAllTablesData(cur)
    a.importData(data)
    print('Done')
