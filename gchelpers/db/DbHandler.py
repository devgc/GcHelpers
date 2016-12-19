#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from gchelpers.db import SqliteCustomFunctions

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class UnhandledDbTypeError(Exception):
    def __init__(self, message, errors):
        super(UnhandledDbTypeError, self).__init__(message)

class DbConfig():
    def __init__(self,**kwargs):
        '''Create a DbConfig object
        kwargs:
            db_type: The type of database (Currently supported: 'sqlite')
            db: The name or location of the database
        '''
        self.db_type = kwargs.get('db_type',None)
        if self.db_type is not None:
            pass
        else:
            raise(
                Exception(u'db_type is required as an argument for DbConfig. Supported types are: {}'.format(
                    [u'sqlite']
                ))
            )
        
        self.db = kwargs.get('db',None)
        if self.db_type == 'sqlite':
            if self.db is None:
                raise(
                    Exception(u'db is required as an argument for DbConfig with type sqlite.')
                )
        
    def GetDbHandler(self):
        '''Get the DbHandler for this configuration.
        
        returns:
            db_handler: DbHandler object
        '''
        db_handler = DbHandler(
            self
        )
        
        return db_handler
    
class DbHandler():
    '''Helpful Database Functions'''
    def __init__(self,db_config):
        '''Create DbHandler Object
        args:
            db_config: A DbConfig object
        '''
        self.db_config = db_config
        
    def GetDbHandle(self):
        '''Create database handle based off of the DbConfig
        
        returns:
            dbh: A database handle
        '''
        dbh = None
        
        if self.db_config.db_type == 'sqlite':
            dbh = sqlite3.connect(
                self.db_config.db,
                #isolation_level=None,
                timeout=10000
            )
        else:
            raise UnhandledDbTypeError('Unhandled Database Type {}'.format(
                self.db_config['db_type']
            ))
        
        return dbh
        
    def FetchRecords(self,sql_string,row_factory=None):
        '''Generator for return fields from sql_string
        
        Args:
            sql_string: SQL statement to execute
            row_factory: How to handle rows.
                -MySQL: MySQLdb.cursors.DictCursor
        
        Yields:
            list of column names,
            row
        '''
        dbh = self.GetDbHandle()
        
        if self.db_config.db_type == 'sqlite':
            SqliteCustomFunctions.RegisterSQLiteFunctions(dbh)
        
        column_names = []
        
        if self.db_config.db_type == 'sqlite':
            # Register custom functions #
            
            if row_factory == type(dict):
                dbh.row_factory = dict_factory
            else:
                dbh.row_factory = sqlite3.Row
            
            sql_c = dbh.cursor()
        else:
            raise UnhandledDbTypeError('Unhandled Database Type {}'.format(
                self.db_config['db_type']
            ))
        
        sql_c.execute(sql_string)
        
        for desc in sql_c.description:
            column_names.append(
                desc[0]
            )
        
        for record in sql_c:
            yield column_names,record
        
    def CreateTableFromMapping(self,table_name,table_template,primary_key_str):
        '''Create a table based on OrderedDict table template
        
        args:
            table_name: the name of the table to create
            table_template: OrderedDict of the table schema
            primary_key_str: Primary key string for create query
        '''
        dbh = self.GetDbHandle()
        
        sql_string = "CREATE TABLE IF NOT EXISTS {0:s} (\n".format(tbl_name)
        # build column statement based off of template
        for f_name,f_type in table_template.items():
            sql_string += "\"{0:s}\" {1:s},\n".format(f_name,f_type)
        
        if primary_key_str is not None:
            sql_string = sql_string + primary_key_str
        else:
            sql_string = sql_string[0:-2]
        
        sql_string = sql_string + ')'
        
        cursor = dbh.cursor()
        
        cursor.execute(sql_string)