from read_off import read_off 
from write_off import write_off 
import matplotlib.pyplot as plt
from main import Mesh
import numpy as np

(v, f) = read_off('off_files/example_off_files/sphere_s0.off')
write_off('output.off', v, f)

sphere_mesh = Mesh('off_files/example_off_files/sphere_s0.off')
# vf_adj = sphere_mesh.vertex_face_adjacency()
# vv_adj = sphere_mesh.vertex_vertex_adjacency()
# v_deg = sphere_mesh.vertex_degree()
# plotter = sphere_mesh.render_wireframe()
# boring_cmap = plt.cm.get_cmap("viridis", 162)

# plotter = sphere_mesh.render_pointcloud(boring_cmap)
# sphere_mesh.render_surface(boring_cmap)
# fn = sphere_mesh.face_normals(normalized=True)
# f_bc = sphere_mesh.face_barycenters()
# fa = sphere_mesh.face_areas()
# bc_areas = sphere_mesh.barycentric_vertex_areas()
# v_n = sphere_mesh.vertex_normals()
sphere_mesh.gaussian_curvature()


print('end')



