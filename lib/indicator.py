#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import datetime
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.stock_data import StockData
from lib.stock  import StockPool,StockChart,StockInfo
from conf.settings import TECH_ANALY_IND

class Indicator(object):
    '''
    technical analysis indicators
    '''
    def __init__(self, stock_pool, start, ind_list):
        self._ind_format_data = []
        self._useful_ind_format_data = []
        if stock_pool and start and ind_list:
            self._stock_pool = stock_pool
            self._ind_list = ind_list   
            self._start = start      #indicator count start time
            #self._ind_format_data = self._stock_pool.stock_pool_ind_computing_format()
            if(self.prepare_computing()):
                self.start_computing()
                
        else:
            print "technical analysis indicators init ERROR"
            return False
    
    def get_ind_count_start(self):
        return self._start
    
    def get_ind_count_end(self):
        return self._stock_pool.get_stock_pool_end()
    
    def start_computing(self):
        print "......start calculate indicators......"
        
        # calculate Moving Average
        ma_ind = self.fetch_ma()
        if ma_ind:
            self.ma_ind_computing(ma_ind)
        
        # calculate MACD
        if 'MACD' in self._ind_list:
            self.macd_ind_computing()
            
        if 'KDJ' in self._ind_list:
            self.kdj_ind_computing()
        
        self.generate_useful_ind_format_data()
        
        print "......calculating indicators done......"
    
    def generate_useful_ind_format_data(self):
        self._useful_ind_format_data = []
        #for stock in self._ind_format_data:    #stock
        #    for dat in stock['chart']:         #chart
        #        for ind in self._ind_list:     #MA120 MA240
        #            print ind
                    #if dat[ind] in dat.keys():    
                    #    print dat[ind]
        start = self.get_ind_count_start()
        end = self.get_ind_count_end()
        if start and end:
            for stock in self._ind_format_data:    #stock
                use_stock = {}
                use_stock['code'] = stock['code']
                use_stock['exch'] = stock['exch']
                
                use_stock_chart = {}
                for dat in stock['chart']:         #chart
                    if dat>=start and dat<=end:
                        use_stock_chart[dat] = stock['chart'][dat]
                    #print use_stock_chart
                use_stock['chart'] = use_stock_chart
                self._useful_ind_format_data.append(use_stock)
    
        #print self._useful_ind_format_data
        #print self._ind_format_data
    
    def kdj_ind_computing(self):
        print "kdj ind not ready yet"
        
    def macd_ind_computing(self):
        print "macd ind not ready yet"
    
    def find_ma_day_type(self, ma):
        m = re.match(r'^(MA)(\d+)', ma)
        if m:
            return m.group(2)
        else:
            return False
    
    def bubblesort_desc(self, ob_list):
        for j in range(len(ob_list)-1,-1,-1):
            for i in range(j):
                if ob_list[i] < ob_list[i+1]:
                    ob_list[i],ob_list[i+1] = ob_list[i+1],ob_list[i]
        return ob_list

    def bubblesort_asc(self, ob_list):
        for j in range(len(ob_list)-1,-1,-1):
            for i in range(j):
                if ob_list[i] > ob_list[i+1]:
                    ob_list[i],ob_list[i+1] = ob_list[i+1],ob_list[i]
        return ob_list
        
    def ma_ind_computing(self, ma_ind):
        """
        [
        {'code':code,
         'exch':exch,
         'chart':{'DATE1':{'High':NUM,'Volume':NUM,'AdjClose'NUM,'Low':NUM,'CLOSE':NUM,'OPEN':NUM},'DATE2':[data],'DATE3':[data]...}
        },{...}
        ]
        """
        #ind_format_data = self._stock_pool.stock_pool_ind_computing_format()
        #print ind_format_data
        day_index = self._ind_format_data[0]['chart'].keys()
        #day_index = ind_format_data[0]['chart'].keys()
        day_index = self.bubblesort_asc(day_index)
        #print day_index
        
        #print len(ind_format_data[0]['chart'].keys()) #日期数量
        
        for ma_type in ma_ind:
            print "...calculating",ma_type
            ma_day_type = self.find_ma_day_type(ma_type)
            if not ma_day_type:
                print "MA day type wrong"
                return False
            
            for stock in self._ind_format_data:
            #for stock in ind_format_data:
                #print stock
                #print stock['code'],stock['exch'],stock['chart'][0],stock['chart'][1],stock['chart'][2]
                #print stock['code']
                count_day_list = self.prepare_count_day_list(stock,self._start)
                date_index = self.bubblesort_asc(stock['chart'].keys())
                #print len(date_index)
                #print count_day_list
                for date in count_day_list:
                    #print date
                    ma = self.counting_averae(stock['chart'],date,date_index,ma_day_type)
                    stock['chart'][date][ma_type] = ma
                    
        #print self._ind_format_data[0]['chart']
        
    def counting_averae(self, stock_data, date, date_index, ma_day_type):
        '''
        stock_data:
        {'DATE1':{'High':NUM,'Volume':NUM,'AdjClose'NUM,'Low':NUM,'CLOSE':NUM,'OPEN':NUM},'DATE2':[data],'DATE3':[data]...}
        '''
        if date < date_index[0]:
            return False
        else:
            #print date
            #print ma_day_type
            #print stock_data
            '''
                                                    平均值开始计算的日期     
                                                    平均值计算结束日期，即当天
            '''
            if date_index.index(date) < (int(ma_day_type)-1):
                print "ERROR, not enough stock pool data to cal indicator",date
                return False
            
            d_start = date_index[date_index.index(date) - (int(ma_day_type)-1)]           #平均值开始计算的日期
            d_end = date                                                                  #平均值计算结束日期，即当天
            #print date_index.index(d_start),date_index.index(d_end)
            cal_day_list = self.prepare_cal_day_list(d_start, d_end, date_index)
            
            if len(cal_day_list) != int(ma_day_type):
                print "ERROR the number of cal days and MA type doesn't match"
                return False
            else:
                sum_close = 0.0
                for day in cal_day_list:
                    #print day
                    #print  stock_data[day]
                    sum_close += float(stock_data[day]['CLOSE'])
                #print sum_close
                return "%0.02f"%float(sum_close/int(ma_day_type))
       
    def prepare_cal_day_list(self, start, end, date_index):
        res = []
        if start > end:
            print "ERROR,MAYBE THE STOCK POOL START TIME NOT EARLY ENOUPH"
            return False
        else:
            for i in date_index:
                if i >= start and i<= end:
                    res.append(i)
        return res  
    
    def prepare_count_day_list(self, stock, start):
        #date_list = stock['chart'].keys()
        #date_list = self.delete_useless_date(date_list,start)
        #date_list = self.bubblesort_asc(date_list)
        #return date_list
        return self.bubblesort_asc(self.delete_useless_date(stock['chart'].keys(),start))
        
    def delete_useless_date(self,date_list,start):
        res = []
        for date in date_list:
            if date < start:
                continue
            else:
                res.append(date)
        return res
    
    def fetch_ma(self):
        ma_ind = []
        for i in self._ind_list:
            #if 'MA' in i and i.startswith:
            m = re.search(r'MA\d+', i)
            if m:
                ma_ind.append(i)
        return ma_ind
    
    def prepare_computing(self):
        if not self.check_indicator():
            print "indicator wrong, please check indicator list again"
            return False
        if not self.check_start_time():
            print "start time wrong, please check start time again"
            return False
        print "......data checking done......"
        self._ind_format_data = self._stock_pool.stock_pool_ind_computing_format()
        print "......indicator calculate data form prepare done......"
        return True
        
    def check_indicator(self):
        if not self._ind_list:
            return False
        for ind in self._ind_list:
            assert ind in TECH_ANALY_IND
        return True
    
    def check_start_time(self):
        if not self._start:
            return False
        else:
            min_date = self._stock_pool.get_min_date().date()
            if min_date > self._start:
                print "min date:",min_date
                print "start:   ",self._start
                return False
            else:
                return True

if __name__ == '__main__':
    now = datetime.datetime.now()
    start = datetime.datetime.strptime('2014-08-22','%Y-%m-%d').date()
    end = datetime.datetime.strptime('2014-09-22','%Y-%m-%d').date()
    start_ind_counting_date = datetime.datetime.strptime('2014-09-01','%Y-%m-%d').date()
    si = StockInfo({'code':'002653','exch':'sz'})
    si2 = StockInfo({'code':'002654','exch':'sz'})
    sp = StockPool([si,si2],start,end)
    #print sp.stock_pool_desc()
    ind = Indicator(sp,start_ind_counting_date,['MA5'])
    #print ind._ind_format_data[0]['chart']
    print ind._useful_ind_format_data
    print datetime.datetime.now()-now
    
    
    
    
    
    
    
    