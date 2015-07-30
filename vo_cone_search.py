# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettiesttable import from_db_cursor
from globals import get_conn, JINJA
from utils import dict_values_to_list
from astropy.coordinates import SkyCoord
from astropy import units as u

def build_key_constraint(conn, key, subkey_cond, condition):
    """
    Create an advanced constraint on the key/subkey pair.
    Might involve inequalities on the key value.
    Example:
      constraint = build_key_constraint(conn, 'z', 'subkey is null',
                                        '> 0.5')
    """
    cur = conn.cursor()
    tables = cur.execute("""select reference_table, reference_column, uid_column
                              from reference_tables_keys k
                              join reference_tables t  on t.table_name = k.reference_table
                             where key = '%s'
                               and %s""" % (key, subkey_cond)).fetchall()
    conditions = []
    for table in tables:
        cond = """exists (select 1 from data_references dr
                            join [%s] x on dr.reference_uid = x.[%s]
                           where dr.cluster_uid = c.uid
                             and dr.reference_table = '%s'x
                             and x.[%s] %s)""" % (table[0], table[2],
                                                  table[0], table[1], condition)
        conditions.append(cond)
    return 'and (%s)' % ' or '.join(conditions)


def vo_cone_search(args):
    """
    Performs a cluster search request.
    Possible args keys are:
        ra, decl - cone center in degrees;
        radius - cone radius in arcmin;
        fullsky - perform full-sky search. Cone constraints are ignored;
        in_table - name of the table or list of table names,
                   constraint will be set on cluster presence/
                   absence in this table(s);
        has_record - list of 'exists' or 'not exists' strings,
                     one for each value in in_table;
        condition \
        in_key    |
        constraint|
        expression/
        in_moc - name of MOC or list of MOCs,
                 constraint will be set on cluster entering/
                 not entering the MOC area;
        has_moc - list of 'exists' or 'not exists' strings,
                  one for each value in in_moc;
    """
    conn = get_conn()
    conditions = []
    if 'fullsky' not in args:
        ra = args['ra']
        decl = args['decl']
        if ':' in ra or ':' in decl:
            coord = SkyCoord(ra, decl, unit=(u.hourangle, u.deg))
        elif 'h' in ra:
            coord = SkyCoord(ra, decl, unit=(u.hourangle, u.deg))
        elif '.' in ra:
            coord = SkyCoord(ra, decl, unit='deg')
        else:
            coord = SkyCoord(ra, decl, unit=(u.hourangle, u.deg))
        ra = coord.ra.deg
        decl = coord.dec.deg
        radius = args['radius']
        conditions.append("""
        and haversine(c.ra, c.dec, {0}, {1}) < {2}/60.""".format(ra, decl,
                                                              radius))
        extra_columns = """ haversine(c.ra, c.dec, {0}, {1})
                            as "_r (arcmin)", """.format(ra, decl, radius)
    else:
        extra_columns = ''
    if 'in_table' in args:
        if isinstance(args['in_table'], basestring):
            conditions.append("""and %s (select 1
                                       from data_references dr
                                      where dr.cluster_uid = c.uid
                                        and dr.reference_table = '%s')""" % (
                                        args['has_record'], args['in_table']))
        else:
            for itable, table in enumerate(args['in_table']):
                conditions.append("""and %s (select 1
                                           from data_references dr
                                          where dr.cluster_uid = c.uid
                                            and dr.reference_table = '%s')""" % (
                                            args['has_record'][itable], table))

    if 'condition' in args:
        extra_counter = 0
        args =  dict_values_to_list(args, ['condition', 'in_key',
                                           'constraint', 'expression'])
        for icondition, condition in enumerate(args['condition']):
            if ',' in args['in_key'][icondition]:
                key, subkey = args['in_key'][icondition].split(',')
                if subkey != 'all subkeys':
                    subkey_cond = "k.subkey ='%s'" % subkey
                else:
                    subkey_cond = '1=1'
            else:
                key = args['in_key'][icondition]
                subkey_cond = 'k.subkey is null'
            if condition != 'extra':
                conditions.append("""and %s (select 1
                                       from reference_tables_keys k
                                       join data_references dr on dr.reference_table = k.reference_table
                                      where dr.cluster_uid = c.uid
                                        and key = '%s'
                                        and %s)""" % (condition, key, subkey_cond))
            else:
                expr = '%s %s' % (args['constraint'][extra_counter],
                                  args['expression'][extra_counter])
                conditions.append(build_key_constraint(conn, key, subkey_cond,
                                                       expr))
                extra_counter = extra_counter + 1
    if 'has_moc' in args:
        args = dict_values_to_list(args, ['has_moc', 'in_moc'])
        for cond, moc in zip(args['has_moc'], args['in_moc']):
            conditions.append(""" and %s (select 1
                                            from cluster_in_moc m
                                           where m.uid = c.uid
                                             and m.moc_name = '%s')
                                             """ % (cond, moc))
    if 'flag_name' in args:
        args = dict_values_to_list(args, ['flag_name', 'flag_constraint',
                                          'xid_values', 'obs_values'])
        for iflag, flag in enumerate(args['flag_name']):
            if flag == 'obs_flag':
                value = args['obs_values'][iflag]
            else:
                value = args['xid_values'][iflag]
            conditions.append("""
                and %s %s %s""" % (flag, args['flag_constraint'][iflag], value))
    t = JINJA.get_template('vo_cone_search.template')

    sql = """select c.uid, %s ra, dec, c.source, source_id, xid_flag, obs_flag,
                    group_concat(distinct r.reference_table) as Tables
               from clusters c
               join data_references r on r.cluster_uid = c.uid
              where 1=1
                %s
              group by c.uid, ra, dec, c.source, source_id
              order by c.ra""" % (extra_columns, ' '.join(conditions))
    print sql
    t1 = from_db_cursor(conn.execute(sql))
    t1.float_format['ra'] = '.5f'
    t1.float_format['dec'] = '.5f'
    html_data = {'table': t1.get_html_string(attributes={'border': 1,
                                                         'id': 'search',
                                                         'columns': 'IFFSIIIS'},
                                             unescape=[('Tables')])}
    return t.render(html_data)
