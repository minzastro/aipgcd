# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 20:28:43 2014

@author: minz
"""

import cherrypy
from AIP_clusters.single_cluster import single_cluster
from AIP_clusters.edit_tables import edit_tables
from AIP_clusters.edit_table import edit_table, edit_table_update, \
                                    list_table, \
                                    edit_table_key, edit_table_key_update
from AIP_clusters.key_list import key_list
from AIP_clusters.vo_cone_search import vo_cone_search
from AIP_clusters.globals import get_key_class_list, get_key_description, get_table_columns

def error_page_404(status, message, traceback, version):
    return "Error %s - Page does not exist yet. It might appear later!" % status
cherrypy.config.update({'error_page.404': error_page_404})

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return open('static/main.html', 'r').readlines()

    @cherrypy.expose
    def single(self, uid=60036):
        return single_cluster(uid)

    @cherrypy.expose
    def edit_tables(self):
        return edit_tables()

    @cherrypy.expose
    def edit_table(self, table):
        return edit_table(table)

    @cherrypy.expose
    def key_list(self):
        return key_list()

    @cherrypy.expose
    def edit_table_key(self, table, key, key_class, is_new=0):
        return edit_table_key(table, key, key_class, is_new)

    @cherrypy.expose
    def edit_table_key_update(self, table, mode, key, key_class,
                              reference_column, error_column_low,
                              error_column_high, comment):
        edit_table_key_update(table, mode, key, key_class,
                              reference_column, error_column_low,
                              error_column_high, comment)
        raise cherrypy.InternalRedirect('edit_table?table=%s' % str(table))

    @cherrypy.expose
    def get_key_class_list(self, key):
        return ','.join(get_key_class_list(key))

    @cherrypy.expose
    def get_key_description(self, key, key_class):
        return ','.join(map(str, get_key_description(key, key_class)))

    @cherrypy.expose
    def get_table_columns(self, table):
        return ','.join(map(str, get_table_columns(table)))

    @cherrypy.expose
    def list_table(self, table):
        return list_table(table)

    @cherrypy.expose
    def vo_cone_search(self, ra, decl, radius):
        return vo_cone_search(ra, decl, radius)

    @cherrypy.expose
    def edit_table_update(self, table, description, uid_column, brief_columns):
        return edit_table_update(table, description, uid_column, brief_columns)

if __name__ == '__main__':
   cherrypy.quickstart(HelloWorld(), config="aipccd.conf")