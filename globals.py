# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:00:29 2014

@author: minz
"""

#import sqlite3
from pysqlite2 import dbapi2 as sqlite3
from jinja2 import Environment, PackageLoader

JINJA = Environment(loader=PackageLoader('AIP_clusters', '.'))

def get_conn():
    conn = sqlite3.connect('AIP_clusters.sqlite')
    conn.enable_load_extension(True)
    conn.execute("select load_extension('/home/mints/prog/AIP_clusters/sqlite_extentions/libsqlitefunctions.so')")
    conn.enable_load_extension(False)
    return conn

def null_condition(column, value):
    if value is None or value == 'None' or value == 'none':
        return '%s is null' % column
    elif isinstance(value, str) or isinstance(value, unicode):
        return '%s = "%s"' % (column, value)
    else:
        return '%s = %s' % (column, value)

def nullify(value):
    if value is None or value == 'None' or value == 'none' or str(value) == '':
        return 'null'
    elif isinstance(value, str):
        return '"%s"' % value
    elif isinstance(value, unicode):
        return u'"%s"' % value #.encode('ascii', 'ignore')
    else:
        return value

def get_key_list(conn):
    keys = conn.execute("select distinct key from keys order by key")
    return [item[0] for item in keys.fetchall()]

def get_key_class_list(key):
    keys = get_conn().execute("select distinct key_class from keys where key = '%s'" % key)
    return [str(item[0]) for item in keys.fetchall()]

def get_key_description(key, key_class):
    keys = get_conn().execute("""select description, data_format
                                   from keys
                                  where key = '%s'
                                    and %s""" % (key, null_condition('key_class', key_class)))
    return keys.fetchone()
