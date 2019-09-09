# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:07:16 2015
@author: minz

A script to fill in column metadata.
Use on your own risk.
Proper job is to be done by import script.
"""

import sys
from astropy.io import fits
from .globals import get_conn

COLUMN_FORMATS_FITS = {
    'J': 'integer',
    'I': 'integer',
    'L': 'boolean',
    'E': 'real',
    'D': 'real',
    'A': 'text'
}

table = sys.argv[1]
filename = sys.argv[2]

f = fits.open(filename)[1]
column_names = []

conn = get_conn()

for coldef in f.columns:
    print(coldef.name, coldef.unit, coldef.format)
    if coldef.unit is not None:
        unit = coldef.unit
    else:
        unit = ''
    if coldef.name.lower() in column_names:
        colname = '%s_' % coldef.name
    else:
        colname = coldef.name
    sql = """insert into reference_tables_columns 
             (reference_table, column_name, data_type, data_unit, output_format)
             values ('%s', '%s', '%s', '%s', '%s')""" % (
             table, colname, COLUMN_FORMATS_FITS[coldef.format[-1:]],
             unit, '%s')
    conn.execute(sql)
    column_names.append(colname.lower())
conn.commit()
conn.close()

