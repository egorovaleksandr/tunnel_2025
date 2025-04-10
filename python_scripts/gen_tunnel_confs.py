from tunnel_constants import x_size, y_size, z_size

print('Generating tunnel configs', end=' ')
#source_z = [50 + i * 2 for i in range(24)]
#dist = [19.2, 20.4, 21.4, 22.9, 24.2, 25.5, 26.8, 28.1, 29.4, 30.7, 32, 33.3, 34.5, 35.7, 37, 38.3, 39.6, 40.9, 42]
#dist = [19, 20.5, 21.5, 23, 24, 25.5, 27, 28, 29.5, 30.5, 32, 33.5, 34.5, 35.5, 37, 38.5, 39.5, 41, 42]
source_z = [50 + 2 * i for i in range(24)]

with open('tunnel_confs/template_2D.conf', 'r') as conf_2D, open('tunnel_confs/template_tunnel.conf', 'r') as conf_3D: 
    t_2D = conf_2D.read() 
    t_2D = t_2D.replace("$curve_x_sz$", str(x_size))
    t_2D = t_2D.replace("$curve_y_sz$", str(y_size))
    open('tunnel_confs/curve_grid_2D.conf', 'w+').write(t_2D)
    
    t_3D = conf_3D.read()
    t_3D = t_3D.replace("$curve_x_sz$", str(x_size))
    t_3D = t_3D.replace("$curve_y_sz$", str(y_size))
    t_3D = t_3D.replace("$curve_z_sz$", str(z_size))
    for z in source_z:
        t = t_3D.replace("$Z$", str(z))
        open('tunnel_confs/tunnel_' + str(z) + '.conf', 'w+').write(t)

print('-- DONE')
