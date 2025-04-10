#!/usr/bin/env python

import numpy as np
import os
from tunnel_constants import R1, R2, L, x_size, y_size, z_size

print('Generating 3D tunnel bins', end=' ')

r_vals = np.linspace(R1, R2, y_size)
angle = np.linspace(2 * np.pi, 0, x_size)
z_vals = np.linspace(0, L, z_size)

X = []
Y = []
Z = []

for iz in range(z_size):
    Z.append(np.ones(y_size * x_size) * z_vals[iz])
    for r in r_vals:
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        X.append(x)
        Y.append(y)

output_dir = 'bins/'
#os.makedirs(output_dir, exist_ok=True)

np.hstack(X).astype('f').tofile(os.path.join(output_dir, 'x.bin'))
np.hstack(Y).astype('f').tofile(os.path.join(output_dir, 'y.bin'))
np.hstack(Z).astype('f').tofile(os.path.join(output_dir, 'z.bin'))
print('-- DONE')
