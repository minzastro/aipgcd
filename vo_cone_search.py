# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from AIP_clusters.prettiesttable import from_db_cursor
from AIP_clusters.globals import get_conn, JINJA

def vo_cone_search(args):
    """
    Perform a cone-search.
    ra, decl in degrees,
    radius in arcmin.
    """
    ra = args['ra']
    decl = args['decl']
    radius = args['radius']
    conditions = []
    if 'table' in args and args['table'] == 'on':
        conditions.append("""and %s (select 1
                                   from data_references dr
                                  where dr.cluster_uid = c.uid
                                    and dr.reference_table = '%s')""" % (
                                    args['has_record'], args['in_table']))
    conn = get_conn()
    t = JINJA.get_template('vo_cone_search.template')
    print """
select c.uid, ra, dec, c.source, source_id, group_concat(distinct r.reference_table) as Tables
  from clusters c
  join data_references r on r.cluster_uid = c.uid
 where haversine(c.ra, c.dec, {0}, {1}) < {2}./60.
   {3}
 group by c.uid, ra, dec, c.source, source_id
 order by c.ra""".format(ra, decl, radius, ' '.join(conditions))
    t1 = from_db_cursor(conn.execute("""
select c.uid, ra, dec, c.source, source_id, group_concat(distinct r.reference_table) as Tables
  from clusters c
  join data_references r on r.cluster_uid = c.uid
 where haversine(c.ra, c.dec, {0}, {1}) < {2}./60.
   {3}
 group by c.uid, ra, dec, c.source, source_id
 order by c.ra""".format(ra, decl, radius, ' '.join(conditions))))
    html_data = {'table': t1.get_html_string(attributes={'border': 1, 'id': 'search'},
                                             unescape=[('Tables')])}
    return t.render(html_data)
