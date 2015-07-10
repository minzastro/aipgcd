#!/usr/bin/python
"""
Created on Wed Feb 11 17:02:04 2015
@author: mints
"""
import numpy as np
from astropy.table import Table as ATable
from globals import get_conn, sqllist
from tempfile import NamedTemporaryFile, mkdtemp
import simplejson as json

VO_TYPES = {int: 'I8',
            unicode: 'S',
            float: 'F8',
            bool: 'bool'}

def data_to_votable(coltypes, header, data):
    coltypes = list(coltypes)
    data = json.loads(data)
    data = np.array(data)
    data = zip(*data)
    print header, coltypes, len(data), data[0]
    for irow in xrange(len(data)):
        print data[irow][0], coltypes[irow]
        if coltypes[irow].lower() == 'i':
            data[irow] = np.genfromtxt(data[irow], dtype=np.int,
                                       missing_values='None',
                                       usemask=True)
            coltypes[irow] = 'i4'
        elif coltypes[irow].lower() == 'f':
            data[irow] = np.genfromtxt(data[irow], dtype=np.float,
                                       missing_values='None',
                                       usemask=True)
            coltypes[irow] = 'f8'
    table = ATable(data=data, names=header, dtype=coltypes)
    temp_file = NamedTemporaryFile(delete=False, dir='./static/output_cache',
                                   suffix='.votable')
    table.write(temp_file, format='votable')
    temp_file.close()
    return temp_file.name

def sql_to_file(sql, output_name='default', write_format='ascii',
                automatic_extention=True):
    """
    Run SQL query and save output to ascii (or other formats) file.
    """
    cursor = get_conn().execute(sql)
    column_names = []
    column_types = []
    max_len = []
    data = cursor.fetchall()
    for column_descr in cursor.description:
        column_names.append(column_descr[0])
    for item in data[0]:
        max_len.append(0)
        column_types.append(VO_TYPES[type(item)])
    for row in data:
        print row
        for icol, coltype in enumerate(column_types):
            print icol, coltype
            if coltype == 'S' and row[icol] is not None:
                if max_len[icol] < len(row[icol]):
                    max_len[icol] = len(row[icol])
    for icol, coltype in enumerate(column_types):
        if coltype == 'S':
            column_types[icol] = 'S%s' % max_len[icol]
    if len(data) == 0:
        table = ATable(names=column_names, dtype=column_types)
    else:
        table = ATable(data=zip(*data), names=column_names, dtype=column_types)
    if output_name is not None:
        if automatic_extention:
            file_name = '%s.%s' % (output_name, write_format)
        else:
            file_name = output_name
        temp_file = open('./static/output_cache/%s' % (file_name), 'w')
    else:
        temp_file = NamedTemporaryFile(delete=False, dir='./static/output_cache',
                                       suffix=write_format)
    table.write(temp_file, format=write_format)
    temp_file.close()
    return temp_file.name


def get_samp_table(params):
    if 'sql' not in params:
        raise Exception('No sql code provided')
    sql = params.pop('sql')
    if sql not in sqllist.SQL_LIST:
        raise Exception('This sql code is not valid: %s' % sql)
    sql = sqllist.get_sql(sql, **params)
    return sql_to_file(sql, write_format='votable')


if __name__ == '__main__':
    sql_to_file('select * from xdcp_b')