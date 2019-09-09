#!/usr/bin/python
"""
Created on Wed Jan 14 18:21:14 2015
@author: mints
"""
from .prettiesttable import from_db_cursor
from .globals import get_conn, JINJA

def moc_list():
    t = JINJA.get_template('moc_list.template')
    t1 = from_db_cursor(get_conn().execute("""
        select moc_name, moc_file, description, vizier_catalog, is_full_sky
          from mocs"""))
    select_moc = []
    for row in t1._rows:
        if row[0] not in select_moc:
            select_moc.append(row[0])

    return t.render({'moc_list': t1.get_html_string(attributes={'border': 1,
                                                                'id': 'moc_list'}),
                     'select_moc': select_moc})
