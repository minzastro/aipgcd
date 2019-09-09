
"""
SQL bindings for AstroPy tables.
Most of this code was inherited from ATpy.
Copied and simplified from atpy 0.9.7 by A. Mints (2015).
"""

import warnings

import numpy as np

from . import sqlhelper as sql
from ...utils.exceptions import AstropyUserWarning as TableException
from ...utils.exceptions import AstropyUserWarning as  ExistingTableException

invalid = {}
invalid[np.uint8] = np.iinfo(np.uint8).max
invalid[np.uint16] = np.iinfo(np.uint16).max
invalid[np.uint32] = np.iinfo(np.uint32).max
invalid[np.uint64] = np.iinfo(np.int64).max
invalid[np.int8] = np.iinfo(np.int8).max
invalid[np.int16] = np.iinfo(np.int16).max
invalid[np.int32] = np.iinfo(np.int32).max
invalid[np.int64] = np.iinfo(np.int64).max
invalid[np.float32] = np.float32(np.nan)
invalid[np.float64] = np.float64(np.nan)

def is_sql(origin, filepath, fileobj, *args, **kwargs):
    return True

def read(input, dbtype='sqlite', *args, **kwargs):
    '''
    Required Arguments:

        *dbtype*: [ 'sqlite' | 'mysql' | 'postgres' ]
            The SQL database type

    Optional arguments (only for Table.read() class):

        *table*: [ string ]
            The name of the table to read from the database (this is only
            required if there are more than one table in the database). This
            is not required if the query= argument is specified, except if
            using an SQLite database.

        *query*: [ string ]
            An arbitrary SQL query to construct a table from. This can be
            any valid SQL command provided that the result is a single
            table.

    The remaining arguments depend on the database type:

    * SQLite:

        Arguments are passed to sqlite3.connect(). For a full list of
        available arguments, see the help page for sqlite3.connect(). The
        main arguments are listed below.

        Required arguments:

            *dbname*: [ string ]
                The name of the database file

    * MySQL:

        Arguments are passed to MySQLdb.connect(). For a full list of
        available arguments, see the documentation for MySQLdb. The main
        arguments are listed below.

        Optional arguments:

            *host*: [ string ]
                The host to connect to (default is localhost)

            *user*: [ string ]
                The user to conenct as (default is current user)

            *passwd*: [ string ]
                The user password (default is blank)

            *db*: [ string ]
                The name of the database to connect to (no default)

            *port* [ integer ]
                The port to connect to (default is 3306)

    * PostGreSQL:

        Arguments are passed to pgdb.connect(). For a full list of
        available arguments, see the help page for pgdb.connect(). The
        main arguments are listed below.

        *host*: [ string ]
            The host to connect to (default is localhost)

        *user*: [ string ]
            The user to conenct as (default is current user)

        *password*: [ string ]
            The user password (default is blank)

        *database*: [ string ]
            The name of the database to connect to (no default)
    '''

    if 'table' in kwargs:
        atable = kwargs.pop('table')
    else:
        atable = None

    if 'verbose' in kwargs:
        verbose = kwargs.pop('verbose')
    else:
        verbose = True

    if 'query' in kwargs:
        query = kwargs.pop('query')
    else:
        query = None

    if atable is None and query is None:
        if input[:6].lower() == 'select':
            query = input
        else:
            atable = input
    connection, cursor = sql.connect_database(dbtype, *args, **kwargs)

    # If no table is requested, check that there is only one table

    table_names = sql.list_tables(cursor, dbtype)

    if len(table_names) == 0:
        raise Exception("No table in selected database")

    from ...table import Table
    table = Table()
    if not query or dbtype == 'sqlite':
        if atable==None:
            if len(table_names) == 1:
                table_name = list(table_names.keys())[0]
            else:
                raise TableException(table_names, 'table')
        else:
            table_name = table_names[atable]

        # Find overall names and types for the table
        column_names, column_types, primary_keys = sql.column_info(cursor, dbtype, \
            str(table_name))

        table.meta['table_name'] = table_name

    else:

        column_names = []
        column_types = []
        primary_keys = []

        table.meta['table_name'] = "sql_query"

    if query:

        # Execute the query
        cursor.execute(query)

        if dbtype == 'sqlite':
            column_types_dict = dict(list(zip(column_names, column_types)))
        else:
            column_types_dict = None

        # Override column names and types
        try:
            column_names, column_types = sql.column_info_desc(dbtype, cursor.description, column_types_dict)
        except KeyError as exc:
            if dbtype == 'sqlite':
                raise TableException('Only single-column queries are allowed for SQLite')
            else:
                raise exc

    else:

        cursor = connection.cursor()

        cursor.execute('select * from ' + table_name)

    results = cursor.fetchall()

    if results:
        results = np.rec.fromrecords(list(results), \
                        names = column_names)
    else:
        raise Exception("SQL query did not return any records")

    for i, column in enumerate(results.dtype.names):

        if column_types[i] in invalid:
            null = invalid[column_types[i]]
            results[column][np.equal(np.array(results[column],
                                     dtype=np.object), None)] = null
        else:
            null = 'None'
        column = table.Column(name=column, data=results[column],
                              dtype=column_types[i], meta={'null': null})
        table.add_column(column)
    return table

def write(input, output, dbtype='sqlite', *args, **kwargs):

    # Check if table overwrite is requested
    if 'overwrite' in kwargs:
        overwrite = kwargs.pop('overwrite')
    else:
        overwrite = False


    # Open the connection
    kwargs['database'] = output
    connection, cursor = sql.connect_database(dbtype, *args, **kwargs)

    # Check that table name is set
    if 'table_name' in input.meta:
        table_name = str(input.meta['table_name'])
    elif 'table_name' in kwargs:
        table_name = kwargs['table_name']
    else:
        raise Exception("Table name is not set")

    # Check that table name is ok
    # todo

    # lowercase because pgsql automatically converts
    # table names to lower case

    # Check if table already exists

    existing_tables = list(sql.list_tables(cursor, dbtype).values())
    if table_name in existing_tables or \
        table_name.lower() in existing_tables:
        if overwrite:
            sql.drop_table(cursor, table_name)
        else:
            raise ExistingTableException()

    # Create table
    columns = [(name, input.columns[name].dtype.type) for name in list(input.columns.keys())]
    sql.create_table(cursor, dbtype, table_name, columns)
    # Insert row
    for row in input.as_array():
        sql.insert_row(cursor, dbtype, table_name,
                       list(row.tolist()), fixnan=not input._masked)
    # Close connection
    connection.commit()
    cursor.close()

write.__doc__ = read.__doc__


def read_set(input, dbtype, *args, **kwargs):

    input.reset()

    connection, cursor = sql.connect_database(dbtype, *args, **kwargs)
    table_names = sql.list_tables(cursor, dbtype)
    cursor.close()

    from .basetable import Table
    for table in table_names:
        kwargs['table'] = table
        table = Table()
        read(table, dbtype, *args, **kwargs)
        input.append(table)

read_set.__doc__ = read.__doc__


def write_set(input, dbtype, *args, **kwargs):

    for table_key in input.tables:
        write(input.tables[table_key], dbtype, *args, **kwargs)

write_set.__doc__ = write.__doc__
