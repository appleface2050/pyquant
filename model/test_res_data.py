#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Abstract: Stat Models

import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.database import Model

class TestOrderData(Model):
    '''
    A share stock data Model
    '''    
    _db = 'A_shares_data'
    _pk = 'id'
    _table = 'test_order_data'
    _fields = set(['id','strategy','code','exchange','deal_date','direction','price','quantity','uptime'])
    _scheme = ("`id` BIGINT NOT NULL AUTO_INCREMENT",
        "`strategy` varchar(16) NOT NULL DEFAULT ''",
        "`code` varchar(16) NOT  NULL DEFAULT ''",
        "`exchange` varchar(16) NOT NULL DEFAULT ''",
        "`deal_date` datetime NOT NULL DEFAULT '1970-01-01 00:00:00'",
        "`direction` enum('long','short','unknown') NOT NULL DEFAULT 'unknown'",
        "`price` float NOT NULL DEFAULT '0'",
        "`quantity` INT NOT NULL DEFAULT '0'",
        "`uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        "PRIMARY KEY `idx_id` (`id`)",
        "UNIQUE KEY `test_order_data_code_exchange_deal_date_direction` (`code`,`exchange`,`deal_date`,`direction`)")