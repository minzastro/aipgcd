#!/usr/bin/python
"""
Created on Thu Mar  5 17:06:56 2015
@author: mints
"""

from AIP_clusters.globals import JINJA, get_conn

def search():
    t = JINJA.get_template('search.template')
    conn = get_conn()
    cur = conn.cursor()
    tables = cur.execute('select table_name from reference_tables').fetchall()
    html_data = {'table_list': [table[0] for table in tables]}
    return t.render(html_data)

