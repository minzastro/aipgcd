#!/usr/bin/python
"""
Created on Mon Dec  8 15:51:22 2014
@author: mints
"""
from AIP_clusters.prettiesttable import from_db_cursor
#from prettytable import from_db_cursor
from AIP_clusters.globals import get_conn, JINJA, get_brief_columns


def single_cluster(uid):
    t = JINJA.get_template('single_cluster.template')
    CONN = get_conn()
    cur = CONN.cursor()
    html_data = {}
    html_data['uid'] = uid
    result = CONN.execute("select source, source_id "
                          "from clusters where uid = %s" % uid).fetchone()
    html_data['source'] = result[0]
    html_data['source_id'] = result[1]

    html_data['params'] = []
    html_data['tables'] = []
    for row in cur.execute("""select rt.table_name,
                                     rt.uid_column, rt.is_string_uid,
                                     rt.extra_column, rt.description,
                                     rt.brief_columns
                                from reference_tables rt"""):
        t1 = from_db_cursor(CONN.execute("""
            select x.*
              from %s x
              join data_references r on r.reference_uid = [%s]
                                    and r.reference_table = '%s'
             where r.cluster_uid = %s""" % (row[0], row[1], row[0], uid)))
        t1.border = True
        t1.float_format = '.3e'
        if len(t1._rows) > 0:
            print row[0], row[5]
            html_data['tables'].append({
                'title': row[4],
                'id': row[0],
                'briefcols': ','.join(get_brief_columns(row[0], [row[5]])),
                'html': t1.get_html_string(attributes={'border': 1,
                                                       'id': row[0]})})
        for key in CONN.cursor().execute("""select kr.reference_column, kr.is_string,
                                         kr.error_column_high, kr.error_column_low,
                                         k.key, k.key_class, k.description,
                                         k.data_format
                                    from key_referencer kr
                                    join keys k on k.key = kr.key
                                               and ifnull(k.key_class, 'null') = ifnull(kr.key_class, 'null')
                                   where reference_table = '%s'
                                   order by k.key, k.key_class""" % row[0]):
            values = CONN.cursor().execute("""select [%s]
                       from %s x
                       join data_references r on r.reference_uid = [%s]
                      where r.cluster_uid = %s""" % (key[0], row[0], row[1], uid)).fetchall()
            if len(values) > 0:
                par = {'name': key[4],
                       'desc': key[6],
                       'value': values[0][0],
                       'err_low': 0.0,
                       'err_high': 0.0,
                       'source': row[0]}
                html_data['params'].append(par)

    return t.render(html_data)
