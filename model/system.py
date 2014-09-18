#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Abstract: Stat Models

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.utils import strptime,time_next
from lib.database import Model

class ASharesCode(Model):
	'''
	A_shares_code Model
	'''	
	_db = 'A_shares_data'
	_pk = 'id'
	_table = 'a_shares_code'
	_fields = set(['id','code','exchange','name','uptime'])
	_scheme = ("`id` BIGINT NOT NULL AUTO_INCREMENT",
		"`code` varchar(32) NOT  NULL DEFAULT ''",
		"`exchange` varchar(32) NOT NULL DEFAULT ''",
		"`name` varchar(32) NOT NULL DEFAULT ''",
		"`uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
		"PRIMARY KEY `idx_id` (`id`)",
		"UNIQUE KEY `code_exchange` (`code`,`exchange`)")

	def get_all_codes(self):
		qtype = 'SELECT code,exchange' 
		q = self.Q(qtype=qtype)
		return q

	def get_all_unreal_code(self):
		sql = "SELECT code,exchange FROM a_shares_code WHERE a_shares_code.code NOT IN(SELECT CODE FROM a_shares_code_real)"
		q = self.raw(sql)
		return q

class ASharesCodeReal(Model):
	'''
	A_shares_code_real Model
	'''	
	_db = 'A_shares_data'
	_pk = 'id'
	_table = 'a_shares_code_real'
	_fields = set(['id','code','exchange','name','status','uptime'])
	_scheme = ("`id` BIGINT NOT NULL AUTO_INCREMENT",
		"`code` varchar(32) NOT  NULL DEFAULT ''",
		"`exchange` varchar(32) NOT NULL DEFAULT ''",
		"`name` varchar(32) NOT NULL DEFAULT ''",
		"`status` enum('valid','unvalid') NOT NULL DEFAULT 'valid'",
		"`uptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
		"PRIMARY KEY `idx_id` (`id`)",
		"UNIQUE KEY `code_exchange` (`code`,`exchange`)")

	def get_all_codes(self):
		qtype = 'SELECT code,exchange' 
		q = self.Q(qtype=qtype)
		return q

	def get_len_codes(self):
		sql = 'SELECT count(1)num from a_shares_code_real'
		q = self.raw(sql)
		return q[0]['num']

