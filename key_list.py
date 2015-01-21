#!/usr/bin/python
"""
Created on Wed Jan 14 18:21:14 2015
@author: mints
"""
from prettytable import from_db_cursor
from AIP_clusters.globals import get_conn, JINJA

def key_list():
    t = JINJA.get_template('key_list.template')
    t1 = from_db_cursor(get_conn().execute("""
        select key, key_class, description, data_format,
               '<a href="edit_key?table=%s&key='||k.key||'&key_class='||coalesce(k.key_class, 'none')||'">edit</a>' as link
          from keys k"""))
    return t.render({'key_list': t1.get_html_string(attributes={'border': 1},
                                                    unescape=['link'])})
