#!/usr/bin/python
"""
Created on Tue Dec 30 12:48:40 2014
@author: mints
"""
import sqlite3
import argparse

def drop_table(table_name):
    conn = sqlite3.connect('AIP_clusters.sqlite')
    conn.executescript("""
delete from data_references where reference_table = '{0}';
delete from reference_tables_keys where reference_table = '{0}';
delete from reference_tables_columns where reference_table = '{0}';
delete from reference_tables where table_name = '{0}';
delete from clusters where source = '{0}';
drop table {0}""".format(table_name))
    conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Delete all traces of the table from the database""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--table', type=str, default=None,
                        help='Table name')
    args = parser.parse_args()
    drop_table(args.table)
    print 'Done'