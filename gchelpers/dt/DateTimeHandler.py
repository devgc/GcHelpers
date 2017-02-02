#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pytz
import dateutil.parser

def DatetimeFromString(datetime_string):
    '''
    args:
        datetime_string: A string version of date and time
    return:
        datetime_obj: A datetime object representing the input string
    '''
    datetime_obj = None
    datetime_obj = dateutil.parser.parse(datetime_string)
    
    return datetime_obj

def ConvertDatetimeTz(datetime_obj,current_tz_str,new_tz_str):
    '''
    args:
        datetime_obj: A string version of date and time
        current_tz: The current timezone of datetime_obj
        new_tz: The timezone to convert to
    return:
        new_datetime_obj: A datetime object representing the input string
    '''
    new_datetime_obj = None
    
    # Set current Timezone #
    current_tz = pytz.timezone(current_tz_str)
    datetime_obj.replace(tzinfo=current_tz)
    
    # Convert to new timezone #
    new_tz = pytz.timezone(new_tz_str)
    new_datetime_obj = datetime_obj.astimezone(new_tz)
    
    return new_datetime_obj

def StringFromDatetime(datetime_obj,out_format):
    '''
    args:
        datetime_obj: a datetime object
        out_format: the output format desired
    return:
        datetime_string: representing our datetime object
    '''
    datetime_string = None
    datetime_string = out_format.format(datetime_obj)
    
    return datetime_string

def test01():
    test_string = '2015-Nov-09 21:53:26.265074 UTC'
    datetime_obj = DatetimeFromString(test_string)
    
    new_dt = ConvertDatetimeTz(
        datetime_obj,
        'UTC',
        'US/Central'
    )
    
    print datetime_obj
    print new_dt

def test02():
    test_string = '2017-Jan-11 15:16:27.467916 UTC'
    
# If this is ran as a script and not imported as a library
if __name__ == '__main__':
    test01()
    