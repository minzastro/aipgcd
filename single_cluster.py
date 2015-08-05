#!/usr/bin/python
"""
Created on Mon Dec  8 15:51:22 2014
@author: mints
"""
from prettiesttable import from_db_cursor, PrettiestTable
from globals import get_conn, JINJA, get_brief_columns, format_value
from globals import get_key_list
from utils import key_subkey_cond
from urllib import urlencode

def single_cluster_update_comment(uid, comment):
    """
    Updates comment for a cluster.
    """
    CONN = get_conn()
    xcomment = comment.replace("'", "''")
    CONN.execute("update clusters set comment = '%s' where uid = %s" % (
        xcomment, uid))
    CONN.commit()
    return None


def single_cluster_update_xid_flag(uid, xid_flag, xid_flag_source,
                                   xid_flag_comment):
    """
    Updates xid status for a cluster.
    """
    CONN = get_conn()
    CONN.execute("""update clusters
                       set xid_flag = %s,
                           xid_flag_source = '%s',
                           xid_flag_comment = '%s'
                     where uid = %s""" % (
        xid_flag, xid_flag_source, xid_flag_comment, uid))
    CONN.commit()
    return None

def single_cluster_update_obs_flag(uid, obs_flag, obs_flag_source,
                                   obs_flag_comment):
    """
    Updates detection status for a cluster.
    """
    CONN = get_conn()
    CONN.execute("""update clusters
                       set obs_flag = %s,
                           obs_flag_source = '%s',
                           obs_flag_comment = '%s'
                     where uid = %s""" % (
        obs_flag, obs_flag_source, obs_flag_comment, uid))
    CONN.commit()
    return None


def single_cluster_key_value_update(uid, old_key, key, key_value,
                                    key_err_low, key_err_high,
                                    key_comment):
    """
    Update per cluster key.
    """

    old_key, _, subkey_cond = key_subkey_cond(old_key)
    key, subkey, _ = key_subkey_cond(key)
    if subkey == '':
        subkey = 'null'
    else:
        subkey = '"%s"' % subkey
    CONN = get_conn()
    CONN.execute("""update per_cluster_keys
                       set key = "%s",
                           subkey = %s,
                           value = "%s",
                           value_error_low = "%s",
                           value_error_high = "%s",
                           comment = "%s"
                     where uid = %s
                       and key = "%s"
                       and %s
                       """ % (key, subkey,
                              key_value, key_err_low, key_err_high,
                              key_comment, uid, old_key, subkey_cond))
    CONN.commit()
    return None


def select_cluster_key(uid, table_data, conn):
    params = []
    for key in conn.cursor().execute("""
        select kr.reference_column, kr.is_string,
               kr.error_column_low, kr.error_column_high, kr.comment_column,
               k.key, k.subkey, k.description,
               ifnull(k.data_format, rc.output_format) as output_format
          from reference_tables_keys kr
          join keys k on k.key = kr.key
                     and ifnull(k.subkey, 'null') = ifnull(kr.subkey, 'null')
          join reference_tables_columns rc on kr.reference_table = rc.reference_table
                                          and kr.reference_column = rc.column_name
         where kr.reference_table = '%s'
      order by k.key, k.subkey""" % table_data['table_name']):
        select = 'x.[%s] as reference_column' % key['reference_column']
        for extra in ['error_column_low', 'error_column_high',
                      'comment_column']:
            if key[extra] is not None:
                select = '%s, x.[%s] as %s' % (select, key[extra], extra)
        ext_row = table_data.copy()
        ext_row['uid'] = uid
        ext_row['select'] = select
        values = conn.execute("""select {select}, r.reference_uid
                   from [{table_name}] x
                   join data_references r on r.reference_uid = [{uid_column}]
                  where r.cluster_uid = {uid}
                    and r.reference_table = '{table_name}'""".format(**ext_row)).fetchall()
        for value in values:
            print value['reference_column'], key['output_format']
            par = {'name': key['key'],
                   'desc': key['description'],
                   'value': format_value(value['reference_column'], key['output_format']),
                   'source': '%s[%s]:%s' % (table_data['table_name'],
                                           value['reference_uid'],
                                           key['reference_column'])}
            if key['error_column_low'] is not None:
                par['err_low'] = format_value(value['error_column_low'], key['output_format'])
            if key['error_column_high'] is not None:
                par['err_high'] = format_value(value['error_column_high'], key['output_format'])
            if key['comment_column'] is not None:
                par['comment'] = key['comment_column']
            params.append(par)
    return params

def single_cluster(uid):
    t = JINJA.get_template('single_cluster.template')
    CONN = get_conn(dict_row=True)
    cur = CONN.cursor()
    html_data = {}
    result = CONN.execute("select source, source_id, comment, "
                          "xid_flag, xid_flag_source, xid_flag_comment,"
                          "obs_flag, obs_flag_source, obs_flag_comment,"
                          "ra, dec"
                          " from clusters where uid = %s" % uid).fetchone()
    html_data = dict(result)
    for key in ['xid_flag_source', 'xid_flag_comment',
                'obs_flag_source', 'obs_flag_comment']:
        if html_data[key] is None:
            html_data[key] = ''
    html_data['uid'] = uid
    html_data['ra'] = '%.6f' % html_data['ra']
    html_data['dec'] = '%.6f' % html_data['dec']
    html_data['params'] = []
    html_data['tables'] = []
    for key in CONN.cursor().execute("""
    select k.key, k.subkey, k.description,
           v.value, v.value_error_low, v.value_error_high,
           v.comment,
           ifnull(k.data_format, 's') output_format
      from per_cluster_keys v
      join keys k on k.key = v.key
                 and ifnull(k.subkey, 'null') = ifnull(v.subkey, 'null')
     where v.uid = %s""" % uid):
         if key['subkey'] is not None and key['subkey'] != '':
             key_name = '%s,%s' % (key['key'], key['subkey'])
         else:
             key_name = key['key']
         par = {'name': key_name,
                'desc': key['description'],
                'value': format_value(key['value'], key['output_format']),
                'err_low': key['value_error_low'],
                'err_high': key['value_error_high'],
                'comment': key['comment'],
                'source': 'User defined'}
         html_data['params'].append(par)
    html_data['select_key'] = get_key_list(CONN)
    mocs = []
    for row in CONN.execute("""select m.moc_name,
                                      coalesce(m.description, m.moc_name) as description,
                                      m.vizier_catalog
                               from cluster_in_moc c
                            join mocs m on c.moc_name = m.moc_name
                           where uid = %s
                           union
                           select mm.moc_name, mm.description, mm.vizier_catalog
                             from mocs mm where mm.is_full_sky
                             """ % uid).fetchall():
        moc = {'moc': row[0],
               'description': row[1],
               'link': ''}
        if row[2] is not None:
            url_data = {'-source': row[2],
                        '-out.max': 'unlimited',
                        '-out.form': 'HTML Table',
                        '-out.add': '_r,_RAJ,_DEJ',
                        '-sort': '_r',
                        '-oc.form': 'dec',
                        '-c': '%+f%+f' % (float(html_data['ra']),
                                          float(html_data['dec'])),
                        '-c.eq': 'J2000',
                        '-c.r': 2,
                        '-c.u': 'arcmin',
                        '-c.geom': 'r'}
            link = 'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?%s' % urlencode(url_data)
            moc['link'] = '<a href="%s">Vizier data</a>' % link
        mocs.append(moc)
    html_data['mocs'] = mocs
    for row in cur.execute("""select rt.table_name,
                                     rt.uid_column,
                                     rt.extra_column, rt.description,
                                     rt.brief_columns
                                from reference_tables rt
                               where exists (select 1
                                               from data_references d
                                              where d.reference_table = rt.table_name
                                                and d.cluster_uid = %s)
                                  """ % uid):
        row = dict(row)
        column_list = get_brief_columns(row['table_name'],
                                        row['brief_columns'].split(','),
                                        negate=False)
        column_list = ','.join(['x.[%s]' % x for x in column_list])

        t1 = from_db_cursor(CONN.execute("""
            select {column_list}
              from [{table_name}] x
              join data_references r on r.reference_uid = [{uid_column}]
                                    and r.reference_table = '{table_name}'
             where r.cluster_uid = {uid}""".format(column_list=column_list,
                                                   uid=uid, **row)))
        t1.border = True
        t1.float_format = '.3e'
        for column_properties in CONN.execute("""
        select column_name, output_format, description,
               data_unit, lower(data_type) as data_type
          from reference_tables_columns
         where reference_table = '%s'""" % row['table_name']).fetchall():
            if column_properties['data_type'] == 'integer':
                t1.int_format[column_properties['column_name']] = \
                    column_properties['output_format']
            elif column_properties['data_type'] in ('real', 'double'):
                t1.float_format[column_properties['column_name']] = \
                    column_properties['output_format']

        # Full table record (initially hidden)
        cursor = CONN.execute("""
            select x.*
              from [{table_name}] x
              join data_references r on r.reference_uid = [{uid_column}]
                                    and r.reference_table = '{table_name}'
             where r.cluster_uid = {uid}""".format(uid=uid, **row))
        full_table = PrettiestTable()
        full_table.add_column('Parameter',
                              [item[0] for item in cursor.description])
        for irow, arow in enumerate(cursor.fetchall()):
            full_table.add_column(str(irow), arow)
        if len(t1._rows) > 0:
            html_data['tables'].append({
                'title': row['description'],
                'id': row['table_name'],
                'full_table': full_table.get_html_string(attributes={'border': 1}),
                'html': t1.get_html_string(attributes={'border': 1,
                                                       'id': row['table_name']})})
            html_data['params'].extend(select_cluster_key(uid, row, CONN))
    return t.render(html_data)
