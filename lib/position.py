#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import datetime
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.indicator import Indicator
from conf.settings import TECH_ANALY_IND,DIRECTION_LIST

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
            self._trade_list.append(trade)
            self.trade_exec(trade)
            return True
        else:
            return False
    
    def init_stock_in_position_table(self, trade):
        stock_position_info = {}
        stock_position_info['code'] = trade.get_stock().get_stockinfo_code()         #just for debug 
        stock_position_info['direction'] = trade.get_direction()
        stock_position_info['avg_price'] = trade.get_price()
        stock_position_info['quantity'] = trade.get_quantity()
        stock_position_info['net'] = 0.0
        self._position_table[trade.get_stock()] = stock_position_info
        
        
    def update_again_stock_in_position_table(self, trade):
        '''
        用于上次清仓后再次交易这只股票的情况，这种情况下quantity=0 ,net！=0
        eg: {'direction': 'long', 'quantity': 0, 'net': 10, 'avg_price': 8.63}
        '''         
        stock_position_info = self._position_table[trade.get_stock()]
        stock_position_info['avg_price'] = trade.get_price()
        stock_position_info['direction'] = trade.get_direction()
        stock_position_info['quantity'] = trade.get_quantity()
        #stock_position_info['net'] do not update
    
    def update_stock_in_position_table(self, trade):
        #find stock in position_table
        stock_position_info = self._position_table[trade.get_stock()]
        if not stock_position_info:
            print "stock not in self._position_table"
            return False
        else:
            direction = trade.get_direction()
            price = trade.get_price()
            quantity = trade.get_quantity()
            
            if direction == stock_position_info['direction']: #same direction update average price , quantity
                stock_position_info['avg_price'] = (quantity*price + stock_position_info['quantity']*stock_position_info['avg_price']) / (int(quantity)+int(stock_position_info['quantity']))
                stock_position_info['avg_price'] = float("%0.02f"%float(stock_position_info['avg_price']))
                stock_position_info['quantity'] += quantity
            else:
                if quantity <= stock_position_info['quantity']:
                    stock_position_info['net'] += self.cal_diff_direction_net(stock_position_info['direction'],stock_position_info['avg_price'],stock_position_info['quantity'],
                                                                            direction,price,quantity)
                    stock_position_info['quantity'] -= quantity
                elif quantity > stock_position_info['quantity']:  
                    stock_position_info['net'] += self.cal_diff_direction_net(stock_position_info['direction'],stock_position_info['avg_price'],stock_position_info['quantity'],
                                                                          direction,price,stock_position_info['quantity'])
                    stock_position_info['quantity'] = quantity - stock_position_info['quantity']
                    stock_position_info['avg_price'] = price
                    stock_position_info['direction'] = direction


    def cal_diff_direction_net(self, direction1, price1, quantity1, direction2 ,price2 ,quantity2):
        '''
        in this function, quantity2 should less than(or equal) quantity1
        '''

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
    
    
    def trade_exec(self, trade):
        if not trade:
            return False
        else:
            if trade.get_stock() not in self._position_table.keys():
                self.init_stock_in_position_table(trade)              #init this stock
            elif self._position_table[trade.get_stock()]['quantity'] == 0:
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
            
    def close_position(self):
        '''
        close position: generate a close position trade and exce it
        '''
        start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "close position need today close price ,not ready yet"
        #print self._position_table
        for stock_info in self._position_table:
            cpt = Trade(start,stock_info,'short',9.63,200)
            
        
    
    def result(self):
        pass
        
class Trade():
    '''
    Class Trade use to record every deal infomation ,
    include: deal_time, stock, direction, quantity, 
    '''
    def __init__(self,deal_datetime, stock, direction, price, quantity ):
        assert direction in DIRECTION_LIST
        #self._deal_time = deal_time
        self._deal_datetime = deal_datetime
        self._stock = stock
        self._direction = direction
        self._price = float(price)
        self._quantity = quantity
        
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
    
if __name__ == '__main__':
    
    now = datetime.datetime.now().strptime('2002-08-17','%Y-%m-%d')
    start = datetime.datetime.strptime('2014-09-20','%Y-%m-%d')
    end = datetime.datetime.strptime('2014-09-21','%Y-%m-%d')
    
    si = StockInfo({'code':'600882','exch':'ss'})
    si2 = StockInfo({'code':'900920','exch':'ss'})
    t1 = Trade(start,si,'long',8.63,100)
    p = Position()
    p.add(t1)
    #print p._position_table
    p.add(Trade(end,si,'short',9.63,200))
    p.add(Trade(end,si,'short',11.63,100))
    p.add(Trade(end,si,'short',12.63,100))
    p.add(Trade(end,si,'short',12.63,100))
    p.add(Trade(end,si,'short',12.63,100))
    p.add(Trade(end,si2,'long',0.63,100))
    #p.close_position()
    p.add(Trade(end,si2,'short',0.1,100))
    p.add(Trade(end,si,'long',11.63,500))
    p.desc()
    print p._position_table





