#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
if __name__ == '__main__':
    sys.path.append('../../')
import json
import logging
import sqlite3
from gchelpers.ip.GeoDbManager import GeoDbManager
from gchelpers.dt import DateTimeHandler 

GEO_MANAGER = GeoDbManager()

def splitpath(path, n):
    path_array = re.split('[\\\/]',path)
    start_index = -(n+1)
    
    # Check that path has enough elements
    if abs(start_index) > len(path_array):
        new_path = os.path.join(path_array[0],*path_array[1:])
    else:
        new_path = os.path.join(path_array[start_index],*path_array[start_index+1:])
        
    return new_path

def RegisterSQLiteFunctions(dbh):
    sqlite3.enable_callback_tracebacks(True)
    dbh.create_function("REGEXP", 2, Regexp)
    dbh.create_function('Basename',1,Basename)
    dbh.create_function('BasenameN',2,BasenameN)
    dbh.create_function("GetRegMatch", 3, GetRegMatch)
    dbh.create_function("GetRegMatchArray", 3, GetRegMatchArray)
    dbh.create_function("RemoveNewLines", 1, RemoveNewLines)
    dbh.create_function("DtFormat", 2, DtFormat)
    dbh.create_function("DtFormatTz", 4, DtFormatTz)
    
    if GEO_MANAGER.DB_ATTACHED:
        dbh.create_function("GetIpInfo", 1, GetIpInfo)
    
def DtFormatTz(dtstringin,newformat,current_tz_str,new_tz_str):
    if dtstringin:
        string_out = None
        
        # Get object from in string
        datetime_obj = DateTimeHandler.DatetimeFromString(
            dtstringin
        )
        
        # Timezone Conversion
        new_datetime_obj = DateTimeHandler.ConvertDatetimeTz(
            datetime_obj,
            current_tz_str,
            new_tz_str
        )
        
        # Format object
        string_out = DateTimeHandler.StringFromDatetime(
            new_datetime_obj,
            newformat
        )
        
        return string_out
    
    return None
    
def DtFormat(dtstringin,newformat):
    if dtstringin:
        string_out = None
        
        # Get object from in string
        datetime_obj = DateTimeHandler.DatetimeFromString(
            dtstringin
        )
        
        # Format object
        string_out = DateTimeHandler.StringFromDatetime(
            datetime_obj,
            newformat
        )
        
        return string_out
    
    return None

def Regexp(pattern,input):
    if input is None:
        return False
    
    try:
        if re.search(pattern, input):
            return True
        else:
            return False
    except Exception as error:
        print(u'ERROR: {}'.format(str(error)))
        return False

def Basename(fullname):
    '''Get the base name of a fullname string'''
    value = ''
    if fullname:
        try:
            value = os.path.basename(fullname)
        except:
            value = filename
        
    return value

def BasenameN(fullname,n):
    '''Get the base name of a fullname string'''
    value = ''
    if fullname is None:
        return None
    
    value = splitpath(fullname,n)
    
    return value
    
def GetIpInfo(ip_address):
    if ip_address is None:
        return None
    
    geo = GEO_MANAGER
    info = geo.GetIpInfo(ip_address)
    return json.dumps(info)

def RemoveNewLines(input):
    if input is None:
        return None
    
    input = input.replace("\n", "")
    input = input.replace("\r", "")
    
    return input

def GetRegMatch(input,group,pattern):
    if input is None:
        return None
    
    match = re.search(pattern, input)
    
    result = None
    if match:
        result = match.group(group)
        
    return result

def GetRegMatchArray(input,group,pattern):
    hits = []
    
    if input is None:
        return json.dumps(hits)
    
    for result in re.finditer(pattern, input):
        hits.append(result.group(group))
    
    if len(hits) > 0:
        return json.dumps(hits)
    
    return json.dumps(hits)
    
def test1():
    n = 2
    fullname = "Partition 1\\TEST_P1 [NTFS]\\[root]\\testfolder002\\testfolder001\\testfile088.png"
    splitname = splitpath(fullname,n)
    
    print splitname
    
def test2():
    n = 2
    fullname = "testfolder001\\testfile088.png"
    splitname = splitpath(fullname,n)
    
    print splitname
    
if __name__ == '__main__':
    test1()
    test2()