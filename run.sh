#!/bin/bash

rm -r bins
rm -r contacts
rm erased_nodes.txt
rm -r results
rm -r tunnel_confs/tunnel_*
rm -r tunnel_confs/curve_grid_*
mkdir bins
mkdir contacts
mkdir results
mkdir results/vtk
mkdir results/receivers
mkdir results/seismogramms

python3 python_scripts/gen_tunnel_confs.py
python3 python_scripts/gen_data_2D.py
rect_2024-04-15_13_58/rect/build/interpolation contact_configs/curve_to_main_2D.cfg
rect_2024-04-15_13_58/rect/build/interpolation contact_configs/main_to_curve_2D.cfg
python3 python_scripts/gen_data.py
python3 python_scripts/curve_main_contact.py
python3 python_scripts/stopper_main_contacts.py
python3 python_scripts/gen_erased_nodes.py
rect_2024-04-15_13_58/rect/build/contact_finder contact_configs/main_layer_contact.cfg
rect_2024-04-15_13_58/rect/build/contact_finder contact_configs/layer_main2_contact.cfg
rect_2024-04-15_13_58/rect/build/interpolation contact_configs/curve_to_stopper.cfg
rect_2024-04-15_13_58/rect/build/interpolation contact_configs/stopper_to_curve.cfg
for i in tunnel_confs/tunnel_*
do
    rect_2024-04-15_13_58/rect/build/rect "$i"
done
#rect_2024-04-15_13_58/rect/build/rect tunnel_confs/without.conf
