#!/usr/bin/python
"""
Created on Thu Mar  5 17:06:56 2015
@author: mints
"""

from .globals import JINJA, get_conn, get_key_list
from .utils import quoted_list, quoted_list_item

def search():
    t = JINJA.get_template('search.template')
    conn = get_conn()
    cur = conn.cursor()
    keys = get_key_list(conn, any_subkey=True)
    tables = cur.execute('select table_name from reference_tables').fetchall()
    mocs = cur.execute('select moc_name, ifnull(description, moc_name) from mocs').fetchall()
    html_data = {'table_x': quoted_list_item(tables, 0),
                 'moc_names': quoted_list_item(mocs, 0),
                 'moc_descr': quoted_list_item(mocs, 1),
                 'key_x': quoted_list(keys)}
    return t.render(html_data)

