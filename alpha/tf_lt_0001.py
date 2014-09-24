# -*- coding: utf-8 -*-

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.alpha import StockPoolBuilder,Alpha

class TFLT0001(Alpha):
    def __init__(self, sim_start, sim_end, sp):
        if sim_start > sim_end:
            print "sim time error"
            return False
        else:
            self._sim_start = sim_start
            self._sim_end = sim_end
            self._sp = sp
            self._strategy_desc = """
        strategy name:tf_lt_0001
        create time:2014-09-18 
        period type:long
        period:
        strategy description:
                    当120日均线突破240日均线  clear 并且long 100
                    当240日均线突破120日均线 clear 并且short 100
    """
    
    def strategy(self, start):
        for stock in self._sp:
            sp_all_date = stock['chart'].keys()
            if start in sp_all_date:
                print stock['chart'][start]
        

if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    print yest
    #stock_condition = {'date':yest,'condition':[{'item':'Close','min':18.0,'max':22.0},{'item':'Volume','min':'','max':1000000}]}
    stock_condition = {'date':yest,'condition':[{'item':'code','min':'600882','max':'600882'}]}
    indicator_list = ['MA120','MA240']
    sim_start = datetime.datetime.strptime('2014-09-01','%Y-%m-%d').date()
    sim_end = yest
    spb = StockPoolBuilder(stock_condition,indicator_list,sim_start)
    print "stocknum:",spb.count_stock_num()
    
    spb.build_stock_pool_indicator()
    spb.delete_incompleted_data()
    print 'Initializing Stock Pool done, time used:  ',datetime.datetime.now()-now
    
    #for stock in spb._ind._useful_ind_format_data:
    #    print stock
    print "---------------------------------------"
    print 'Simulating Strategy ...',sim_start,'-->',sim_end 
    s = TFLT0001(sim_start,sim_end,spb.get_useful_ind_format_data())
    s.running()
    print 'Simulating Strategy done, time used:  ',datetime.datetime.now()-now
    







