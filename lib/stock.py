#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.stock_data import StockData

class StockPool(object):
    '''
    {StockInfo:StockChart}
    '''
    def __init__(self, stock_list, start, end):
        print "----------Initializing Stock Pool--------------"
        self._stock_pool = {}
        self._start = start
        self._end = end
        for stock in stock_list:
            self._stock_pool[stock] = StockChart(stock,start,end)
        
        print "-----------------------"
        print "Stock Pool Infomation"
        print "start: ",start
        print "end:   ",end
        print "stock number:",len(stock_list)
        print "chart days number:",end-self.get_min_date().date()
        print "-----------------------"
        
    def get_stock_pool_start(self):
        return self._start
    
    def get_stock_pool_end(self):
        return self._end    
    
    def get_min_date(self):
        desc = self.stock_pool_desc()
        min_date = ''
        for stock in desc:
            #print stock
            for chart in stock['chart']:
                if not min_date:
                    min_date = chart['DATE']
                elif min_date > chart['DATE']:
                    min_date = chart['DATE']
                else:
                    continue
        return min_date
        
    def get_stock_pool(self):
        return self._stock_pool

    def print_stock_pool(self):
        for i in self._stock_pool:
            print i.get_stockinfo_code(),i.get_stockinfo_exch()
    
    def stock_pool_ind_computing_format(self):
        '''
        [
        {'code':code,
         'exch':exch,
         'chart':{'DATE1':{'High':NUM,'Volume':NUM,'AdjClose'NUM,'Low':NUM,'CLOSE':NUM,'OPEN':NUM},'DATE2':[data],'DATE3':[data]...}
        },{...}
        ]
        '''
        res = []
        stock = {}
        s_chart = []
        for i in self._stock_pool:
            s_code = i.get_stockinfo_code()
            s_exch = i.get_stockinfo_exch()
            s_chart = self._stock_pool[i].get_stock_chart()
            chart = {}
            for day_c in s_chart:
                tmp_day = day_c['DATE'].date()
                #chart[day_c['DATE']] = day_c
                day_c.pop('DATE')
                day_c.pop('CODE')
                day_c.pop('exchange')
                chart[tmp_day] = day_c
            #print chart            
            stock = {'code':s_code,
                     'exch':s_exch,
                     'chart':chart}
            res.append(stock)

            #print stock['chart'].keys()
        return res 
    
    def stock_pool_desc(self):
        res = []
        stock = {}
        for i in self._stock_pool:
            #s_info = {"code":i.get_stockinfo_code(),"exch":i.get_stockinfo_exch()}
            s_code = i.get_stockinfo_code()
            s_exch = i.get_stockinfo_exch()
            s_chart = self._stock_pool[i].get_stock_chart()
            stock = {'code':s_code,
                     'exch':s_exch,
                     'chart':s_chart}
            res.append(stock)
        return res
    
    def get_first_stock_info(self):
        if self._stock_pool:
            return self._stock_pool[0]
        else:
            return None
        
    def get_stock_pool_stock_num(self):
        return len(self._stock_pool)    
    
    def get_stock_pool_day_num(self, stock_info):
        if not stock_info:
            return None
        else:
            return self._stock_pool[stock_info].get_stock_chart_len()
    
class StockChart(object):
    '''
    _stock_data
    {'stock_info':{},
    'stock_chart':[]}
    '''
    def __init__(self, stock, start, end):
        self._stock = stock
        self._stock_data = {'stock_info':self._stock}
        q = StockData.mgr().get_stock_data_from_db(self._stock_data['stock_info'].get_stockinfo_code(),self._stock_data['stock_info'].get_stockinfo_exch(),start,end)[:]
        self._stock_data['stock_chart'] = q

    def get_stock_info(self):
        return self._stock

    def get_stock_chart(self):
        return self._stock_data['stock_chart']
    
    def get_stock_data(self):
        return self._stock_data

    def get_stock_chart_len(self):
        return len(self.get_stock_chart())

class StockInfo(object):
    def __init__(self, stock_dict):
        self._code = str(stock_dict['code'])
        self._exch = str(stock_dict['exch'])
        
    def get_stockinfo_code(self):
        return self._code

    def get_stockinfo_exch(self):
        return self._exch



if __name__ == '__main__':

    start = datetime.datetime.strptime('2014-08-17','%Y-%m-%d').date()
    end = datetime.datetime.strptime('2014-09-01','%Y-%m-%d').date()
    #s = StockChart(start,end)
    si = StockInfo({'code':'600882','exch':'ss'})
    si2 = StockInfo({'code':'900920','exch':'ss'})
    #sc = StockChart(si,start,end)
    #print si.get_stockinfo_code()
    #print []
    sp = StockPool([si,si2],start,end).stock_pool_desc()
    #for s in sp:
    #    print s
    #print sp.get_stock_pool_day_num(si)
    spif = StockPool([si,si2],start,end).stock_pool_ind_computing_format()
    for i in spif:
        print i
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        

    
    