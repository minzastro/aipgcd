# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 20:28:43 2014

@author: minz
"""
import sys
from os import path
NAME = '%s/..' % path.dirname(__file__)
sys.path.insert(0, path.abspath(path.dirname(__file__)))
print sys.path

import cherrypy
from single_cluster import single_cluster, \
                                        single_cluster_update_comment, \
                                        single_cluster_update_xid
from edit_tables import edit_tables
from edit_table import edit_table, edit_table_update, \
                                    list_table, \
                                    edit_table_key_delete, edit_table_key_update, \
                                    edit_table_update_column
from key_list import key_list, key_list_update
from vo_cone_search import vo_cone_search
from search import search
#from samp import get_samp_table
from globals import get_key_class_list, get_key_description, \
                                 get_table_columns


def error_page_404(status, message, traceback, version):
    return "Error %s - Page does not exist yet. It might appear later!" % status
cherrypy.config.update({'error_page.404': error_page_404})


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return search()

    #@cherrypy.expose
    #def get_samp_table(self, **params):
#        return get_samp_table(params)

    @cherrypy.expose
    def single(self, uid=60036):
        return single_cluster(uid)

    @cherrypy.expose
    def single_cluster_update_comment(self, uid, comment):
        return single_cluster_update_comment(uid, comment)

    @cherrypy.expose
    def single_cluster_update_xid(self, uid, xid):
        return single_cluster_update_xid(uid, xid)

    @cherrypy.expose
    def edit_tables(self):
        return edit_tables()

    @cherrypy.expose
    def edit_table(self, table):
        return edit_table(table)

    @cherrypy.expose
    def edit_table_update_column(self, table, column_name, data_type,
                                 data_unit, output_format, description):
        return edit_table_update_column(table, column_name, data_type,
                                        data_unit, output_format, description)

    @cherrypy.expose
    def key_list(self):
        return key_list()

    @cherrypy.expose
    def key_list_update(self, key, key_class, description, format):
        return key_list_update(key, key_class, description, format)

    @cherrypy.expose
    def edit_table_key_delete(self, table, uid):
        edit_table_key_delete(table, uid)
        return key_list()

    @cherrypy.expose
    def edit_table_key_update(self, table, mode, uid, key,
                              reference_column, error_column_low,
                              error_column_high, comment):
        edit_table_key_update(table, mode, uid, key,
                                     reference_column, error_column_low,
                                     error_column_high, comment)
        raise cherrypy.InternalRedirect('edit_table?table=%s' % str(table))

    @cherrypy.expose
    def get_key_class_list(self, key):
        return ','.join(get_key_class_list(key))

    @cherrypy.expose
    def get_key_description(self, key):
        key, key_class = key.split(',')
        return ','.join(map(str, get_key_description(key, key_class)))

    @cherrypy.expose
    def get_table_columns(self, table):
        return ','.join(map(str, get_table_columns(table)))

    @cherrypy.expose
    def list_table(self, table):
        return list_table(table)

    @cherrypy.expose
    def vo_cone_search(self, **params):
        print params
        return vo_cone_search(params)

    @cherrypy.expose
    def edit_table_update(self, table, description, uid_column, brief_columns):
        return edit_table_update(table, description, uid_column, brief_columns)

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(), config="aipgcd.conf")
