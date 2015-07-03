#!/usr/bin/python
"""
Created on Mon Dec  8 14:49:34 2014
@author: mints
Universal tool to import data into AIP Galaxy clusters database.
"""
import numpy as np
import argparse
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.extern.configobj.configobj import ConfigObj
from globals import get_conn
from astropy import units as u


def get_field_datatype(field):
    """
    Convert python type into VO type.
    """
    typename = field.dtype.name
    if typename.startswith('int'):
        return 'integer'
    elif typename.startswith('float'):
        return 'float'
    elif typename.startswith('string'):
        return 'text'
    else:
        return typename


def insert_clusters(conn, table_name, uid_column,
                    ra_column, dec_column, gal_l, gal_b):
    """
    Insert clusters that are really new into a "clusters" table.
    """
    if gal_l is not None and gal_b is not None:
        # We have information on the galactic coordinates in table already.
        gal_ls = ', gal_l, gal_b'
        gal_select = ', %s, %s' % (gal_l, gal_b)
        update_gal = False
    else:
        gal_ls = ''
        gal_select = ''
        update_gal = True
    conn.executescript("""
insert into clusters(ra, dec, source, source_id, dec_int {4})
select {2}, {3}, '{0}', {1}, cast({3} as int) {5}
  from [{0}] x
 where not exists (select 1
                     from data_references d
                    where d.reference_table = '{0}'
                      and d.reference_uid = x.{1});
insert into data_references (cluster_uid, reference_table, reference_uid)
select uid, '{0}', source_id
  from clusters c
 where source = '{0}';""".format(table_name, uid_column,
                                 ra_column, dec_column, gal_ls, gal_select))
    data = conn.execute("""select uid, ra, dec from clusters
                            where source = '%s'""" % table_name).fetchall()
    data = np.array(data)
    print 'Inserted %s new clusters' % len(data)
    if update_gal:
        print 'Updating galactic coordinates'
        sky = SkyCoord(data[:, 1], data[:, 2], frame='icrs', unit='deg')
        gal = sky.galactic
        #conn.commit() # Trying to speed things up
        for irow, uid in enumerate(data[:, 0]):
            conn.execute("""
              update clusters
                 set gal_l = %s, gal_b = %s
               where uid = %s""" % (gal[irow].l.deg, gal[irow].b.deg, uid))


def cross_match(conn, table, ra_column, dec_column, gal_l, gal_b,
                uid_column, table_name):
    """
    Do a cross-match and save all matched objects.
    """
    # Get a list of all known clusters
    data = conn.execute("select ra, dec, uid from clusters").fetchall()
    data = np.array(data)
    if len(data) > 0:
        # Match new clusters to known clusters
        smatch = SkyCoord(data[:, 0], data[:, 1], unit='deg')
        starget = SkyCoord(table[ra_column].data, table[dec_column].data,
                           unit='deg')
        matches = smatch.search_around_sky(starget, (1./60.)*u.deg)
        for match in xrange(len(matches[0])):
            # Save all found matches
            conn.execute("""
            insert into data_references
            (cluster_uid, reference_table, reference_uid)
            values (%s, '%s', %s)""" % (int(data[matches[1][match], 2]),
                                        table_name,
                                        table[uid_column].data[matches[0][match]]))
        print "Inserted %s references" % len(matches[0])


def create_key(table, key, reference, error_low, error_high, comment,
               comment_column):
    conn = get_conn()
    key, subkey = key.split(',')
    row = [key, subkey, table, reference, error_low, error_high,
           comment, comment_column]
    row = ["'%s'" % item if item is not None and item != ''
           else 'null' for item in row]
    conn.execute("""insert into reference_tables_keys (key, subkey,
    reference_table, reference_column, error_column_low, error_column_high,
    comment, comment_column)
    values (%s)""" % ','.join(row))
    conn.commit()
    if key in ['xid_flag', 'obs_flag']:
        cursor = conn.execute("""select uid_column from reference_tables
                                  where table_name = '%s'""" % table)
        update_flags(conn, key, table,
                     flag_column=reference,
                     flag_comment=comment_column,
                     uid_column=cursor.fetchone()[0])

def update_flags(conn, flag, table, flag_value=None,
                 flag_comment=None,
                 flag_column=None, uid_column=None):
    """
    Updating OBS or XID flags with new values.
    """
    if flag_value is not None:
        # Set fixed value, if it is larger than existing.
        conn.execute("""update clusters
                           set {flag} = {flag_value},
                               {flag}_source = '{table}',
                               {flag}_comment = '{comment}'
                         where source = '{table}';
                        update clusters
                           set {flag} = {flag_value}
                         where source != '{table}'
                           and exists (select 1
                                         from data_references d
                                        where d.cluster_uid = clusters.uid
                                          and d.reference_table = '{table}')
                           and {flag} < {flag_value}
                           """.format(flag=flag, flag_value=flag_value,
                                      table=table, comment=flag_comment))
    else:
        # Update by value in the table column.
        # Create a temp. table with new values:
        conn.executescript("""create table temp_flags(
                          uid integer null,
                          old_flag integer,
                          new_flag integer,
                          new_flag_comment text);
         insert into temp_flags(uid, new_flag, new_flag_comment)
         select d.cluster_uid, [{flag_column}], [{flag_comment}]
           from [{table}] x
           join data_references d on d.reference_uid = x.[{uid_column}]
          where d.reference_table = '{table}';
         update clusters
            set {flag} = (select new_flag from temp_flags t where t.uid = clusters.uid),
                {flag}_source = '{table}',
                {flag}_comment = (select new_flag_comment from temp_flags t where t.uid = clusters.uid)
          where exists (select new_flag from temp_flags t
                         where t.uid = clusters.uid
                           and t.new_flag > clusters.{flag});
         drop table temp_flags
         """.format(flag_column=flag_column, flag_comment=flag_comment,
                    table=table,
                    uid_column=uid_column, flag=flag))


def create_table(file_name, file_type, table_name, description,
                 uid_column, ra_column, dec_column,
                 brief_columns='*',
                 gal_l=None, gal_b=None,
                 delimiter=',',
                 reference_table=None,
                 reference_column=None,
                 xid_column=None,
                 xid_value=None,
                 xid_comment=None,
                 obs_column=None,
                 obs_value=None,
                 obs_comment=None):
    # Import data first:
    if file_type is not None and file_type in ['ascii', 'ascii.csv']:
        table = Table.read(file_name, format=file_type, delimiter=delimiter)
    elif file_type is not None:
        table = Table.read(file_name, format=file_type)
    else:
        table = Table.read(file_name)

    if table_name is not None:
        table.meta['table_name'] = '[%s]' % table_name
    colnames = []
    tnames = table.colnames
    for t in tnames:
        if t.lower() in colnames:
            table.rename_column(t, '%s_' % t)
        colnames.append(t.lower())
    table.write('AIP_clusters.sqlite', format='sql', dbtype='sqlite')
    print 'Table %s created' % table_name
    # Now proceed metadata:
    conn = get_conn()
    conn.execute("""create unique index idx_{0}_uid
                                     on [{0}]({1})""".format(table_name,
                                                             uid_column))
    conn.execute("insert into reference_tables(table_name, uid_column, "
                 "description, ra_column, dec_column, "
                 "brief_columns, obs_class_global, obs_class_value)"
                 "values ('%s', '%s', '%s', '%s', '%s', "
                 "'%s', 'true', 0)" % (table_name, uid_column,
                                      description, ra_column, dec_column,
                                      brief_columns))
    for colname in table.columns.keys():
        column = table.columns[colname]
        form = column.format[1:] if column.format is not None else 's'
        if 'ucd' in column.meta:
            ucd = column.meta['ucd']
        else:
            ucd = ''
        sql = """insert into reference_tables_columns
                 (reference_table, column_name, data_type,
                 data_unit, output_format, ucd)
                 values ('%s', '%s', '%s', '%s', '%s', '%s')""" % (
                 table_name, column.name, get_field_datatype(column),
                 column.unit, form, ucd)
        conn.execute(sql)

    if reference_table is None:
        cross_match(conn, table, ra_column, dec_column, gal_l, gal_b,
                    uid_column, table_name)
    else:
        # Add references:
        rt_uid = conn.execute("""select uid_column
                                  from reference_tables
                                 where table_name = '%s'""" % reference_table)
        rt_uid = rt_uid.fetchone()[0]
        sql = """
        insert into data_references
        (cluster_uid, reference_table, reference_uid)
        select c.uid, '{0}', {4}
          from clusters c
          join data_references d on c.uid = d.cluster_uid
                                and d.reference_table = '{1}'
          join [{1}] r on d.reference_uid = r.{2}
          join [{0}] x on x.{3} = r.{3}""".format(table_name,
                                                  reference_table,
                                                  rt_uid,
                                                  reference_column,
                                                  uid_column)
        print sql
        conn.execute(sql)

    insert_clusters(conn, table_name, uid_column, ra_column, dec_column,
                    gal_l, gal_b)
    if xid_value is not None:
        update_flags(conn, 'xid_flag', table,
                     flag_value=xid_value,
                     flag_comment=xid_comment,
                     uid_column=uid_column)
    if obs_value is not None:
        update_flags(conn, 'obs_flag', table,
                     flag_value=obs_value,
                     flag_comment=obs_comment,
                     uid_column=uid_column)
    conn.commit()
    print 'Done'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Tool to import whole file-table into the database""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--file', type=str, default=None,
                        help='input filename')

    parser.add_argument('-C', '--config', type=str, default=None,
                        help='config filename')

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

    parser.add_argument('-D', '--description', type=str, default=None,
                        help='Table description')

    args = parser.parse_args()
    if args.config is None:
        create_table(args.file, args.type, args.table, args.description,
                     args.uid, args.ra, args.dec,
                     delimiter=args.delimiter)
    else:
        config = ConfigObj(args.config)
        main = config['main']
        params = {}
        for par in ['file_name', 'file_type', 'table_name', 'description',
                    'uid_column', 'ra_column', 'dec_column', 'gal_l', 'gal_b',
                    'brief_columns',
                    'reference_table', 'reference_column',
                    'xid_value', 'xid_comment',
                    'obs_value', 'obs_comment',
                    ]:
            if par in main:
                params[par] = main[par]
        if 'brief_columns' in params:
            params['brief_columns'] = ','.join(params['brief_columns'])
        for key in params.keys():
            if params[key] == '':
                params[key] = None
        create_table(**params)
        for key in config['keys'].sections:
            key_s = config['keys'][key]
            key_par = {par: key_s[par] if par in key_s else None for par in ['reference', 'error_low',
                                                                        'error_high', 'comment',
                                                                        'comment_column']}
            key_par['table'] = main['table_name']
            key_par['key'] = key_s.name
            create_key(**key_par)

