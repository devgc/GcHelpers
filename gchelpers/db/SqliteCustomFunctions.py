#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import json
import logging
from gchelpers.ip.GeoDbManager import GeoDbManager

GEO_MANAGER = GeoDbManager()

def splitpath(fullpath):
    allparts = []
    while 1:
        parts = os.path.split(fullpath)
        if parts[0] == fullpath:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == fullpath: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            fullpath = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def RegisterSQLiteFunctions(dbh):
    dbh.create_function("REGEXP", 2, Regexp)
    dbh.create_function('Basename',1,Basename)
    dbh.create_function('BasenameN',2,BasenameN)
    dbh.create_function("GetRegMatch", 3, GetRegMatch)
    dbh.create_function("GetRegMatchArray", 3, GetRegMatchArray)
    dbh.create_function("RemoveNewLines", 1, RemoveNewLines)
    
    if GEO_MANAGER.DB_ATTACHED:
        dbh.create_function("GetIpInfo", 1, GetIpInfo)

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
    if fullname:
        spitname = splitpath(fullname)
        if spitname[0] == '':
            spitname.pop(0)
            
        if len(spitname) < n:
            value = os.path.join(
                *spitname
            )
        else:
            value = os.path.join(
                *spitname[-(n):]
            )
            
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