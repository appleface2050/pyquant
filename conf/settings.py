# -*- coding: utf-8 -*-
# Abstract: settings

import json

# mysql

A_SHARES_CODE = {
	'host':'192.168.88.129',
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




