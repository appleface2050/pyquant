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

TIMEOUT_REFETCH_DAILY = 15
TIMEOUT_FETCH_DAILY = 10





