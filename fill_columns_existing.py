# -*- coding: utf-8 -*-
"""
Fill reference_tables_columns for an existing table.
WARNING! Data in reference_tables_columns for this table will be re-created.

Created on Sat Jan 24 12:07:16 2015

@author: minz
"""

import sys
from .globals import get_conn

table = sys.argv[1]
conn = get_conn()

data =  conn.execute("pragma table_info('%s')" % table).fetchall()
for coldef in data:
    unit = ''
    colname = coldef[1]
    format = coldef[2].split()[0]
    sql = """insert into reference_tables_columns
             (reference_table, column_name, data_type, data_unit, output_format)
             values ('%s', '%s', '%s', '%s', '%s')""" % (
             table, colname, format, unit, '%s')
    conn.execute(sql)
conn.commit()
conn.close()

