#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import datetime

class StockPool(object):
    def __init__(self, stock_list, start, end):
        pass
    
    
class StockChart(object):
    def __init__(self, stock, start, end):
        self._stock = stock

    def get_stock_info(self):
        return self._stock

    

class StockInfo(object):
    def __init__(self, stock_dict):
        self._code = str(stock_dict['code'])
        self._exch = str(stock_dict['exch'])
        
    def get_stock_code(self):
        return self._code

    def get_stock_exch(self):
        return self._exch



if __name__ == '__main__':

    start = datetime.datetime.strptime('2014-08-17','%Y-%m-%d').date()
    end = datetime.datetime.strptime('2014-09-01','%Y-%m-%d').date()
    #s = StockChart(start,end)
    si = StockInfo({'code':'600882','exch':'ss'})
    sc = StockChart(si,start,end)
    print sc.get_stock_info().get_stock_code()
    

        

    
    