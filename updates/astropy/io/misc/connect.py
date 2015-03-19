# Licensed under a 3-clause BSD style license - see LICENSE.rst
# This file connects any readers/writers defined in io.misc to the
# astropy.table.Table class

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .hdf5 import read_table_hdf5, write_table_hdf5, is_hdf5
from .sqltable import read as sql_read, write as sql_write, is_sql

from .. import registry as io_registry
from ...table import Table

io_registry.register_reader('hdf5', Table, read_table_hdf5)
io_registry.register_writer('hdf5', Table, write_table_hdf5)
io_registry.register_identifier('hdf5', Table, is_hdf5)

io_registry.register_reader('sql', Table, sql_read)
io_registry.register_writer('sql', Table, sql_write)
io_registry.register_identifier('sql', Table, is_sql)
