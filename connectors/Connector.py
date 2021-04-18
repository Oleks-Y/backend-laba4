from abc import abstractmethod, ABCMeta

class Connector(metaclass =ABCMeta): 
    def __init__(self, conn):
        self.conn = conn 
        # todo here need to create database 
    # todo а тут блять йопта весь крад 
    @abstractmethod 
    def _select(self, fields, table, query):
        pass 
    @abstractmethod 
    def _insert(self, data, table):
        pass 
    @abstractmethod
    def _update(self, data, table, query):
        pass 
    @abstractmethod 
    def _delete(self, table, query):
        pass 
# class MySqlConnector(Connector): 


