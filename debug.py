#!/usr/bin/python
import numpy as np
from astropy.table import Table
t = Table([[1, 2, 3], [0.1, 0.2, -0.3]], names=('a', 'b'))
t.add_column(Table.Column(data=[0.1, 0.3, -0.55], name='x', dtype=np.float32))
t.meta['table_name'] = 'defa'
t.write('a.sqlite', format='sql', dbtype='sqlite')