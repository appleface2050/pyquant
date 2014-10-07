# -*- coding: utf-8 -*-
# Abstract: settings

import json

# mysql

A_SHARES_CODE = {
	'host':'192.168.1.108',
	#'host':'localhost',
	'port':3306,
	'user':'appleface',
	'passwd':'root',
	'db':'',
	'sock':''
}


DB_CNF = {
	'm':{json.dumps(A_SHARES_CODE):['A_shares_data']},
	's':{json.dumps(A_SHARES_CODE):['A_shares_data']},
}

#DATAFECHING
TIMEOUT_REFETCH_DAILY = 15
TIMEOUT_FETCH_DAILY = 10


#technical analysis indicators
TECH_ANALY_IND = ['MA5','MA120','MA240','MACD','KDJ']

#direction list
DIRECTION_LIST = ['long', 'short']

#trade price order list
TRADE_PRICE_ORDER_LIST = ['today:Close','today:Open','today:AdjClose']

#tragger op list
TRIGGER_OP_LIST = ['up','down']

#trade enter list
TRADE_ENTER_LIST = ['in','out','inout','outin','mix']

STOCK_CONDITION_TYPE = ['total', #所有股票
					'condition', #条件选股
					]

RISK_FREE_RATE_DAILY = 0.03/252

RISK_FREE_RATE_YEARLY = 0.03

YEARLY_TRADE_DAY_NUMBER = 252















