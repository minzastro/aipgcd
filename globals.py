# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:00:29 2014

@author: minz
"""

#import sqlite3
from pysqlite2 import dbapi2 as sqlite3
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
import sqllist
sqllist.load_defaults()


JINJA = Environment(loader=FileSystemLoader('.'))


def get_conn(dict_row=False):
    conn = sqlite3.connect('AIP_clusters.sqlite')
    conn.enable_load_extension(True)
    conn.execute("select load_extension('%s/sqlite_extentions/libsqlitefunctions.so')" % os.path.dirname(__file__))
    conn.enable_load_extension(False)
    if dict_row:
        conn.row_factory = sqlite3.Row
    return conn

def null_condition(column, value):
    if value is None or value == 'None' or value == 'none':
        return '%s is null' % column
    elif isinstance(value, str) or isinstance(value, unicode):
        return '%s = "%s"' % (column, value)
    else:
        return '%s = %s' % (column, value)

def nullify(value):
    if value is None or value == 'None' or value == 'none':
        return 'null'
    elif isinstance(value, str):
        if value == '':
            return 'null'
        return '"%s"' % value
    elif isinstance(value, unicode):
        if value == u'':
            return 'null'
        return u'"%s"' % value #.encode('ascii', 'ignore')
    else:
        return value

def get_key_list(conn):
    keys = conn.execute("select distinct key || ',' || ifnull(subkey, 'none') from keys")
    return [item[0] for item in keys.fetchall()]

def get_subkey_list(key):
    keys = get_conn().execute("select distinct subkey from keys where key = '%s'" % key)
    return [str(item[0]) for item in keys.fetchall()]

def get_key_description(key, subkey):
    keys = get_conn().execute("""select description, data_format
                                   from keys
                                  where key = '%s'
                                    and %s""" % (key, null_condition('subkey', subkey)))
    return keys.fetchone()

def get_table_columns(table):
    cur = get_conn().execute('PRAGMA table_info("%s")' % table)
    return [row[1] for row in cur.fetchall()]


def get_brief_columns(table, masks, negate=True):
    from fnmatch import filter
    col = get_table_columns(table)
    matched = []
    for mask in masks:
        matched.extend(filter(col, mask))
    if negate:
        result_set = set(col) - set(matched)
    else:
        result_set = set(matched)
    columns = get_conn().execute("""select column_name
      from reference_tables_columns
     where reference_table = '%s'
       and column_name in (%s)
       order by uid""" % (table, ','.join("'%s'" % c for c in result_set)))
    result = [row[0] for row in columns.fetchall()]
    return result

def format_value(value, xformat):
    if xformat is None:
        return str(value)
    elif value is None:
        return ''
    else:
        if xformat[-1] in 'gef':
            return ('%%%s' % xformat) % float(value)
        elif xformat[-1] in 'd':
            return ('%%%s' % xformat) % int(value)
        else:
            return ('%%%s' % xformat) % value
