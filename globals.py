# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:00:29 2014

@author: minz
"""

from pysqlite2 import dbapi2 as sqlite3
from jinja2 import Environment, FileSystemLoader
import os
import sqllist
import re
sqllist.load_defaults()

# This is for the ARCHIE server distribution
if os.path.dirname(__file__).startswith('/srv'):
    DB_LOCATION = '/srv/db/cluster-db/'
else:
    DB_LOCATION = ''


JINJA = Environment(loader=FileSystemLoader('.'))


def get_conn(dict_row=False):
    """
    Get the default connection to the database.
    Loads custom extension with lots of useful functions.
    """
    conn = sqlite3.connect('%sAIP_clusters.sqlite' % DB_LOCATION)
    print DB_LOCATION
    conn.enable_load_extension(True)
    conn.execute("select load_extension('%s/sqlite_extentions/libsqlitefunctions.so')" % os.path.dirname(__file__))
    conn.enable_load_extension(False)
    if dict_row:
        conn.row_factory = sqlite3.Row
    return conn


def null_condition(column, value):
    """
    Set the proper NULL condition:
    Value is treated as null if it is empty (is None)
    or contains a string 'None'.
    Otherwithe return a proper SQL constraint.
    """
    if value is None or value == 'None' or value == 'none':
        return '%s is null' % column
    elif isinstance(value, str) or isinstance(value, unicode):
        # Add quotes to condition
        return '%s = "%s"' % (column, value)
    else:
        return '%s = %s' % (column, value)


def nullify(value):
    """
    Returns proper SQL value, with null for None and
    quotes if needed.
    """
    if value is None or value == 'None' or value == 'none':
        return 'null'
    elif isinstance(value, str):
        if value == '':
            return 'null'
        return '"%s"' % value
    elif isinstance(value, unicode):
        if value == u'':
            return 'null'
        return u'"%s"' % value
    else:
        return value


def get_key_list(conn, any_subkey=False):
    """
    Returns a list of keys.
    :param any_subkey: add an item without any subkey for each key.
    :result: list of keys or key,subkey pairs.
    """
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
    """
    Returns a list of subkeys for a given key.
    """
    keys = get_conn().execute("""select distinct subkey
                                   from keys where key = '%s'""" % key)
    return [str(item[0]) for item in keys.fetchall()]


def get_key_description(key, subkey):
    """
    Get key's data format and description for
    a given key-subkey pair.
    """
    condition = null_condition('subkey', subkey)
    keys = get_conn().execute("""select description, data_format
                                   from keys
                                  where key = '%s'
                                    and %s""" % (key, condition))
    return keys.fetchone()


def get_table_columns(table, full=False):
    """
    Get list of the table column names.
    """
    cur = get_conn().execute('PRAGMA table_info("%s")' % table)
    if not full:
        return [row[1] for row in cur.fetchall()]
    else:
        return cur.fetchall()


def get_brief_columns(table, masks, negate=True):
    """
    Prepare list of columns for brief output.
    :param table: table name;
    :param masks: comma-separated list of column names and name masks.
    :param negate: if True then invert the list.
    """
    from fnmatch import filter
    col = get_table_columns(table)
    matched = []
    for mask in masks:
        matched.extend(filter(col, mask))
    if negate:
        result_set = set(col) - set(matched)
    else:
        result_set = set(matched)
    # Is this redundand???
    columns = get_conn().execute("""select column_name
      from reference_tables_columns
     where reference_table = '%s'
       and column_name in (%s)
       order by uid""" % (table, ','.join("'%s'" % c for c in result_set)))
    result = [row[0] for row in columns.fetchall()]
    return result


def format_value(value, xformat):
    """
    Format value with a given format.
    """
    if xformat is None or xformat == '':
        return str(value)
    elif value is None or str(value).strip() == 'None':
        return ''
    else:
        try:
            if re.search(r'\d*\.\d+[gef]', xformat) is not None:
                return ('%%%s' % xformat) % float(value)
            elif xformat[-1] in 'd':
                return ('%%%s' % xformat) % int(value)
            else:
                return ('%%%s' % xformat) % value
        except ValueError:
            # Wrongly formatted value will be returned as string
            return str(value)