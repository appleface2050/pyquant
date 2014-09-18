#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Abstract: Stat Models

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.utils import strptime,time_next
from lib.database import Model

class StockData(Model):
	'''
	A share stock data Model
	'''	
	_db = 'A_shares_data'
	_pk = 'id'
	_table = 'a_shares_stock_data'
	_fields = set(['id','code','exchange','Date','Open','High','Low','Close','Volume','AdjClose','uptime'])
	_scheme = ("`id` BIGINT NOT NULL AUTO_INCREMENT",
		"`code` varchar(32) NOT  NULL DEFAULT ''",
		"`exchange` varchar(32) NOT NULL DEFAULT ''",
		"`Date` datetime NOT NULL DEFAULT '1970-01-01 00:00:00'",
		"`Open` float NOT NULL DEFAULT '0'",
		"`High` float NOT NULL DEFAULT '0'",
		"`Low` float NOT NULL DEFAULT '0'",
		"`Close` float NOT NULL DEFAULT '0'",
		"`Volume` BIGINT NOT NULL DEFAULT '0'",
		"`AdjClose` float NOT NULL DEFAULT '0'",
		"`uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
		"PRIMARY KEY `idx_id` (`id`)",
		"UNIQUE KEY `code_exchange_Date` (`code`,`exchange`,`Date`)")


