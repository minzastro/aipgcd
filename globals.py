# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:00:29 2014

@author: minz
"""

from pysqlite2 import dbapi2 as sqlite3
from jinja2 import Environment, FileSystemLoader
import os
import sqllist
sqllist.load_defaults()

if os.path.dirname(__file__).startswith('/srv'):
    DB_LOCATION = '/srv/db/cluster-db/'
else:
    DB_LOCATION = ''


JINJA = Environment(loader=FileSystemLoader('.'))


def get_conn(dict_row=False):
    conn = sqlite3.connect('%sAIP_clusters.sqlite' % DB_LOCATION)
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

def get_key_list(conn, any_subkey=False):
    keys = conn.execute("select key, subkey from keys").fetchall()
    result = []
    for key, subkey in keys:
        if subkey is None:
            result.append(key)
        else:
            result.append('%s,%s' % (key, subkey))
    if any_subkey:
        for xkey in conn.execute("select distinct key from keys").fetchall():
            result.append('%s,all subkeys' % xkey)
    return result

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
    if xformat is None or xformat == '':
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
