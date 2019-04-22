import psycopg2
import psycopg2.extras
from instance.config import configs
from app.v1.sql import table_create_sql, drop_tables2

class SetUpDb:
    """ Class tha create all the tables for the app"""


    def __init__(self, config_name='development'):
        """ create connection to the database using config setting
        Argument
        config_name[{String}]
         """
        connection_string = configs[config_name].CONNECTION_STRING
        self.connection= psycopg2.connect(connection_string)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def get_connection(self):
        """ returns the databse connnection """
        return self.connection


    def create_tables(self):
        """ create tables in the database """
        for query in table_create_sql:
                self.cursor.execute(query)
        
        self.commit()

    def commit(self):
        """Does the commit action to the db """
        self.connection.commit()

    def commit_and_close(self):
        """ commit changes and close databse connnections"""
        self.connection.commit()
        self.cursor.close()
    
