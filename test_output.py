#!/usr/bin/python
"""
Created on Mon Dec  8 15:51:22 2014
@author: mints
"""

import sqlite3
import sys
from prettytable import from_db_cursor
from prettytable import PrettyTable

conn = sqlite3.connect('AIP_clusters.sqlite')

cur = conn.cursor()

uid = sys.argv[1]

print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<link rel=stylesheet href='style.css' type='text/css'>
<head>
    <title>AIP Cluster Database</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>
<body>
"""
tk = PrettyTable(['Key', 'Key2', 'Description', 'Value'])
tk.border = True
for row in cur.execute("""select dr.reference_table, dr.reference_uid,
                                 rt.uid_column, rt.is_string_uid, rt.extra_column
                            from data_references dr
                            join reference_tables rt on rt.table_name = dr.reference_table
                           where cluster_uid = %s""" % uid):
    print "<h1>%s</h1>" % row[0]
    #import ipdb; ipdb.set_trace()
    for key in conn.cursor().execute("""select kr.reference_column, kr.is_string,
                                     kr.error_column_high, kr.error_column_low,
                                     k.key, k.key_class, k.description,
                                     k.data_format
                                from key_referencer kr
                                join keys k on k.key = kr.key and ifnull(k.key_class, 'null') = ifnull(kr.key_class, 'null')
                               where reference_table = '%s'
                               order by k.key, k.key_class""" % row[0]):
        tk.add_row([key[4], key[5], key[6], conn.cursor().execute("""select %s from %s where %s = %s""" %(
                             key[0], row[0], row[2], row[1])).fetchall()[0][0]])
    t1 = from_db_cursor(conn.execute("""select * from %s where %s = %s""" % (row[0], row[2], row[1])))
    t1.border = True
    t1.float_format = '.3e'
    print t1.get_html_string(attributes={'border': 1})
    #print conn.cursor().execute("""select * from %s where %s = %s""" % (row[0], row[2], row[1])).fetchall()
print tk.get_html_string()

print "</body></html>"