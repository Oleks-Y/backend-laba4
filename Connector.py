from abc import abstractmethod, ABCMeta

class Connector(metaclass =ABCMeta): 
    def __init__(self):
        pass
        # todo here need to create database 
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
    @abstractmethod
    def exportTo(self, connector):
        pass
    @abstractmethod 
    def importData(self, data):
        pass
# class MySqlConnector(Connector): 


