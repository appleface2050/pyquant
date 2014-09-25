#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Abstract: Stat Models

import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))




class Alpha(object):
    #_qq = [1,2,3]
    def __init__(self):
        self._qq = [1]

         
class B(Alpha):
    def __init__(self):
        super(B, self).__init__()
        print self._qq
        
        
b = B()