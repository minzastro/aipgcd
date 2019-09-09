#!/usr/bin/python
"""
Created on Mon May  4 17:50:37 2015
@author: mints
"""

def quoted_list(data):
    return ','.join(["'%s'" % key for key in data])

def quoted_list_item(data, item):
    return ','.join(["'%s'" % key[item] for key in data])

def dict_values_to_list(args, keys):
    for valid in keys:
        if valid in args:
            if isinstance(args[valid], str):
                args[valid] = [args[valid]]
    return args

def key_subkey_cond(key):
    if ',' in key:
        key, subkey = key.split(',')
    else:
        subkey = ''
    #TODO: support key changes.
    if subkey == '':
        subkey_cond = 'subkey is null'
    else:
        subkey_cond = "subkey = '%s'" % subkey
    return key, subkey, subkey_cond