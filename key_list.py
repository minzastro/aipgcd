#!/usr/bin/python
"""
Created on Wed Jan 14 18:21:14 2015
@author: mints
"""
from prettiesttable import from_db_cursor
from globals import get_conn, JINJA

def key_list():
    t = JINJA.get_template('key_list.template')
    t1 = from_db_cursor(get_conn().execute("""
        select key, key_class, description, data_format
          from keys k"""))
    select_key = []
    for row in t1._rows:
        if row[0] not in select_key:
            select_key.append(row[0])
        
    return t.render({'key_list': t1.get_html_string(attributes={'border': 1, 
                                                                'id': 'key_list'}),
                     'select_key': select_key})

def key_list_update(key, key_class, description, format):
    conn = get_conn()
    check = conn.execute(u"""select count(*)
                               from keys
                              where key = '%s'
                                and ifnull(key_class, 'None') = '%s'""" % (key, key_class)).fetchone()[0]
    print key, key_class, check
    if check > 0:
        conn.execute(u"""update keys
                            set description = '%s',
                                data_format = '%s'
                              where key = '%s'
                                and ifnull(key_class, 'None') = '%s'""" % (description,
                                                           format, 
                                                           key, key_class))
    else:
        print u"""
         insert into keys (key, key_class, description, data_format)
         values ('%s', '%s', '%s', '%s');
        """ % (key, key_class, description, format)
        conn.execute(u"""
         insert into keys (key, key_class, description, data_format)
         values ('%s', '%s', '%s', '%s');
        """ % (key, key_class, description, format))
    conn.commit()
    return None
        