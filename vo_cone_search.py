# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettytable import from_db_cursor
from AIP_clusters.globals import get_conn, JINJA

def vo_cone_search(ra, decl, radius):
    """
    Perform a cone-search.
    ra, decl in degrees,
    radius in arcmin.
    """
    conn = get_conn()
    t = JINJA.get_template('vo_cone_search.template')
    t1 = from_db_cursor(conn.execute("""
select c.uid, ra, dec, c.source, source_id, group_concat(distinct r.reference_table) as Tables,
       '<a href="single?uid='||c.uid||'">link</a>' as link
  from clusters c
  join data_references r on r.cluster_uid = c.uid
 where haversine(c.ra, c.dec, {0}, {1}) < {2}./60.
 group by c.uid, ra, dec, c.source, source_id, link
 order by c.ra""".format(ra, decl, radius)))
    html_data = {'table': t1.get_html_string(attributes={'border': 1, 'id': 'search'},
                                             unescape=('Tables', 'link'))}
    return t.render(html_data)
