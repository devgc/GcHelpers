#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlsxwriter
import yaml
import json
import os
import datetime
import logging

class XlsxTemplateManager():
    def __init__(self,template_directory):
        '''Create a XlsxTemplateManager
        args:
            template_directory: path to where xlsx YAML templates reside
        '''
        self.template_directory = template_directory
        
    def CreateReports(self,db_config,output_folder):
        '''Create reports based off of templates'''
        template_files = []
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        #Look in our template folder for yaml files#
        for subdir, dirs, files in os.walk(self.template_directory):
            for filename in files:
                if filename.lower().endswith('.yml') or filename.lower().endswith('.yaml'):
                    template_files.append(
                        os.path.join(subdir,filename)
                    )
        
        for template_filename in template_files:
            template_basename = os.path.basename(template_filename)
            print(u'Processing File {}'.format(template_basename))
            
            # Create our XlsxHandler
            reporter = XlsxHandler(
                template_filename,
                outpath=output_folder
            )
            
            # Write report
            reporter.WriteReport(
                db_config.GetDbHandler()
            )

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
                self.outpath,
                self.properties['workbook_name']
            )
        logging.debug('creating workbook {}'.format(filename))
        
        # Create Workbook
        workbook = xlsxwriter.Workbook(
            filename
        )
        
        # Maintain worksheet boundaries
        WORKSHEET_BOUNDARIES = {}
        
        # Iterate over each spreadsheet
        worksheet_count = 0
        for worksheet_struct in self.properties['worksheets']:
            # Check worksheet name #
            worksheet_name = worksheet_struct.get('worksheet_name',None)
            if not worksheet_name:
                raise(Exception(u"'worksheet_name' required at index {}".format(worksheet_count)))
            
            # Check worksheet name is unique #
            check = WORKSHEET_BOUNDARIES.get(worksheet_struct['worksheet_name'],None)
            if check:
                raise(Exception(u'You cannot have to worksheets named the same: {} at index {}'.format(
                    worksheet_struct['worksheet_name'],
                    worksheet_count
                )))
            WORKSHEET_BOUNDARIES[worksheet_struct['worksheet_name']] = {
                'index': worksheet_count
            }
            
            # Create Worksheet
            worksheet = workbook.add_worksheet(
                worksheet_struct['worksheet_name']
            )
            
            # Check worksheet type #
            worksheet_type = worksheet_struct.get('worksheet_type',None)
            if not worksheet_type:
                raise(Exception(u"'worksheet_name' required at index {}".format(
                    worksheet_count
                )))
            if worksheet_struct['worksheet_type'].lower() == 'records':
                attributes_struct = worksheet_struct.get('attributes',None)
                if not attributes_struct:
                    raise(Exception(u"'attributes' required at index {}".format(
                        worksheet_count
                    )))
                
                # Iterate Records if SQL Query
                check = attributes_struct.get('sql_query',None)
                if check:
                    # Add Column Formats
                    column_formats = {}
                    columnformats_struct = attributes_struct.get('xlsx_column_formats',None)
                    if columnformats_struct:
                        for column_number in columnformats_struct.keys():
                            if 'format' in columnformats_struct[column_number].keys():
                                column_formats[column_number] = workbook.add_format(
                                    columnformats_struct[column_number]['format']
                                )
                                
                    # Write Records
                    column_cnt = 0
                    row_start = 1
                    row_num = row_start
                    header_flag = False
                    record_count = 0
                    WORKSHEET_BOUNDARIES[worksheet_struct['worksheet_name']]['StartColumn'] = 0
                    WORKSHEET_BOUNDARIES[worksheet_struct['worksheet_name']]['StartRow'] = 0
                    for column_names,record in db_handler.FetchRecords(attributes_struct['sql_query']):
                        if not header_flag:
                            column_cnt = len(column_names)
                            worksheet.write_row(0,0,column_names)
                            header_flag = True
                            
                        row = tuple(record)
                        
                        c_cnt = 0
                        for value in row:
                            formatter = None
                            
                            #Check for special treatment for column#
                            if columnformats_struct:
                                if c_cnt in column_formats.keys():
                                    if 'format' in columnformats_struct[c_cnt].keys():
                                        formatter = column_formats[c_cnt]
                                    
                                    if 'column_type' in columnformats_struct[c_cnt].keys():
                                        '''Supported column_type's ['datetime']'''
                                        if columnformats_struct[c_cnt]['column_type'] == 'datetime':
                                            value = datetime.datetime.strptime(
                                                str(value),
                                                columnformats_struct[c_cnt]['strptime']
                                            )
                                
                            worksheet.write(
                                row_num,
                                c_cnt,
                                value,
                                formatter
                            )
                            
                            c_cnt = c_cnt + 1
                        row_num = row_num+1
                    
                    WORKSHEET_BOUNDARIES[worksheet_struct['worksheet_name']]['EndRow'] = row_num
                    WORKSHEET_BOUNDARIES[worksheet_struct['worksheet_name']]['EndColumn'] = column_cnt
                    
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
                            "Query: {}".format(attributes_struct['sql_query']),
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
                        attributes_struct['freeze_panes']['columns'] = attributes_struct['freeze_panes'].get('columns',0)
                        if 'freeze_panes' in worksheet_struct:
                            worksheet.freeze_panes(
                                attributes_struct['freeze_panes']['row'],
                                attributes_struct['freeze_panes']['columns'],
                            )
            elif worksheet_struct['worksheet_type'].lower() == 'chart':
                attributes_struct = worksheet_struct.get('attributes',None)
                if not attributes_struct:
                    raise(Exception(u"'attributes' required at index {}".format(
                        worksheet_count
                    )))
                
                chart_struct = attributes_struct.get('chart',None)
                if not chart_struct:
                    raise(Exception(u"'chart' required for 'atributes' of type {}.".format(
                        worksheet_struct['worksheet_type']
                    )))
                
                # Create chart object
                chart = workbook.add_chart(chart_struct)
                
                sytle_value = attributes_struct.get('style',None)
                if sytle_value:
                    chart.set_style(sytle_value)
                    
                # Set Title
                title_struct = attributes_struct.get('title',None)
                if title_struct:
                    chart.set_title(title_struct)
                
                # Set Legend
                legend_struct = attributes_struct.get('legend',None)
                if legend_struct:
                    chart.set_legend(legend_struct)
                    
                # Set Plot Area
                plotarea_struct = attributes_struct.get('plotarea',None)
                if plotarea_struct:
                    chart.set_plotarea(plotarea_struct)
                
                # Iterate Series Data
                series = attributes_struct.get('series',None)
                if not series:
                    raise(Exception(u"At least one set of 'series' is required. Worksheet {}".format(
                        worksheet_count
                    )))
                for series_struct in series:
                    for key in series_struct.keys():
                        if isinstance(series_struct[key],str) or isinstance(series_struct[key],unicode):
                            series_struct[key] = series_struct[key].format(**WORKSHEET_BOUNDARIES)
                            
                    chart.add_series(series_struct)
                
                # Insert the chart into the worksheet.
                insert_value = attributes_struct.get('insert_cell',None)
                if not insert_value:
                    raise(Exception(u"'insert_cell' required. Worksheet {}".format(
                        worksheet_count
                    )))
                
                size_struct = attributes_struct.get('size',None)
                if size_struct:
                    chart.set_size(size_struct)
                
                worksheet.insert_chart(attributes_struct['insert_cell'], chart)
            else:
                raise(Exception(u"Unhandled worksheet_type of {} at index {}".format(
                    worksheet_struct['worksheet_type'],
                    worksheet_count
                )))
            
            worksheet_count += 1
            
        workbook.close()
        logging.info('finished writing records')
        
def GetAttribute(object,key):
    pass