#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import codecs
import cStringIO

class CsvUnicodeWriter:
    """
    A CSV writer which will write rows to a CSV file,
    which is encoded in the given encoding.
    """
    def __init__(self, file_handle, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.encoding = encoding
        self.writer = csv.DictWriter(
            self.queue,
            dialect=dialect,
            **kwds
        )
        self.stream = file_handle
        self.encoder = codecs.getincrementalencoder(encoding)()
        
    def writeheader(self):
        '''Write a header'''
        self.writer.writeheader()

    def writerow(self, row):
        '''Write a row'''
        for column_name in row.keys():
            if isinstance(row[column_name],unicode):
                row[column_name] = row[column_name].encode(
                    self.encoding
                )
                
        self.writer.writerow(row)
        
        data = self.queue.getvalue()
        data = data.decode(
            self.encoding
        )
        
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        
        # write to the target stream
        self.stream.write(data)
        
        # empty queue
        self.queue.truncate(0)