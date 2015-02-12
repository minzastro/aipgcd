# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 21:03:38 2014

@author: minz
"""
from globals import get_conn, JINJA

def edit_tables():
    t = JINJA.get_template('tables.template')
    cur = get_conn().cursor()
    html_data = {}

    html_data['tables'] = []
    for row in cur.execute("""select rt.table_name,
                                     rt.uid_column, rt.is_string_uid, rt.extra_column,
                                     rt.description
                                from reference_tables rt"""):
        html_data['tables'].append({
            'name': row[0],
            'desc': row[4],
            'uid': row[1]})
    return t.render(html_data)
