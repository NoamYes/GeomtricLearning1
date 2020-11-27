from read_off import read_off 
from write_off import write_off 
import matplotlib.pyplot as plt
from mesh import Mesh
import numpy as np

from test_mesh import test_mesh

off_files = ['sphere_s0.off', 'cat.off', 'torus_fat_r2.off']
# off_files = ['cat.off']
for off_file in off_files:

    # (v, f) = read_off('off_files/example_off_files/' + off_file)
    # write_off('output.off', v, f)
    mesh = Mesh('off_files/example_off_files/' + off_file)
    test_mesh(mesh)
