# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettiesttable import from_db_cursor
from globals import get_conn, JINJA
from astropy.coordinates import SkyCoord
from astropy import units as u

def build_key_constraint(conn, key, subkey_cond, condition):
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
    Perform a cone-search.
    ra, decl in degrees,
    radius in arcmin.
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
        for valid in ['condition', 'in_key', 'constraint', 'expression']:
            if valid in args:
                if isinstance(args[valid], basestring):
                    args[valid] = [args[valid]]
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
        for valid in ['has_moc', 'in_moc']:
            if isinstance(args[valid], basestring):
                args[valid] = [args[valid]]
        for cond, moc in zip(args['has_moc'], args['in_moc']):
            conditions.append(""" and %s (select 1
                                            from cluster_in_moc m
                                           where m.uid = c.uid
                                             and m.moc_name = '%s')
                                             """ % (cond, moc))
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
