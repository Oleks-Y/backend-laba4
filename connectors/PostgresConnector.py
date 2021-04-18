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
        self.conn = psycopg2.connect(dsn)


    def select(self, fields, table, query):
        pass

    def insert(self, data, table):
        pass

    def update(self, data, table, query):
        pass

    def delete(self, table, query):
        pass

    def createDatabase(self):
        pass


a = PostgresConnector()
print("Done")
