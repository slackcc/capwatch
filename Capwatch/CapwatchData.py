import sqlite3
from CapwatchConfig import CapwatchConfig

class CapwatchData(object):

    def __init__(self):
    
        self.config = CapwatchConfig()
        self.db = self.__create_connection__()


    def __create_connection__(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.config.db_file)
        except sqlite3.Error as e:
            print(e)
    
        return conn
