#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.position import Trade,Position
from conf.settings import RISK_FREE_RATE_DAILY
from lib.utils import std

class StrategyRecorder(object):
    '''
    use to record daily stratgy status 
    '''
    def __init__(self):
        self._strategy_recorder = {}
        '''
        {date:
{net， float_net, solid_net, current_exposure，acc_exposure, trade_count,win_trade_count,lose_trade_count}
         }
         '''
        #finish running
        self._max_exposure = 0.0
        #self._daily_oscillation_standard_deviation = 0.0
        self._enter_time = 0
        self._trade_days = 0
        self._absolute_rate_of_return = 0.0
        self._yearly_rate_of_return = 0.0        
        self._sharp_retio = 0.0
        self._max_draw_down = 0.0    #最大搓跌
        self._max_draw_down_duration = ''  #最长搓跌期
        self._total_net = 0.0
        self._total_exposure = 0
        self._total_trade_time = 0
        self._total_win_time = 0
        self._total_lose_time = 0
        
        self._daily_net_value_list = []
    
    def get_sharp_retio(self):
        return self._sharp_retio
    
    def get_strategy_recorder(self):
        return self._strategy_recorder 
    
    def record(self, dat, position):
        #print dat, position.get_table_list(),position.get_position_table()
        trade_list = position.get_trade(dat)
        #if trade_list:
        #    for t in trade_list:
        #        self.cal_solid_net(dat,t)
        solid_net = self.get_last_trade_day_solid_net(dat)
        if trade_list:
            for t in trade_list:
                solid_net += self.cal_delta_solid_net(dat,t)
        float_net = self.cal_float_net(dat,position)
        net = solid_net + float_net
        self._strategy_recorder[dat] = {'solid_net':solid_net,
                                       'float_net':float_net,
                                       'net':net,
                                       }
        #print self._strategy_recorder[dat]
    
    def cal_finish_strategy_indicators(self):
        for i in self._strategy_recorder:
            print i,self._strategy_recorder[i]
        self._daily_oscillation_standard_deviation
        self._sharp_retio 
    
    def report(self):
        self.cal_finish_strategy_indicators()
        print "sharp_retio:",self.get_sharp_retio()
    
    
    
    def cal_delta_solid_net(self, dat, trade):
        res = 0
        if dat != trade.get_deal_time():
            print "ERROR dat != trade.get_deal_time()"
            exit(2)
        if trade.get_stock_enter() == 'in':
            res = -(float(trade.get_price()) * int(trade.get_quantity()))
        elif trade.get_stock_enter() == 'out':
            res = float(trade.get_price()) * int(trade.get_quantity())
        else:
            print "ERROR enter type wrong"
            exit(2)
        return res
    
    def get_last_trade_day_solid_net(self, dat):
        day_list = self._strategy_recorder.keys()
        if not day_list:
            return 0
        else:
            last_day = self.bubblesort_desc(day_list)[0]
            return self.get_strategy_recorder()[last_day]['solid_net']
    
    def cal_float_net(self, dat, position):
        #print position.get_position_table()
        sum_float_net = 0
        pt = position.get_position_table()
        for stock_if in pt:
            current_price = stock_if.get_last_exist_close_price(dat)                #for some day, stock data missing
            quantity = position.get_position_table_stock_quantity(stock_if)
            if current_price and quantity:
                float_net = current_price * quantity
            else:
                float_net = 0
            sum_float_net += float_net
        return sum_float_net
    
    def bubblesort_desc(self, ob_list):
        for j in range(len(ob_list)-1,-1,-1):
            for i in range(j):
                if ob_list[i] < ob_list[i+1]:
                    ob_list[i],ob_list[i+1] = ob_list[i+1],ob_list[i]
        return ob_list
    
if __name__ == '__main__':
    now = datetime.datetime.now()
    start = datetime.datetime.strptime('2014-08-22','%Y-%m-%d').date()
    end = datetime.datetime.strptime('2014-09-22','%Y-%m-%d').date()
    si = StockInfo({'code':'600882','exch':'ss'})
    si2 = StockInfo({'code':'600883','exch':'ss'})
    p = Position()
    #p.add(Trade(end,si,'long',20,100,'in'))
    #p.add(Trade(end,si,'short',20,100,'out'))
    p.add(Trade(end,si2,'long',20,100,'in'))
    p.add(Trade(end,si2,'long',20,100,'in'))
    p.desc()
    s = StrategyRecorder()
    s.record(end,p)
    s.report()
    print datetime.datetime.now()-now
    
    
    
    
    
    
    
    
    
    
    
    
    