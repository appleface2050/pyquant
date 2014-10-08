#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import time
import datetime
import StringIO
import gzip

def strptime(dtime, format):
    """
    for < 2.6
    """
    time_stamp = time.mktime(time.strptime(dtime,format))
    return datetime.datetime.fromtimestamp(time_stamp)

def time_start(d, typ):
    """
    """
    if typ == "hour":
        d -= datetime.timedelta(minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "day":
        d -= datetime.timedelta(hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "week":
        d -= datetime.timedelta(days=d.weekday(),hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "month":
        d -= datetime.timedelta(days=d.day-1,hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    else:
        raise Exception("wrong type %s" % (typ,))
    return d

def time_next(d, typ):
    if typ == "hour":
        d += datetime.timedelta(hours=1)
    elif typ == "day":
        d += datetime.timedelta(days=1)
    elif typ == "week":
        d += datetime.timedelta(days=7)
    elif typ == "month":
        year = d.year+1 if d.month==12 else d.year
        month = 1 if d.month==12 else d.month+1
        d = datetime.datetime(year,month,1)
    else:
        raise Exception("wrong type %s" % (typ,))
    return time_start(d,typ)
    
def strftime_day(dtime):
    """
    for simplariy
    """
    return str(time_start(dtime,"day"))

def gzip_compress(data):
    zbuf = StringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb',compresslevel=9,fileobj=zbuf)
    zfile.write(data)
    zfile.close()
    return zbuf.getvalue()

def gzip_decompress(data):
    zbuf = StringIO.StringIO(data)
    zfile = gzip.GzipFile(fileobj=zbuf)
    data = zfile.read()
    zfile.close()
    return data

def average(data_list):
    su = 0.0
    for data in data_list:
        su += data
    return su/len(data_list)
    
def std(data_list):
    '''
    Standard deviation
    '''
    tmp = 0.0
    avg = average(data_list)
    for data in data_list:
        tmp += (data - avg)**2
    return float("%.4f"%((tmp/(len(data_list)-1))**0.5))
    
def find_max_date(day_list):
    if not day_list:
        return False
    max_d = ""
    for i in day_list:
        if not max_d:
            max_d = i 
        elif max_d < i:
            max_d = i
        else:
            continue
    return max_d

def partition(array,low,high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        while low < high and array[high] < key:
            array[low] = array[high]
            low += 1
            array[high] = array[low]
    array[low] = key
    return low


def quick_sort(array,low,high):
    if low < high:
        key_index = partition(array,low,high)
        quick_sort(array,low,key_index)
        quick_sort(array,key_index+1,high)


if __name__ == '__main__':
    a = datetime.date(2007, 8, 21)
    b = datetime.date(2008, 3, 10)
    c = datetime.date(2009, 12, 25)
    
    array = [a,c,b]
    print array
    quick_sort(array,0,len(array)-1)
    print array
    
    
    
