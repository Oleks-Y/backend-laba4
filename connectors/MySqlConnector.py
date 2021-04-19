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
        dbConf = config["Postgres"]
        self.conn = pymysql.connect(user='blyat',
                                    password='12345678',
                                    host='0.0.0.0',
                                    db='univercity',
                                    port=3307,
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
        pass


a = MySqlConnector()
print("Done")
