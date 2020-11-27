
import matplotlib.pyplot as plt
from mesh import Mesh
import numpy as np

def test_mesh(mesh):
    vf_adj = mesh.vertex_face_adjacency()
    vv_adj = mesh.vertex_vertex_adjacency()
    v_deg = mesh.vertex_degree()
    # plotter = mesh.render_wireframe()

    # scalar_map = mesh.vertex_degree()
    # plotter = mesh.render_pointcloud(scalar_map)
    # scalar_map = np.random.rand(mesh.faces.shape[0])
    # mesh.render_surface(scalar_map)
    # fn = mesh.face_normals(normalized=True)
    # f_bc = mesh.face_barycenters()
    # fa = mesh.face_areas()
    # bc_areas = mesh.barycentric_vertex_areas()
    # v_n = mesh.vertex_normals()
    mesh.gaussian_curvature()



print('end')



