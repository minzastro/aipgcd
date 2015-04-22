# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettiesttable import from_db_cursor
from globals import get_conn, JINJA
from astropy.coordinates import SkyCoord
from astropy import units as u

def vo_cone_search(args):
    """
    Perform a cone-search.
    ra, decl in degrees,
    radius in arcmin.
    """
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
        and haversine(c.ra, c.dec, {0}, {1}) < {2}./60.""".format(ra, decl,
                                                              radius))
    if 'table' in args and args['table'] == 'on':
        conditions.append("""and %s (select 1
                                   from data_references dr
                                  where dr.cluster_uid = c.uid
                                    and dr.reference_table = '%s')""" % (
                                    args['has_record'], args['in_table']))
    if 'key' in args and args['key'] == 'on':
        if ',' in args['key_list']:
            key, subkey = args['key_list'].split(',')
            subkey_cond = "k.subkey ='%s'" % subkey
        else:
            key = args['key_list']
            subkey_cond = 'k.subkey is null'
        conditions.append("""and %s (select 1
                                       from reference_tables_keys k
                                       join data_references dr on dr.reference_table = k.reference_table
                                      where dr.cluster_uid = c.uid
                                        and key = '%s'
                                        and %s)""" % (args['has_key'], key, subkey_cond))
    conn = get_conn()
    t = JINJA.get_template('vo_cone_search.template')

    sql = """select c.uid, ra, dec, c.source, source_id,
                    group_concat(distinct r.reference_table) as Tables
               from clusters c
               join data_references r on r.cluster_uid = c.uid
              where 1=1
                %s
              group by c.uid, ra, dec, c.source, source_id
              order by c.ra""" % ' '.join(conditions)
    #print sql
    t1 = from_db_cursor(conn.execute(sql))
    html_data = {'table': t1.get_html_string(attributes={'border': 1,
                                                         'id': 'search',
                                                         'columns': 'IFFSIS'},
                                             unescape=[('Tables')])}
    return t.render(html_data)
