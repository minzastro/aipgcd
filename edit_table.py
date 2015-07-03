# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:22:39 2014

@author: minz
"""
from prettiesttable import from_db_cursor
from globals import get_conn, JINJA
from globals import get_table_columns
from globals import null_condition, nullify, get_key_list


def edit_table(table):
    """
    Editing single table.
    """
    t = JINJA.get_template('edit_table.template')
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("""select rt.table_name,
                                rt.uid_column,
                                rt.description,
                                rt.brief_columns
                           from reference_tables rt
                          where table_name = '%s'""" % table).fetchone()
    cur.close()
    columns = get_table_columns(table)
    columns[0] = 'None'
    html_data = {'table': table,
                 'description': row[2],
                 'uid_column': row[1],
                 'brief_columns': row[3],
                 'key_list': get_key_list(conn),
                 'column_names': columns
                 }
    t1 = from_db_cursor(conn.execute("""
             select r.uid, k.key, k.subkey, k.description, k.data_format,
                    r.reference_column, r.error_column_low,
                    r.error_column_high, r.comment,
                    "Delete"
               from keys k
               join reference_tables_keys r on r.key = k.key
                                    and ifnull(r.subkey, '') = ifnull(k.subkey, '')
              where r.reference_table = '%s'
                  order by k.key, k.subkey""" % (table)))
    html_data['keys'] = t1.get_html_string(attributes={'border': 1,
                                                       'id': 'keys_table'})
    t2 = from_db_cursor(conn.execute("""
      select column_name, data_type, data_unit,
             output_format, description, ucd
        from reference_tables_columns
       where reference_table = '%s'""" % table))
    html_data['columns'] = t2.get_html_string(attributes={'border': 1,
                                                          'id': 'columns_table'})
    conn.close()
    return t.render(html_data)


def edit_table_update_column(table, column_name, data_type, data_unit,
                             output_format, description):
    conn = get_conn()
    conn.execute("""update reference_tables_columns
                       set data_type = '%s',
                           data_unit = '%s',
                           output_format = '%s',
                           description = '%s'
                     where reference_table = '%s'
                       and column_name = '%s'
                    """ % (data_type, data_unit,
                           output_format, description,
                           table, column_name)).fetchone()
    conn.commit()
    return None


def edit_table_update(table, description, uid_column, brief_columns):
    """
    Committing changes done to the table.
    """
    conn = get_conn()
    conn.execute("""update reference_tables
                      set description = '%s',
                          uid_column = '%s',
                          brief_columns = '%s'
                    where table_name = '%s'""" % (description,
                                                  uid_column,
                                                  brief_columns,
                                                  table)).fetchone()
    conn.commit()
    return open('static/table_edit_ok.html', 'r').readlines()


def edit_table_key_delete(table, uid):
    conn = get_conn()
    conn.execute(u"""
    delete from reference_tables_keys
     where reference_table = '%s'
       and uid = %s""" % (table, uid))
    conn.commit()
    return None


def edit_table_key_update(table, mode, uid, key,
                          reference_column,
                          error_column_low, error_column_high,
                          comment):
    conn = get_conn()
    if ',' in key:
        key, subkey = key.split(',')
    else:
        subkey = None
    if uid != '':
        check = conn.execute(u"""select key
                                   from reference_tables_keys
                                  where uid = %s""" % uid).rowcount
    else:
        check = 0
    if mode == 'edit' or check > 0:
        conn.execute(u"""
            update reference_tables_keys
               set reference_column = %s,
                   error_column_low = %s,
                   error_column_high = %s,
                   comment = %s,
                   key = %s,
                   subkey = %s
             where uid = %s
        """ % (nullify(reference_column),
               nullify(error_column_low),
               nullify(error_column_high),
               nullify(comment),
               nullify(key),
               nullify(subkey),
               uid))
        conn.commit()
    else:
        r1 = conn.execute("""
            select key
              from reference_tables_keys
             where reference_table = '%s'
               and key = '%s'
               and %s""" % (table, key, null_condition('subkey', subkey)))
        if r1.rowcount > 0:
            return "Already exists!"
        else:
            conn.execute(u"""
            insert into reference_tables_keys(reference_table, key, subkey,
                reference_column, error_column_low, error_column_high, comment)
            values ("%s", "%s", %s, %s, %s, %s, %s)
            """ % (table, key, nullify(subkey),
                   nullify(reference_column),
                   nullify(error_column_low),
                   nullify(error_column_high),
                   nullify(comment)))
            conn.commit()
    return None


def list_table(table):
    """
    List the table content.
    """
    t = JINJA.get_template('list_table.template')
    conn = get_conn()
    row = conn.execute("""select uid_column, description
                            from reference_tables
                           where table_name = '%s'""" % table).fetchone()
    sql = """select d.cluster_uid, t.*
               from [{table}] t
               join data_references d
                 on d.reference_table = '{table}'
                and d.reference_uid = t.[{uid}]""".format(table=table,
                                                          uid=row[0])
    t1 = from_db_cursor(conn.execute(sql))
    columns = conn.execute("""select column_name, data_type, output_format
      from reference_tables_columns
     where reference_table = '%s'
     order by uid""" % table).fetchall()
    columns_param = ['I'] # That is for UID
    for column_name, data_type, output_format in columns:
        if data_type.lower() in ('int', 'integer', 'long'):
            t1._int_format[column_name] = output_format
            columns_param.append('I')
        elif data_type.lower() in ('float', 'double', 'real'):
            t1._float_format[column_name] = output_format
            columns_param.append('F')
        else:
            columns_param.append('S')
    html_data = {'name': table,
                 'table': t1.get_html_string(attributes={'border': 1,
                                                         'id': 'list_table',
                                                         'columns': ''.join(columns_param)}),
                 'uid': row[0],
                 'desc': row[1],
                 'sql': sql}
    return t.render(html_data)
