#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import datetime
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.indicator import Indicator
from conf.settings import TECH_ANALY_IND,DIRECTION_LIST,TRADE_PRICE_ORDER_LIST
from model.stock_data import StockData

class Position(object):
    '''
    Class Position use to record every deal infomation ,
    include: deal_time, stock, direction, quantity, 
    '''
    
    def __init__(self):
        self._trade_list = []
        self._position_table = {}
        '''
        _position_table 
        {'stock1':{'direction':,'avg_price':,'quantity':,'net':},
         'stock2':{'direction':,'avg_price':,'quantity':,'net':},
         ......
        }
        '''

    def add(self, trade):
        if trade:
            trade = self.prepare_trade(trade)
            if trade:
                self._trade_list.append(trade)
                self.trade_exec(trade)
                return True
        else:
            return False
    
    def prepare_trade(self, trade):
        if trade.get_price() in TRADE_PRICE_ORDER_LIST:
            trade = self.merge_trade(trade)  #trade may = False       
        return trade
        
    def merge_trade(self, trade):
        m = re.match(r'^(\w+):(\w+)', trade.get_price())
        if m:
            date_order = m.group(1)
            p_order = m.group(2)
            #return m.group(2)
            if date_order == 'today':
                start = trade.get_deal_time()
                #print StockData.mgr().get_one_day_price(start,trade.get_stock_code(),trade.get_stock_exch(),p_order)
                #print start,trade.get_stock_code(),trade.get_stock_exch(),p_order
                try:
                    price = StockData.mgr().get_one_day_price(start,trade.get_stock_code(),trade.get_stock_exch(),p_order)[0]['Close']
                    trade.set_price(price)
                    return trade
                except Exception, e:
                    print e
                    print "may be this day mysql don't have data",start,trade.get_stock_code(),trade.get_stock_exch(),p_order
                    return False
                
            else:
                print "error, date_order not defined"
        else:
            return False
    
    def init_stock_in_position_table(self, trade):
        stock_position_info = {}
        stock_position_info['code'] = trade.get_stock().get_stockinfo_code()         #just for debug 
        stock_position_info['direction'] = trade.get_direction()
        stock_position_info['avg_price'] = trade.get_price()
        stock_position_info['quantity'] = trade.get_quantity()
        stock_position_info['net'] = -(float(stock_position_info['avg_price'])*int(stock_position_info['quantity']))
        self._position_table[trade.get_stock()] = stock_position_info
        
    def update_again_stock_in_position_table(self, trade):
        '''
        用于上次清仓后再次交易这只股票的情况，这种情况下quantity=0 ,net！=0
        eg: {'direction': 'long', 'quantity': 0, 'net': 10, 'avg_price': 8.63}
        '''         
        #stock_position_info = self._position_table[trade.get_stock()]
        stock_position_info = self._position_table[self.find_stock_in_position_table(trade.get_stock())]
        stock_position_info['avg_price'] = trade.get_price()
        stock_position_info['direction'] = trade.get_direction()
        stock_position_info['quantity'] = trade.get_quantity()
        stock_position_info['net'] += -(float(stock_position_info['avg_price'])*int(stock_position_info['quantity']))
    
    def update_stock_in_position_table(self, trade):
        #find stock in position_table
        #stock_position_info = self._position_table[trade.get_stock()]
        stock_position_info = self._position_table[self.find_stock_in_position_table(trade.get_stock())]
        stock_position_info['direction']
        if not stock_position_info:
            print "stock not in self._position_table"
            return False
        else:
            direction = trade.get_direction()
            price = trade.get_price()
            quantity = trade.get_quantity()
            
            if direction == stock_position_info['direction']: #enter same stock again, same direction update average price , quantity, net
                stock_position_info['net'] += -(float(price) * int(quantity))
                stock_position_info['avg_price'] = (quantity*price + stock_position_info['quantity']*stock_position_info['avg_price']) / (int(quantity)+int(stock_position_info['quantity']))
                stock_position_info['avg_price'] = float("%0.02f"%float(stock_position_info['avg_price']))
                stock_position_info['quantity'] += quantity
            else:
                if quantity <= stock_position_info['quantity']:
                    stock_position_info['net'] += float(price)*int(quantity)
                    #stock_position_info['net'] += self.cal_diff_direction_net(stock_position_info['direction'],stock_position_info['avg_price'],stock_position_info['quantity'],
                    #                                                        direction,price,quantity)
                    
                    stock_position_info['quantity'] -= quantity
                elif quantity > stock_position_info['quantity']:
                    #stock_position_info['net'] += self.cal_diff_direction_net(stock_position_info['direction'],stock_position_info['avg_price'],stock_position_info['quantity'],
                    #                                                      direction,price,stock_position_info['quantity'])
                    stock_position_info['net'] += float(price)*int(stock_position_info['quantity'])            #first count withdraw part net 
                    stock_position_info['quantity'] = quantity - stock_position_info['quantity']
                    stock_position_info['avg_price'] = price
                    stock_position_info['direction'] = direction
                    stock_position_info['net'] += -(float(price)*int(stock_position_info['quantity']))          #second count enter part net

    def cal_diff_direction_net(self, direction1, price1, quantity1, direction2 ,price2 ,quantity2):
        '''
        in this function, quantity2 should less than(or equal) quantity1
        '''
        print  direction1, price1, quantity1, direction2 ,price2 ,quantity2
        if quantity2 > quantity1:
            return False
        if direction1 == direction2:
            print "direction error"
            return False
        else:
            if direction1 == "long" and direction2 == 'short':
                return price2*quantity2 - price1*quantity1
            elif direction1 == "short" and direction2 == 'long':
                return price1*quantity1 - price2*quantity2
            else:
                print "direction error"
                return False
    
    def trade_stock_exist_in_position_table(self, trade):
        stock_key_list = []
        if not self._position_table:
            return False
        else:
            for stockinfo in self._position_table.keys():
                stock_key_list.append(stockinfo.get_stockinfo_key())
        if not trade:
            print "ERROR stock_exist_in_position_table error"
        else:
            return trade.get_stock().get_stockinfo_key() in stock_key_list
    
    def find_stock_in_position_table(self, stockinfo):
        s_if = ''
        key = stockinfo.get_stockinfo_key()
        for s in self._position_table.keys():
            pts_key = s.get_stockinfo_key()
            if key == pts_key:
                s_if = s
                break
        return s_if
    
    def trade_exec(self, trade):
        '''
        execute a trade order
        '''
        #print self._position_table[self.find_stock_in_position_table(trade.get_stock())]['quantity']
        if not trade:
            return False
        else:
#             if trade.get_stock() not in self._position_table.keys():
#                 self.init_stock_in_position_table(trade)              #init this stock
#             elif self._position_table[trade.get_stock()]['quantity'] == 0:
#                 self.update_again_stock_in_position_table(trade)
#             else:
#                 self.update_stock_in_position_table(trade)               #cal stock 
            if not self.trade_stock_exist_in_position_table(trade):
                self.init_stock_in_position_table(trade)              #init this stock
            elif self._position_table[self.find_stock_in_position_table(trade.get_stock())]['quantity'] == 0:
                self.update_again_stock_in_position_table(trade)
            else:
                self.update_stock_in_position_table(trade)               #cal stock 
                
        #print self._position_table
                
    def desc(self):
        if not self._trade_list:
            print "position have no trade"
        for i in self._trade_list:
            print "---------"
            print "deal date:",i.get_deal_time()
            print "stock code:",i.get_stock().get_stockinfo_code()
            print "stock exchange:",i.get_stock().get_stockinfo_exch()
            print "directioin:",i.get_direction()
            print "price:",i.get_price()
            print "quantity:",i.get_quantity()
    
    def clear_stock(self, date, stock):
        '''
        close a stock position: generate a stock clear position trade and exce it 
        '''
        if self.get_position_table_stock_quantity(stock) == 0:
            print "ERROR, clear stock error, this stock's quantity is 0"
            exit(2)
        else:
            t = self.generate_reverse_out_trade_today_close(stock, date)
            self.add(t)
    
    def clear_position(self, date):
        '''
        close position: generate a lot of clear position trade and exce it
        '''
        #print self._position_table
        for stock in self._position_table:
            if self.get_position_table_stock_quantity(stock) == 0:
                continue
            else:
                t = self.generate_reverse_out_trade_today_close(stock, date)
                #print t
                self.add(t)

    def generate_reverse_out_trade_today_close(self, stock, date):
        if not stock or not date:
            print "ERROR stock or date is null"
            return False
        #if stock not in self._position_table:
        if not self.find_stock_in_position_table(stock):
            print stock,"this stock not in _position_table" 
            return False
        else:
            t = Trade(date,
                      stock,
                      self.get_reverse_direction(self.get_position_table_stock_direction(stock)),
                      'today:Close',
                      self.get_position_table_stock_quantity(stock),
                      'out')
            return t
        
    def get_reverse_direction(self, direction):
        if direction not in DIRECTION_LIST:
            print "direction not in DIRECTION_LIST"
            return False
        else:
            if direction == 'long':
                return 'short'
            elif direction == 'short':
                return 'long'
            else:
                print "direction doesn't change"
                return direction
            
    def get_table_list(self):
        return self._trade_list
            
    def get_position_table(self):
        return self._position_table    
    
    def get_position_table_stock_code(self, stock):    
        return self._position_table[self.find_stock_in_position_table(stock)]['code']
    
    def get_position_table_stock_exch(self, stock):
        return stock.get_stockinfo_exch()
    
    def get_position_table_stock_direction(self, stock):
        return self._position_table[self.find_stock_in_position_table(stock)]['direction']
        
    def get_position_table_stock_net(self, stock):
        return self._position_table[self.find_stock_in_position_table(stock)]['net']
        
    def get_position_table_stock_quantity(self, stock):
        return self._position_table[self.find_stock_in_position_table(stock)]['quantity']
    
    def get_position_table_stock_avgprice(self, stock):
        return self._position_table[self.find_stock_in_position_table(stock)]['avg_price']
        
    def desc_table_order_result(self):
        for stock_if in self._position_table:
            #print stock_if.get_stockinfo_code(),stock_if.get_stockinfo_exch(),self._position_table[stock_if]
            for trade in self._trade_list:
                if stock_if.get_stockinfo_code() == trade.get_stock_code() and stock_if.get_stockinfo_exch() == trade.get_stock_exch():
                    print trade.get_stock_code(),'\t', 
                    print trade.get_stock_exch(),'\t',
                    print trade.get_deal_time(),'\t',
                    print trade.get_direction(),'\t',
                    print trade.get_price(),'\t',
                    print trade.get_quantity()
        
    def desc_position_table_result(self):
        desc = self.get_position_table()
        for stock_info in desc:
            print stock_info.get_stockinfo_code(),'\t',stock_info.get_stockinfo_exch(),'\t',desc[stock_info]['net']
            print "current position:",'\t',desc[stock_info]
            
    def desc_position_table_result_no_current_position(self):
        desc = self.get_position_table()
        for stock_info in desc:
            print stock_info.get_stockinfo_code(),'\t',stock_info.get_stockinfo_exch(),'\t',desc[stock_info]['net']
            
    def get_trade(self, date):
        res_list = []
        for t in self._trade_list:
            if t.get_deal_time() == date:
                res_list.append(t)
        return res_list
                
class Trade():
    '''
    Class Trade use to record every deal infomation ,
    include: deal_time, stock, direction, price, quantity, 
    '''
    def __init__(self,deal_datetime, stock, direction, price, quantity, enter):
        assert direction in DIRECTION_LIST
        #self._deal_time = deal_time
        self._deal_datetime = deal_datetime
        self._stock = stock
        self._direction = direction
        #self._price = float(price)
        self._price = price
        self._quantity = quantity
        self._enter = enter              #use to easier computing strategyRecorder
    
    def get_deal_time(self):
        return self._deal_datetime
    
    def get_stock(self):
        return self._stock
    
    def get_direction(self):
        return self._direction
    
    def get_quantity(self):
        return self._quantity
    
    def get_price(self):
        return self._price
    
    def get_stock_code(self):
        return self._stock.get_stockinfo_code()

    def get_stock_exch(self):
        return self._stock.get_stockinfo_exch()
    
    def get_stock_enter(self):
        return self._enter
    
    def set_price(self, price):
        if price:
            self._price = float(price)
        else:
            print "set price error"
            return False
        
    def desc(self):
        print "_deal_datetime:",self.get_deal_time()
        print "_code:",self.get_stock_code()
        print "_exch:",self.get_stock_exch()
        print "_direction:",self.get_direction()
        print "_quantity",self.get_quantity()
        print "_price",self.get_price()
        print "_enter:",self.get_stock_enter()
    
if __name__ == '__main__':
    
    now = datetime.datetime.now().strptime('2002-08-17','%Y-%m-%d')
    start = datetime.datetime.strptime('2014-09-20','%Y-%m-%d')
    end = datetime.datetime.strptime('2014-09-22','%Y-%m-%d')
    
    si = StockInfo({'code':'600882','exch':'ss'})
    si2 = StockInfo({'code':'600882','exch':'ss'})
    si3 = StockInfo({'code':'600882','exch':'ss'})
    #t1 = Trade(start,si,'long',10,100)
    p = Position()
    #p.add(t1)
    #print p._position_table
    p.add(Trade(end,si,'long',19,100,'in'))
    p.add(Trade(end,si2,'short',11.63,100,'out'))
    p.add(Trade(start,si3,'long',12.63,100,'in'))
    #p.add(Trade(end,si2,'short',11.63,500,'mix'))
    #p.add(Trade(end,si,'short',12.63,100))
    #p.add(Trade(end,si,'short',12.63,100))
#    p.add(Trade(end,si2,'long',0.63,100))
#    p.add(Trade(end,si2,'short',0.1,100))
    #p.add(Trade(end,si2,'short','today:Close',1000))
    #p.clear_stock(end,si2)
    #p.clear_position(end)
    #for t in p._trade_list:
    #    t.desc()
    p.desc()
    p.desc_table_order_result()
    p.desc_position_table_result()
    #print p._position_table
    print p.get_trade(end.date())





