#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conf.settings import STOCK_CONDITION_TYPE

class StockCondition(object):
    def __init__(self, stockcondition):
        self._stockcondition = stockcondition
        if not self._stockcondition['type']:
            print "StockCondition init error"
            return False
        else:
            assert self._stockcondition['type'] in STOCK_CONDITION_TYPE
            self._type = self._stockcondition['type']
            self._term = self._stockcondition['term']
            
    def get_stock_condition_type(self):
        return self._type
    
    def get_stock_condition_term(self):
        return self._term