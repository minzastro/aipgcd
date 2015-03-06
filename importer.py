#!/usr/bin/python
"""
Created on Mon Dec  8 14:49:34 2014
@author: mints
Universal tool to import data into AIP Galaxy clusters database.
"""

import argparse
from pysqlite2 import dbapi2 as sqlite3
from astropy.table import Table


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

def create_table(file_name, file_type, table_name, description,
                 uid_column, is_string_uid,
                 ra_column, dec_column, delimiter=','):
    # Import data first:
    table = Table()
    if file_type is not None:
        table.read(file_name, format=file_type, delimiter=delimiter)
    else:
        table.read(file_name)

    if table_name is not None:
        table.table_name = table_name
    colnames = []
    for t in table.columns:
        if t.lower() in colnames:
            table.rename_column(t, '%s_' % t)
        colnames.append(t.lower())
    table.write('sqlite', 'AIP_clusters.sqlite')

    # Now proceeith metadata:
    conn = sqlite3.connect('AIP_clusters.sqlite')
    conn.enable_load_extension(True)
    conn.execute("select load_extension('/home/mints/prog/AIP_clusters/sqlite_extentions/libsqlitefunctions.so')")
    conn.enable_load_extension(False)
    conn.execute("insert into reference_tables(table_name, uid_column, "
                 "is_string_uid, description, ra_column, dec_column)"
                 "values ('%s', '%s', %s, '%s', '%s', '%s')" % (
                 table_name, uid_column, int(is_string_uid),
                 description, ra_column, dec_column))
    for column in table.columns:
        form = column.format[1:] if column.format is not None else 's'
        if 'ucd' in column.meta:
            ucd = column.meta['ucd']
        else:
            ucd = ''
        sql = """insert into reference_tables_columns
                 (reference_table, column_name, data_type, data_unit, output_format, ucd)
                 values ('%s', '%s', '%s', '%s', '%s')""" % (
                 table, column.name, get_field_datatype(column), column.unit,
                 form, ucd)
        conn.execute(sql)

    conn.execute("""
insert into data_references (cluster_uid, reference_table, reference_uid)
select c.uid, '{0}', x.{1}
  from clusters c, {0} x
 where c.dec_int >= cast(x.{3} as int) - 1
   and c.dec_int <= cast(x.{3} as int) + 1
   and haversine(c.ra, c.dec, x.{2}, x.{3}) < 1./60.""".format(table_name,
                                                           uid_column,
                                                           ra_column,
                                                           dec_column))
    conn.execute("""
insert into clusters(ra, dec, source, source_id, dec_int)
select {2}, {3}, '{0}', {1}, cast({2} as int)
  from {0} x
 where not exists (select 1
                     from data_references d
                    where d.reference_table = '{0}'
                      and d.reference_uid = x.{1})""".format(table_name,
                                                             uid_column,
                                                             ra_column,
                                                             dec_column))
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