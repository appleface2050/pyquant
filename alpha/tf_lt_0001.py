# -*- coding: utf-8 -*-

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.alpha import Alpha
from lib.position import Trade
from lib.stock import StockInfo

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
                    
                    #si2 = StockInfo({'code':'900920','exch':'ss'})
                    s = StockInfo({'code':stock['code'], 'exch':stock['exch']})
                    self.add_order(Trade(tomorrow,s,'long','today:Close',100,'in'))
                        #print (tomorrow,stock,'long','today:Close',100)
                    #print stock['code'],start,stock['chart'][start]
                if self.trigger_overtake('MA120','MA240','down',stock_data,start):       #withdraw strategy
                    #print start,stock['chart'][start],'down'
                    s = StockInfo({'code':stock['code'],'exch':stock['exch']})
                    if self._position.find_stock_in_position_table(s) and self._position.get_position_table_stock_quantity(s) != 0:        #stock exist in position table and quantity !=0
                        self.clear_stock(tomorrow,s)

                    
if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    sim_start = datetime.datetime.strptime('2014-01-01','%Y-%m-%d').date()
    sim_end = datetime.datetime.strptime('2014-02-01','%Y-%m-%d').date()
    #sim_end = yest
    stock_condition = {'date':sim_start,'condition':[{'item':'close','min':0.0,'max':5.0}]}
    #stock_condition = {'date':sim_start,'condition':[{'item':'code','min':'002407','max':'002407'}]}
    indicator_list = ['MA120','MA240'] 
    print 'Simulating Strategy ...',sim_start,'-->',sim_end 
    s = TFLT0001(sim_start,sim_end,stock_condition,indicator_list)
    s.running()
    s.report()
    print 'Simulating Strategy done, time used:  ',datetime.datetime.now()-now
    
    
    



