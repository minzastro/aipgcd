#!/usr/bin/python
"""
Created on Thu Apr 23 16:00:45 2015
@author: mints
"""
from os import path
NAME = '%s/..' % path.dirname(__file__)

from mocfinder import MOCFinder
from globals import get_conn
from glob import glob
import sys

def search_mocs(mocname, mocfile):
    conn = get_conn()
    cur = conn.cursor()
    moc = MOCFinder(mocfile)
    conn.execute("""insert into mocs (moc_name, moc_file)
                    values ('%s', '%s')""" % (mocname, mocfile))
    for uid, ra, dec in cur.execute("""
        select uid, ra, dec from clusters order by uid""").fetchall():
        if moc.is_in(ra, dec):
            conn.execute("""insert into cluster_in_moc (uid, moc_name)
                            values (%s, '%s')""" % (uid, mocname))
        print mocname, uid
    conn.commit()
    cur.close()

if __name__ == '__main__':
    mocfile = sys.argv[1]
    mocname = mocfile[mocfile.index('_')+1:]
    search_mocs(mocname[:-5], mocfile)
