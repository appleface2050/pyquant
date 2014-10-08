# -*- coding: utf-8 -*-

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.alpha import AlphaFullAmount,Alpha
from lib.position import Trade
from lib.stock import StockInfo
from lib.stockcondition import StockCondition
from model.stock_data import StockData

class TFLT0001FA(AlphaFullAmount):
    '''
    tf_lt_0001策略全量测试
    '''
    def __init__(self, sim_start, sim_end, stock_condition, indicator_list):
        super(TFLT0001FA, self).__init__(sim_start, sim_end, stock_condition, indicator_list)
        self._strategy_name = "TFLT0001FA"
        
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
                    
                    #print stock['code'],start,stock['chart'][start]
                if self.trigger_overtake('MA120','MA240','down',stock_data,start):       #withdraw strategy
                    #print start,stock['chart'][start],'down'
                    s = StockInfo({'code':stock['code'],'exch':stock['exch']})
                    if self._position.find_stock_in_position_table(s) and self._position.get_position_table_stock_quantity(s) != 0:        #stock exist in position table and quantity !=0
                        self.clear_stock(tomorrow,s)

class FuallAmountTestManager():
    def __init__(self, sim_start, sim_end, indicator_list):
        self._sim_start = sim_start
        self._sim_end = sim_end
        self._indicator_list = indicator_list
        
        self._full_stock_list = self.get_full_stock_list()
        self._single_test_stock_amount = 10
        self._alpha = ''
        
        self.run()
        
    def get_full_stock_list(self):
        stock_list = StockData.mgr().get_all_stock_info()[:]
        return stock_list
    
    def run(self):
        stock_list = []
        if not self._full_stock_list:
            print "stock list is empty"
            return False
        while(self._full_stock_list):
            
            if len(stock_list) < self._single_test_stock_amount:
                stock_list.append(self._full_stock_list.pop(0))
            else:
                stock_condition = StockCondition({'type':'stocks',
                                                  'term':stock_list
                                                  })
                print 'Simulating Strategy ...',sim_start,'-->',sim_end 
                self._alpha = TFLT0001FA(self._sim_start,self._sim_end,stock_condition,self._indicator_list)
                self._alpha.running()
                self._alpha.data2db()
                stock_list = []
                self._alpha = ''
                print "last stock number:",len(self._full_stock_list)
                print 'Simulating Strategy done, time used:  ',datetime.datetime.now()-now
                    
if __name__ == '__main__':
#     now = datetime.datetime.now()
#     yest = now.date() - datetime.timedelta(days=1)
#     sim_start = datetime.datetime.strptime('1992-01-01','%Y-%m-%d').date()
#     sim_end = datetime.datetime.strptime('2002-10-01','%Y-%m-%d').date()
#     stock_condition = StockCondition({'type':'stocks',
#                                       'term':[{'code': '000002', 'exch': 'sz'}, {'code': '000004', 'exch': 'sz'}]
#                                       }
#                                      )
#     indicator_list = ['MA120','MA240']
#     print 'Simulating Strategy ...',sim_start,'-->',sim_end 
#     s = TFLT0001FA(sim_start,sim_end,stock_condition,indicator_list)
#     s.running()
#     s.report()
#     print 'Simulating Strategy done, time used:  ',datetime.datetime.now()-now
    
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    sim_start = datetime.datetime.strptime('1991-01-01','%Y-%m-%d').date()
    sim_end = datetime.datetime.strptime('2014-10-01','%Y-%m-%d').date()
#     stock_condition = StockCondition({'type':'stocks',
#                                       'term':[{'code': '000002', 'exch': 'sz'}, {'code': '000004', 'exch': 'sz'}]
#                                       }
#                                      )
    indicator_list = ['MA120','MA240']
    s = FuallAmountTestManager(sim_start,sim_end,indicator_list)
    
    



