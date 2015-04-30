#!/usr/bin/python
"""
Created on Thu Mar  5 17:06:56 2015
@author: mints
"""

from globals import JINJA, get_conn, get_key_list

def search():
    t = JINJA.get_template('search.template')
    conn = get_conn()
    cur = conn.cursor()
    keys = get_key_list(conn, any_subkey=True)
    tables = cur.execute('select table_name from reference_tables').fetchall()
    html_data = {'table_x': ','.join(["'%s'" % table[0] for table in tables]),
                 'key_x': ','.join(["'%s'" % key for key in keys])}
    return t.render(html_data)

