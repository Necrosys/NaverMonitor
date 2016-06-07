#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    libutil
    by Chae Jong Bin
"""

__description__ = 'libutil'
__author__ = 'Chae Jong Bin'

import urllib, os
import config

def downloadSample(url, fileName):
    try:
        os.mkdir(config.SAMPLE_DIR)
    except OSError:
        pass

    try:
        urllib.urlretrieve(url, fileName)
    except IOError:
        # urlretrieve collision bypass
        pass

def naverSearch(target, query):
    params = {"query": query,
              "target": target,
              "key": config.NAVER_API_KEY,
              "display": 100, # Maximum: 100
              "sort": "date"
              }

    queryString = urllib.urlencode(params)
    naverData = urllib.urlopen(config.NAVER_API_URL + queryString).read()

    return naverData

def execute_command(command):
    p = os.popen(command)
    return p.readlines()

def getSignaturesFromPEiD(pe):
    try:
        import peutils
        signatures = peutils.SignatureDatabase(config.PE_SIGNATURE_PATH)
        return signatures.match_all(pe)
    except:
        return None

def getSignaturesFromTrID(fileName):
    try:
        msg = execute_command(config.TRID_PATH + (" %s " % fileName) + ("-d:%s" % config.TRID_SIGNATURE_PATH))

        idx = -1
        for line in msg:
            idx += 1
            if line.find("Collecting data from file:") > -1:
                idx += 1
                break

        return msg[idx:]
    except:
        return None
