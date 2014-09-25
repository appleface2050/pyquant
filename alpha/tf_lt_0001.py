# -*- coding: utf-8 -*-

import os
import sys
import datetime
from lib.stock import StockInfo

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.alpha import Alpha
from lib.position import Trade

class TFLT0001(Alpha):
    def __init__(self, sim_start, sim_end, stock_condition, indicator_list):
        super(TFLT0001, self).__init__(sim_start, sim_end, stock_condition, indicator_list)
        self._strategy_name = "TFLT0001"
        
    def strategy_calculating(self, start):
        tomorrow = self.find_next_trade_day(start)
        #print tomorrow
        if tomorrow: # lastest trade day do not sim
            for stock in self._sp:
                stock_data = stock['chart']
                
                if self.trigger_overtake('MA120','MA240','up',stock_data,start):         #enter strategy
                    #print start,stock['chart'][start]
                    #si2 = StockInfo({'code':'900920','exch':'ss'})
                    s = StockInfo({'code':stock['code'], 'exch':stock['exch']})
                    self.add_order(Trade(tomorrow,s,'long','today:Close',100))
                        #print (tomorrow,stock,'long','today:Close',100)
                    #print stock['code'],start,stock['chart'][start]
                if self.trigger_overtake('MA120','MA240','down',stock_data,start):       #withdraw strategy
                    s = StockInfo({'code':stock['code'], 'exch':stock['exch']})
                    self.clear_stock(tomorrow,s)

if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    stock_condition = {'date':yest,'condition':[{'item':'code','min':'300003','max':'300003'}]}
    indicator_list = ['MA120','MA240']
    sim_start = datetime.datetime.strptime('2012-12-01','%Y-%m-%d').date()
    sim_end = yest
    print 'Simulating Strategy ...',sim_start,'-->',sim_end 
    s = TFLT0001(sim_start,sim_end,stock_condition,indicator_list)
    s.running()
    s.report()
    print 'Simulating Strategy done, time used:  ',datetime.datetime.now()-now
    
    
    



