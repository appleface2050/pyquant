# -*- coding: utf-8 -*-
'''
    strategy name:tf_lt_0001
    create time:2014-09-18 
    period type:long
    period:
    strategy description:
                当120日均线突破240日均线  long
                当240日均线突破120日均线 short
                进场后30天内不平仓
                损失超过20%时进场使得损失变为10%

'''
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.stock_data import StockData

class TFLT0001(object):
    def running(self):
        pass
        

if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = datetime.date.today() - datetime.timedelta(days=1)
    start = '2010-01-01'
    end = ''
    if not start:
        start = datetime.datetime.strptime('2010-01-01','%Y-%m-%d').date()
    else:
        start = datetime.datetime.strptime(start,'%Y-%m-%d').date()
    if not end:
        end = yest
    else:
        end = datetime.datetime.strptime(end,'%Y-%m-%d').date()
    
    s = TFLT0001(start,end)
    s.running()
    print 'testing...',start,'-->',end 
    print 'time used:  ',datetime.datetime.now()-now








