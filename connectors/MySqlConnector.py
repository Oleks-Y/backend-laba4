import mysql 
from Connector import Connector

class MySqlConnector(Connector): 
    def __init__(self, conn): 
        super().__init__(conn)
    def _select(self, fields, table, query):
        pass 
    def _insert(self, data, table):
        pass 
    def _update(self, data, table, query):
        pass 
    def _delete(self, table, query):
        pass 
