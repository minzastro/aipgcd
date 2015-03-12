#!/usr/bin/python
"""
Created on Mon Dec  8 14:49:34 2014
@author: mints
Universal tool to import data into AIP Galaxy clusters database.
"""

import argparse
from pysqlite2 import dbapi2 as sqlite3
from astropy.table import Table
import numpy as np
#from atpy import Table
from astropy.coordinates import SkyCoord
from AIP_clusters.globals import get_conn

def get_field_datatype(field):
    typename = field.dtype.name
    if typename.startswith('int'):
        return 'integer'
    elif typename.startswith('float'):
        return 'float'
    elif typename.startswith('string'):
        return 'text'
    else:
        return typename

def insert_clusters(conn, table_name, uid_column, ra_column, dec_column):
    conn.execute("""
insert into clusters(ra, dec, source, source_id, dec_int)
select {2}, {3}, '{0}', {1}, cast({3} as int)
  from {0} x
 where not exists (select 1
                     from data_references d
                    where d.reference_table = '{0}'
                      and d.reference_uid = x.{1})""".format(table_name,
                                                             uid_column,
                                                             ra_column,
                                                             dec_column))
    data = conn.execute("""select uid, ra, dec from clusters
                            where source = '%s'""" % table_name).fetchall()
    data = np.array(data)                            
    sky = SkyCoord(data[:, 1], data[:, 2], frame='icrs', unit='deg')
    gal = sky.galactic        
    for irow, uid in enumerate(data[:, 0]):
        conn.execute("""
          update clusters
             set gal_l = %s, gal_b = %s
           where uid = %s""" % (gal[irow].l.deg, gal[irow].b.deg, uid))

def create_table(file_name, file_type, table_name, description,
                 uid_column, is_string_uid,
                 ra_column, dec_column, delimiter=','):
    # Import data first:
    if file_type is not None and file_type in ['ascii', 'ascii.csv']:
        table = Table.read(file_name, format=file_type, delimiter=delimiter)
    elif file_type is not None:
        table = Table.read(file_name, format=file_type)
    else:
        table = Table.read(file_name)

    if table_name is not None:
        table.meta['table_name'] = table_name
    colnames = []
    #import ipdb; ipdb.set_trace()
    tnames = table.colnames
    for t in tnames:
        if t.lower() in colnames:
            table.rename_column(t, '%s_' % t)
        colnames.append(t.lower())
    table.write('AIP_clusters.sqlite', format='sql', dbtype='sqlite')

    # Now proceed metadata:
    conn = get_conn()
    conn.execute("insert into reference_tables(table_name, uid_column, "
                 "is_string_uid, description, ra_column, dec_column, "
                 "brief_columns, obs_class_global, obs_class_value)"
                 "values ('%s', '%s', %s, '%s', '%s', '%s', "
                 "'*', 'true', 0)" % (
                 table_name, uid_column, int(is_string_uid),
                 description, ra_column, dec_column))
    for colname in table.columns.keys():
        column = table.columns[colname]
        form = column.format[1:] if column.format is not None else 's'
        if 'ucd' in column.meta:
            ucd = column.meta['ucd']
        else:
            ucd = ''
        sql = """insert into reference_tables_columns
                 (reference_table, column_name, data_type, data_unit, output_format, ucd)
                 values ('%s', '%s', '%s', '%s', '%s', '%s')""" % (
                 table_name, column.name, get_field_datatype(column), column.unit,
                 form, ucd)
        conn.execute(sql)

    insert_clusters(conn, table_name, uid_column, ra_column, dec_column)
    conn.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Tool to import whole file-table into the database""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--file', type=str, default=None,
                        help='input filename')

    parser.add_argument('-d', '--delimiter', type=str, default=',',
                        help='Field delimiter for ascii file')

    parser.add_argument('-T', '--type', type=str, default=None,
                        help='File type')

    parser.add_argument('-t', '--table', type=str, default=None,
                        help='Database table name')

    parser.add_argument('-ra', '--ra', type=str, default=None,
                        help='RA column name')

    parser.add_argument('-de', '--dec', type=str, default=None,
                        help='DE column name')

    parser.add_argument('-u', '--uid', type=str, default=None,
                        help='UID column name')

    parser.add_argument('--string_uid', action="store_true",
                        default=False,
                        help='UID column is a string')

    parser.add_argument('-D', '--description', type=str, default=None,
                        help='Table description')

    args = parser.parse_args()

    create_table(args.file, args.type, args.table, args.description,
                 args.uid, args.string_uid, args.ra, args.dec, args.delimiter)