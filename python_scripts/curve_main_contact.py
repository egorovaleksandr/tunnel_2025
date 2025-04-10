#!/usr/bin/env python

import os
from tunnel_constants import z_size

def convert_2d_to_3d(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file_2D, open(output_file_path, 'w') as file_3D:
        lines = file_2D.readlines()
        file_3D.write(lines[0])
        file_3D.write('3D\n')
        file_3D.write(str((z_size + 1) * int(lines[2])) + '\n')
        for line in lines[3:]:
            line = line.split()
            i_to = line[0]
            j_to = line[1]
            num = line[2]
            from_info = [(line[i], line[i+1], line[i+2]) for i in range(3, len(line), 3)]
            for k in range(-2, z_size - 1, 1):
                file_3D.write(i_to + ' ' + j_to + ' ' + str(k) + ' ' + num)
                for i_from, j_from, coef in from_info:
                    file_3D.write(' ' + i_from + ' ' + j_from + ' ' + str(k) + ' ' + str(float(coef)))
                file_3D.write('\n')

output_dir = 'contacts/'
#os.makedirs(output_dir, exist_ok=True)
print('Converting 2D contact file "curve_to_main" to 3D', end=' ')
convert_2d_to_3d(os.path.join(output_dir, "curve_to_main_2D.txt"), os.path.join(output_dir, "curve_to_main.txt"))
print('-- DONE')

print('Converting 2D contact file "main_to_curve" to 3D', end=' ')
convert_2d_to_3d(os.path.join(output_dir, "main_to_curve_2D.txt"), os.path.join(output_dir, "main_to_curve.txt"))
print('-- DONE')
