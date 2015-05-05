#!/usr/bin/python
"""
Created on Mon May  4 17:50:37 2015
@author: mints
"""

def quoted_list(data):
    return ','.join(["'%s'" % key for key in data])

def quoted_list_item(data, item):
    return ','.join(["'%s'" % key[item] for key in data])