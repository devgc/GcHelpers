#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import logging
try:
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers import XlsxHandler
except:
    sys.path.append('..')
    from gchelpers.db.DbHandler import DbConfig
    from gchelpers.writers import XlsxHandler

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
        '-t','--templatefile',
        dest='templatefile',
        default=None,
        action="store",
        type=unicode,
        help=u'Template File'
    )
    arguements.add_argument(
        '-f','--templatefolder',
        dest='templatefolder',
        default=None,
        action="store",
        type=unicode,
        help=u'Folder of Template Files'
    )
    
    arguements.add_argument(
        '--outfile',
        dest='outfile',
        default=None,
        action="store",
        type=unicode,
        help=u'XLSX Output File'
    )
    arguements.add_argument(
        '--outfolder',
        dest='outfolder',
        default=None,
        action="store",
        type=unicode,
        help=u'XLSX Output Folder'
    )
    
    return arguements

def CreateReports(options):
    if not options.templatefile and not options.templatefolder:
        raise(Exception(u'options.templatefile or options.templatefolder is needed.'))
    
    if not options.outfile and not options.outfolder:
        raise(Exception(u"options.outfile or options.outfolder is needed.\n"+
                        u"options.outfile if using options.templatefile.\n"+
                        u"options.outfolder if using options.templatefolder."
        ))
    
    if options.templatefile and not options.outfile:
        raise(Exception(u'options.outfile must be used with options.templatefile'))
    
    if options.templatefolder and not options.outfolder:
        raise(Exception(u'options.outfolder must be used with options.templatefolder'))
    
    db_config = DbConfig(
        db_type='sqlite',
        db=options.database
    )
    
    db_handler = db_config.GetDbHandler()
    
    if options.templatefile:
        xlsx_handler = XlsxHandler.XlsxHandler(
            options.templatefile,
            outfile=options.outfile
        )
        
        xlsx_handler.WriteReport(
            db_handler
        )
    elif options.templatefolder:
        temp_manager = XlsxHandler.XlsxTemplateManager(
            options.templatefolder
        )
        temp_manager.CreateReports(
            db_config,
            options.outfolder
        )
    else:
        raise(Exception(u'Unhandled options'))

if __name__ == '__main__':
    arguements = GetArguements()
    options = arguements.parse_args()
    
    # Create Reports
    CreateReports(options)