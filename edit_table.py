# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettytable import from_db_cursor
from AIP_clusters.globals import get_conn, JINJA
from AIP_clusters.globals import null_condition, nullify, get_key_list


def edit_table(table):
    """
    Editing single table.
    """
    t = JINJA.get_template('edit_table.template')
    cur = get_conn().cursor()
    row = cur.execute("""select rt.table_name,
                                rt.uid_column,
                                rt.description
                           from reference_tables rt
                          where table_name = '%s'""" % table).fetchone()
    html_data = {'table': table,
                 'description': row[2],
                 'uid_column': row[1]}
    t1 = from_db_cursor(get_conn().execute("""
             select k.key, k.key_class, k.description, k.data_format,
                    r.reference_column, r.error_column_low,
                    r.error_column_high, r.comment,
                    '<a href="edit_key?table=%s&key='||k.key||'&key_class='||coalesce(k.key_class, 'none')||'">edit</a>' as link
               from keys k
               join key_referencer r on r.key = k.key
                                    and ifnull(r.key_class, '') = ifnull(k.key_class, '')
              where r.reference_table = '%s'
              order by k.key, k.key_class""" % (table, table)))
    t1.add_row(['']*8 + ['<a href="edit_key?table=%s&key=&key_class=&is_new=1">add new</a>' % table])
    html_data['keys'] = t1.get_html_string(attributes={'border': 1},
                                           unescape=['link'])
    return t.render(html_data)


def edit_key(table, key, key_class, is_new=0):
    t = JINJA.get_template('edit_key.template')
    conn = get_conn()
    if key_class == 'none':
        key_class = None
        condition = 'key_class is Null'
    else:
        condition = 'key_class = "%s"' % key_class
    html_data = {'table': table,
                 'key': key,
                 'key_class': key_class,
                 'description': '',
                 'key_list': get_key_list(conn)}
    if is_new == 0:
        html_data['mode'] = 'edit'
        t1 = conn.execute("""
             select r.reference_column, r.error_column_low,
                    r.error_column_high, r.comment
               from key_referencer r
              where r.reference_table = '%s'
                and r.key = '%s'
                and %s""" % (table, key, condition)).fetchone()
        html_data.update({'reference_column': t1[0],
                          'error_column_low': t1[1],
                          'error_column_high': t1[2],
                          'comment': t1[3]
                          })
    else:
        html_data['mode'] = 'new'
    return t.render(html_data)


def edit_key_update(table, mode, key, key_class, description,
                    reference_column, error_column_low, error_column_high,
                    comment):
    conn = get_conn()
    if mode == 'edit':
        conn.execute(u"""
            update key_referencer
               set reference_column = %s,
                   error_column_low = %s,
                   error_column_high = %s,
                   comment = %s
             where reference_table = '%s'
               and key = '%s'
               and %s
        """ % (nullify(reference_column),
               nullify(error_column_low),
               nullify(error_column_high),
               nullify(comment),
               table, key, null_condition('key_class', key_class)))
        conn.commit()
    else:
        r1 = conn.execute("""
            select key
              from key_referencer
             where reference_table = '%s'
               and key = '%s'
               and %s""" % (table, key, null_condition('key_class', key_class)))
        if r1.rowcount > 0:
            return "Already exists!"
        else:
            conn.execute(u"""
            insert into key_referencer(reference_table, key, key_class,
                reference_column, error_column_low, error_column_high, comment)
            values ("%s", "%s", %s, %s, %s, %s, %s)
            """ % (table, key, nullify(key_class),
                  nullify(reference_column),
                  nullify(error_column_low),
                  nullify(error_column_high),
                  nullify(comment)))
            conn.commit()

def edit_table_update(table, description, uid_column):
    """
    Committing changes done to the table.
    """
    conn = get_conn()
    conn.execute("""update reference_tables
                      set description = '%s',
                          uid_column = '%s'
                    where table_name = '%s'""" % (description,
                                                  uid_column,
                                                  table)).fetchone()
    conn.commit()
    return open('static/table_edit_ok.html', 'r').readlines()


def list_table(table):
    """
    List the table content.
    """
    t = JINJA.get_template('list_table.template')
    conn = get_conn()
    row = conn.execute("""select uid_column, description
                            from reference_tables
                           where table_name = '%s'""" % table).fetchone()
    t1 = from_db_cursor(conn.execute("""select * from %s""" % table))
    html_data = {'name': table,
                 'table': t1.get_html_string(attributes={'border': 1}),
                 'uid': row[0],
                 'desc': row[1]}
    return t.render(html_data)
