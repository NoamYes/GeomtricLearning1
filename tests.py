from read_off import read_off 
from write_off import write_off 
from main import Mesh
import numpy as np

(v, f) = read_off('off_files/example_off_files/sphere_s0.off')
write_off('output.off', v, f)

sphere_mesh = Mesh('off_files/example_off_files/sphere_s0.off')
vf_adj = sphere_mesh.vertex_face_adjacency()
vv_adj = sphere_mesh.vertex_vertex_adjacency()
v_deg = sphere_mesh.vertex_degree()
# plotter = sphere_mesh.render_wireframe()
colormap = np.linspace(0,256,162)
plotter = sphere_mesh.render_pointcloud(colormap)
print('end')



