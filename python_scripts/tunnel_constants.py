#!/usr/bin/env python

#tunnel geometry
R1 = 6  # 6
R2 = 7  # 7
L = 100 #100

#tunnel grid sizes
x_size = 300
y_size = 10
z_size = 201 # 201

#erased z coords
z   = [-2, -1, 0]

#main grid sizes
N_x = 201
N_y = 201
N_z = 301

#stopper grid sizes
n_x = 33
n_y = 33
n_z = 5

#main-stopper coords shifts
d_z = 200
d_x = (N_x - n_x)//2
d_y = (N_y - n_y)//2
