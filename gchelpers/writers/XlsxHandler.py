#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlsxwriter
import yaml
import os
import datetime
import logging

class XlsxHandler():
    def __init__(self,yaml_template,outpath=None,outfile=None):
        '''Create XlsxHandler from template'''
        if not outpath and not outfile:
            raise(Exception(u"XlsxHandler needs 'outpath' or 'outfile' arguement."))
        
        self.outpath = outpath
        self.outfile = outfile
        self.yaml_template = yaml_template
        
        with open(self.yaml_template,'r') as fh:
            data = fh.read()
            fh.close()
        
        self.properties = yaml.load(
            data
        )
        
    def WriteReport(self,db_handler):
        '''Write report to xlsx.'''
        # Open XLSX File
        if self.outfile:
            filename = self.outfile
        else:
            filename = os.path.join(
                outpath,
                self.properties['workbook_name']
            )
        logging.debug('creating workbook {}'.format(filename))
        
        # Create Workbook
        workbook = xlsxwriter.Workbook(
            filename
        )
        
        # Add Column Formats
        column_formats = {}
        if self.properties['xlsx_column_formats']:
            for column_number in self.properties['xlsx_column_formats'].keys():
                if 'format' in self.properties['xlsx_column_formats'][column_number].keys():
                    column_formats[column_number] = workbook.add_format(
                        self.properties['xlsx_column_formats'][column_number]['format']
                    )
        
        # Create Worksheet
        worksheet = workbook.add_worksheet(
            self.properties['worksheet_name']
        )
        
        # Iterate Records
        column_cnt = 0
        row_start = 1
        row_num = row_start
        header_flag = False
        
        for column_names,record in db_handler.FetchRecords(self.properties['sql_query']):
            if not header_flag:
                column_cnt = len(column_names)
                worksheet.write_row(0,0,column_names)
                header_flag = True
                
            row = tuple(record)
            
            c_cnt = 0
            for value in row:
                formatter = None
                
                #Check for special treatment for column#
                if c_cnt in column_formats.keys():
                    if 'format' in self.properties['xlsx_column_formats'][c_cnt].keys():
                        formatter = column_formats[c_cnt]
                    
                    if 'column_type' in self.properties['xlsx_column_formats'][c_cnt].keys():
                        '''Supported column_type's ['datetime']'''
                        if self.properties['xlsx_column_formats'][c_cnt]['column_type'] == 'datetime':
                            value = datetime.datetime.strptime(
                                str(value),
                                self.properties['xlsx_column_formats'][c_cnt]['strptime']
                            )
                    
                worksheet.write(
                    row_num,
                    c_cnt,
                    value,
                    formatter
                )
                
                c_cnt = c_cnt + 1
            row_num = row_num+1
        
        if header_flag == False:
            worksheet.write(
                0,
                0,
                'No records returned for query',
                None
            )
            worksheet.write(
                1,
                0,
                "Query: {}".format(self.properties['sql_query']),
                None
            )
        else:
            worksheet.autofilter(
                0,
                0,
                row_num - 1,
                column_cnt - 1
            )
        
            #Freeze Panes#
            self.properties['freeze_panes']['columns'] = self.properties['freeze_panes'].get('columns',0)
            if 'freeze_panes' in self.properties:
                worksheet.freeze_panes(
                    self.properties['freeze_panes']['row'],
                    self.properties['freeze_panes']['columns'],
                )
        
        workbook.close()
        logging.info('finished writing records')