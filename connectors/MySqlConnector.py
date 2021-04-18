import mysql 
from Connector import Connector

class MySqlConnector(Connector): 
    def __init__(self, conn): 
        super().__init__(conn)
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
