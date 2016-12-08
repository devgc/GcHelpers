#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gchelpers.writers.CsvUnicodeWriter import CsvUnicodeWriter

class OutputWriter():
    def __init__(self,delimiter="\t"):
        self.outfile = None
        self.delimiter = delimiter
        self.fh = None
        self.writer = None
    
    def SetOutput(self,output):
        self.outfile = output
        self.fh = open(
            self.outfile,
            'wb',
            0
        )
        
    def InitOutfile(self,columns):
        self.writer = CsvUnicodeWriter(
            self.fh,
            delimiter=self.delimiter,
            fieldnames=columns
        )
        self.writer.writeheader()
        
    def Close(self):
        self.fh.close()
    
    def WriteRecord(self,row):
        self.writer.writerow(
            dict(row)
        )