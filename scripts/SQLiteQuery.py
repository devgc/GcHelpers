#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import logging

try:
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers.OutputWriter import OutputWriter
except:
    sys.path.append('..')
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers.OutputWriter import OutputWriter

def GetArguements():
    '''Get needed options for processing'''
    usage = '''SQLiteQuery'''
    
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
        '-q','--queryfile',
        dest='queryfile',
        required=True,
        action="store",
        type=unicode,
        help=u'SQL File'
    )
    
    arguements.add_argument(
        '-o','--outfile',
        dest='outfile',
        required=True,
        action="store",
        type=unicode,
        help=u'Results File'
    )
    
    return arguements

def Main():
    # Get options #
    arguements = GetArguements()
    options = arguements.parse_args()
    
    # Create writer #
    writer = OutputWriter()
    writer.SetOutput(
        options.outfile
    )
    
    # Load Query #
    query_str = None
    with open(options.queryfile,'rb') as qfh:
        query_str = qfh.read()
        qfh.close()
    
    # Get DB Connection #
    dbconfig = DbConfig(
        db_type='sqlite',
        db=options.database
    )
    dbhandler = dbconfig.GetDbHandler()
    
    cnt = 0
    for record in dbhandler.FetchRecords(query_str):
        if cnt == 0:
            writer.InitOutfile(record[0])
        writer.WriteRecord(dict(record[1]))
        cnt+=1

if __name__ == '__main__':
    Main()