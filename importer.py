#!/usr/bin/python
"""
Created on Mon Dec  8 14:49:34 2014
@author: mints
"""

import atpy
import argparse

parser = argparse.ArgumentParser(
    description="""Tool to import whole file-table into the database""",
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-f', '--file', type=str, default=None,
                    help='input filename')

parser.add_argument('-t', '--table', type=str, default=None,
                    help='Database table name')

args = parser.parse_args()


table_file = args.file
table = atpy.Table()
table.read(table_file)

if args.table is not None:
    table.table_name = args.table

colnames = []
for t in table.columns:
    if t.lower() in colnames:
        table.rename_column(t, '%s_' % t)
    colnames.append(t.lower())

print table.columns
table.write('sqlite', 'AIP_clusters.sqlite')
