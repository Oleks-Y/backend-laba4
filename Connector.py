from abc import abstractmethod, ABCMeta

class Connector(metaclass =ABCMeta): 
    def __init__(self):
        pass
        # todo here need to create database 
    @abstractmethod 
    def select(self, fields, table, query):
        pass 
    @abstractmethod 
    def insert(self, data, table):
        pass 
    @abstractmethod
    def update(self, data, table, query):
        pass 
    @abstractmethod 
    def delete(self, table, query):
        pass 
    @abstractmethod 
    def createDatabase(self): 
        pass
    @abstractmethod 
    def getCursor(self):
        pass
    @abstractmethod 
    def dropAllTables(self):
        pass
    @abstractmethod 
    def execute(self):
        pass
# class MySqlConnector(Connector): 


