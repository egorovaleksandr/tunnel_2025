#!/usr/bin/env python

import os
from tunnel_constants import n_x, n_y, R1, R2, z

print('Generating erased nodes for stopper', end=' ')

erased = set()

for i in range(n_x):
    for j in range(n_y):
        if (i - n_x / 2)**2 + (j - n_y / 2)**2 > 4 * R2**2:
            erased.add((i, j))

output_dir = './'
with open(os.path.join(output_dir, 'erased_nodes.txt'), 'w') as file:
    file.write(str(3 * len(erased)) + '\n')
    for i, j in erased:
        for k in z:
            file.write(str(i) + ' ' + str(j) + ' ' + str(k) + '\n')

print('-- DONE')
