# -*- coding: utf-8 -*-
# Abstract: settings

import json

# mysql
SDB = {
	'host':'192.168.0.168',
	'user':'opm',
	'passwd':'operationm_pwd',
	'db':'',
	'sock':'',
	'port':3356
}

MDB = {
    'host':'192.168.0.227',
    'user':'analy',
    'passwd':'analy123',
    'db':'',
    'sock':'/var/zhangyue/mysql/s_mysql.sock',
    'port':3306
}

RECHARGE_LOG_SDB = {
	'host':'192.168.0.161',
	'user':'ebk6',
	'passwd':'zzhy13579',
	'db':'',
	'sock':'',
	'port':3316
}

MONITOR_DATA_SDB = {
	'host':'192.168.0.150',
	'user':'analy',
	'passwd':'test1357',
	'db':'',
	'sock':'',
	'port':3316
}

EBK5_BOOK_EXPAND = {
    'host':'192.168.0.118',
    'port':3306,
    'user':'zydev',
    'passwd':'zzhy+2468!#!D5',
    'db':'',
    'sock':''
}

A_SHARES_CODE = {
	#'host':'192.168.88.129',
	'host':'localhost',
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

DB_TEST = {
    'm':{json.dumps(MDB):['logstat', 'logstatV2','week_ana','external','logstatv3','datamining','payment_v6'], json.dumps(EBK5_BOOK_EXPAND):['polarisebk5']},
    's':{json.dumps(SDB):['logstat', 'logstatV2','week_ana','logstatv3','payment_v6'], 
        json.dumps(RECHARGE_LOG_SDB):['book'],
        json.dumps(MONITOR_DATA_SDB):['dw_v6_test'],
        json.dumps(EBK5_BOOK_EXPAND):['polarisebk5'],
        json.dumps(MDB):['datamining','watchdog','external']
    },
}


TIMEOUT_REFETCH_DAILY = 15
TIMEOUT_FETCH_DAILY = 10





