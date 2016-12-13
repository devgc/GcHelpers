#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import logging
try:
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers.XlsxHandler import XlsxHandler
except:
    sys.path.append('..')
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers.XlsxHandler import XlsxHandler

def GetArguements():
    '''Get needed options for processing'''
    usage = '''SQLiteToXlsx.py'''
    
    arguements = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(usage)
    )
    
    arguements.add_argument(
        '-d','--database',
        dest='database',
        required=True,
        action="store",
        type=unicode,
        help=u'Database to query'
    )
    
    arguements.add_argument(
        '-t','--template',
        dest='template',
        required=True,
        action="store",
        type=unicode,
        help=u'Template File'
    )
    
    arguements.add_argument(
        '-o','--outfile',
        dest='outfile',
        required=True,
        action="store",
        type=unicode,
        help=u'XLSX Output File'
    )
    
    return arguements

def Main():
    arguements = GetArguements()
    options = arguements.parse_args()
    
    db_config = DbConfig(
        db_type='sqlite',
        db=options.database
    )
    
    db_handler = db_config.GetDbHandler()
    
    xlsx_handler = XlsxHandler(
        options.template,
        outfile=options.outfile
    )
    
    xlsx_handler.WriteReport(
        db_handler
    )

if __name__ == '__main__':
    Main()