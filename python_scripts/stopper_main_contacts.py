#!/usr/bin/env python

import os
from tunnel_constants import N_x, N_y, N_z, n_x, n_y, n_z, d_z, d_x, d_y, R1, R2

print('Creating stopper and main contacts', end=' ')

in_tunnel = set()
for i in range(n_x):
    for j in range(n_y):
        if (i - n_x / 2)**2 + (j - n_y / 2)**2 >= 4 * R1**2 and (i - n_x / 2)**2 + (j - n_y / 2)**2 <= 4 * R2**2:
            in_tunnel.add((i, j))    

output_dir = 'contacts/'
#os.makedirs(output_dir, exist_ok=True)

N = 4*(n_x + 4)*(n_y + 4) + 4*(n_x + 4)*n_z + 2*n_y*n_z - len(in_tunnel) * 2

with open(os.path.join(output_dir, "main_to_stopper.txt"), 'w') as file:
    file.write('main\n3D\n')
    file.write(str(N) + '\n')
    
    # front
    for i in range(-2, n_x + 2):
        for j in range(-2, n_y + 2):
            if (i, j) in in_tunnel:
                continue
            file.write(str(i) + ' ' + str(j) + ' ' + str(-2) + ' ' + str(1) + ' ' +
                       str(i + d_x) + ' ' + str(j + d_y) + ' ' + str(d_z - 2) + ' ' + str(1) + '\n')
            file.write(str(i) + ' ' + str(j) + ' ' + str(-1) + ' ' + str(1) + ' ' +
                       str(i + d_x) + ' ' + str(j + d_y) + ' ' + str(d_z - 1) + ' ' + str(1) + '\n')
    
    # back
    for i in range(-2, n_x + 2):
        for j in range(-2, n_y + 2):
            file.write(str(i) + ' ' + str(j) + ' ' + str(n_z + 0) + ' ' + str(1) + ' ' +
                       str(i + d_x) + ' ' + str(j + d_y) + ' ' + str(d_z + n_z + 0) + ' ' + str(1) + '\n')
            file.write(str(i) + ' ' + str(j) + ' ' + str(n_z + 1) + ' ' + str(1) + ' ' +
                       str(i + d_x) + ' ' + str(j + d_y) + ' ' + str(d_z + n_z + 1) + ' ' + str(1) + '\n')
    
    # right
    for j in range(0, n_y):
        for k in range(0, n_z):
            file.write(str(n_x + 0) + ' ' + str(j) + ' ' + str(k) + ' ' + str(1) + ' ' +
                       str(n_x + d_x + 0) + ' ' + str(j + d_y) + ' ' + str(k + d_z) + ' ' + str(1) + '\n')
            file.write(str(n_x + 1) + ' ' + str(j) + ' ' + str(k) + ' ' + str(1) + ' ' +
                       str(n_x + d_x + 1) + ' ' + str(j + d_y) + ' ' + str(k + d_z) + ' ' + str(1) + '\n')
    
    # left
    for j in range(0, n_y):
        for k in range(0, n_z):
            file.write(str(-1) + ' ' + str(j) + ' ' + str(k) + ' ' + str(1) + ' ' +
                       str(d_x - 1) + ' ' + str(j + d_y) + ' ' + str(k + d_z) + ' ' + str(1) + '\n')
            file.write(str(-2) + ' ' + str(j) + ' ' + str(k) + ' ' + str(1) + ' ' +
                       str(d_x - 2) + ' ' + str(j + d_y) + ' ' + str(k + d_z) + ' ' + str(1) + '\n')
    
    # up
    for i in range(-2, n_x+2):
        for k in range(0, n_z):
            file.write(str(i) + ' ' + str(n_y+0) + ' ' + str(k) + ' '+ str(1)+  ' '+ 
                       str(i+d_x)+  ' '+str(d_y+n_y+0)+  ' '+str(k+d_z)+  ' '+str(1)+ '\n')
            file.write(str(i)+  ' '+str(n_y+1)+  ' '+str(k)+  ' '+str(1)+  ' '+ 
                       str(i+d_x)+  ' '+str(d_y+n_y+1)+  ' '+str(k+d_z)+  ' '+str(1)+ '\n')
    
    # down
    for i in range(-2, n_x+2):
        for k in range(0, n_z):
            file.write(str(i)+  " "+str(-1)+ " "+str(k)+ " "+str(1)+ " "+ 
                       str(i+d_x)+ " "+str(d_y-1)+ " "+str(k+d_z)+ " "+str(1)+ '\n')
            file.write(str(i)+ " "+str(-2)+ " "+str(k)+ " "+str(1)+ " "+ 
                       str(i+d_x)+ " "+str(d_y-2)+ " "+str(k+d_z)+ " "+str(1)+ '\n')

with open(os.path.join(output_dir, "stopper_to_main.txt"), 'w') as file:
    file.write('stopper\n3D\n')
    file.write(str(n_x * n_y * n_z - 3 * len(in_tunnel))+'\n')
    for i in range(n_x):
        for j in range(n_y):
            for k in range(n_z):
                if k > 2 or (i, j) not in in_tunnel:
                    file.write(str(i+d_x)+' '+str(j+d_y)+' '+str(k+d_z)+' '+str(1)+' '+ 
                               str(i)+' '+str(j)+' '+str(k)+' '+str(1)+'\n')

print('-- DONE')
