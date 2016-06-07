#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    config for NaverMonitor
    by Chae Jong Bin
"""

__description__ = 'config for NaverMonitor'
__author__ = 'Chae Jong Bin'

import datetime

SAMPLE_DIR = ".\\sample_%s\\" % datetime.date.today()

NAVER_API_URL = "http://openapi.naver.com/search?"
NAVER_API_KEY = ""

PE_SIGNATURE_PATH = ".\\data\\userdb.txt"

TRID_PATH = ".\\bin\\trid"
TRID_SIGNATURE_PATH = ".\\data\\triddefs.trd"
