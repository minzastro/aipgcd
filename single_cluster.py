#!/usr/bin/python
"""
Created on Mon Dec  8 15:51:22 2014
@author: mints
"""
from AIP_clusters.prettiesttable import from_db_cursor, PrettiestTable
from AIP_clusters.globals import get_conn, JINJA, get_brief_columns, format_value

def single_cluster_update_comment(uid, comment):
    CONN = get_conn()
    xcomment = comment.replace("'", "''")
    CONN.execute("update clusters set comment = '%s' where uid = %s" % (
        xcomment, uid))
    CONN.commit()
    return None

def single_cluster_update_xid(uid, xid):
    CONN = get_conn()
    CONN.execute("update clusters set xidflag = %s where uid = %s" % (
        xid, uid))
    CONN.commit()
    return None

def single_cluster(uid):
    t = JINJA.get_template('single_cluster.template')
    CONN = get_conn()
    cur = CONN.cursor()
    html_data = {}
    html_data['uid'] = uid
    result = CONN.execute("select source, source_id, comment, xidflag "
                          "from clusters where uid = %s" % uid).fetchone()
    html_data['source'] = result[0]
    html_data['source_id'] = result[1]
    html_data['comment'] = result[2]
    html_data['xid'] = result[3]

    html_data['params'] = []
    html_data['tables'] = []
    for row in cur.execute("""select rt.table_name,
                                     rt.uid_column, rt.is_string_uid,
                                     rt.extra_column, rt.description,
                                     rt.brief_columns
                                from reference_tables rt"""):
        column_list = get_brief_columns(row[0], row[5].split(','), negate=False)
        t1 = from_db_cursor(CONN.execute("""
            select %s
              from %s x
              join data_references r on r.reference_uid = [%s]
                                    and r.reference_table = '%s'
             where r.cluster_uid = %s""" % (','.join(['x.[%s]' % x for x in column_list]),
                                            row[0], row[1], row[0], uid)))
        t1.border = True
        t1.float_format = '.3e'
        for column_properties in CONN.execute("""
        select column_name, output_format, description, data_unit, lower(data_type)
          from reference_tables_columns
         where reference_table = '%s'""" % row[0]).fetchall():
             if column_properties[4] == 'integer':
                 t1.int_format[column_properties[0]] = column_properties[1]
             elif column_properties[4] == 'real' or column_properties[4] == 'double':
                 t1.float_format[column_properties[0]] = column_properties[1]
        cursor = CONN.execute("""
            select x.*
              from %s x
              join data_references r on r.reference_uid = [%s]
                                    and r.reference_table = '%s'
             where r.cluster_uid = %s""" % (row[0], row[1], row[0], uid))
        full_table = PrettiestTable()
        full_table.add_column('Parameter', [item[0] for item in cursor.description])
        for irow, arow in enumerate(cursor.fetchall()):
            full_table.add_column(str(irow), arow)

        if len(t1._rows) > 0:
            html_data['tables'].append({
                'title': row[4],
                'id': row[0],
                'full_table': full_table.get_html_string(attributes={'border': 1}),
                'html': t1.get_html_string(attributes={'border': 1,
                                                       'id': row[0]})})
            for key in CONN.cursor().execute("""
                    select kr.reference_column, kr.is_string,
                           kr.error_column_low, kr.error_column_high,
                           k.key, k.key_class, k.description,
                           ifnull(k.data_format, rc.output_format)
                      from reference_tables_keys kr
                      join keys k on k.key = kr.key
                                 and ifnull(k.key_class, 'null') = ifnull(kr.key_class, 'null')
                      join reference_tables_columns rc on kr.reference_table = rc.reference_table
                                                      and kr.reference_column = rc.column_name
                     where kr.reference_table = '%s'
                  order by k.key, k.key_class""" % row[0]):
                select = 'x.[%s]' % key[0]
                if key[2] is not None:
                    select = '%s, x.[%s]' % (select, key[2])
                if key[3] is not None:
                    select = '%s, x.[%s]' % (select, key[3])
                values = CONN.cursor().execute("""select %s
                           from %s x
                           join data_references r on r.reference_uid = [%s]
                          where r.cluster_uid = %s
                            and r.reference_table = '%s'""" % (select, row[0],
                                                             row[1], uid,
                                                             row[0])).fetchall()
                if len(values) > 0:
                    par = {'name': key[4],
                           'desc': key[6],
                           'value': format_value(values[0][0], key[7]),
                           'source': row[0]}
                    if key[2] is not None:
                        par['err_low'] = format_value(values[0][1], key[7])
                    if key[3] is not None:
                        par['err_high'] = format_value(values[0][2], key[7])
                    html_data['params'].append(par)

    return t.render(html_data)
