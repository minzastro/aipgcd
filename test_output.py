#!/usr/bin/python
"""
Created on Mon Dec  8 15:51:22 2014
@author: mints
"""

import sqlite3
import sys
from prettytable import from_db_cursor
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('AIP_clusters', '.'))
t = env.get_template('cluster.template')

conn = sqlite3.connect('AIP_clusters.sqlite')

cur = conn.cursor()

uid = sys.argv[1]

html_data = {}
html_data['uid'] = uid
html_data['source'] = 'Unknown'
html_data['source_id'] = 'Unknown'

html_data['params'] = []
html_data['tables'] = []
for row in cur.execute("""select rt.table_name,
                                 rt.uid_column, rt.is_string_uid, rt.extra_column,
                                 rt.description
                            from reference_tables rt"""):
    t1 = from_db_cursor(conn.execute("""select x.*
               from %s x
               join data_references r on r.reference_uid = [%s]
               where r.cluster_uid = %s""" % (row[0], row[1], uid)))
    t1.border = True
    t1.float_format = '.3e'
    if len(t1._rows) > 0:
        html_data['tables'].append({
            'title': row[4],
            'html': t1.get_html_string(attributes={'border': 1})})
    for key in conn.cursor().execute("""select kr.reference_column, kr.is_string,
                                     kr.error_column_high, kr.error_column_low,
                                     k.key, k.key_class, k.description,
                                     k.data_format
                                from key_referencer kr
                                join keys k on k.key = kr.key and ifnull(k.key_class, 'null') = ifnull(kr.key_class, 'null')
                               where reference_table = '%s'
                               order by k.key, k.key_class""" % row[0]):
        values = conn.cursor().execute("""select [%s]
                   from %s x
                   join data_references r on r.reference_uid = [%s]
                  where r.cluster_uid = %s""" % (key[0], row[0], row[1], uid)).fetchall()
        if len(values) > 0:
            par = {'name': key[4],
                   'desc': key[6],
                   'value': values[0][0],
                   'err_low': 0.0,
                   'err_high': 0.0,
                   'source': row[0]}
            html_data['params'].append(par)

html_file = open(sys.argv[2], 'w')
html_file.write(t.render(html_data))
html_file.close()
