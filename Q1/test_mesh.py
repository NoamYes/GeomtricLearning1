
import matplotlib.pyplot as plt
from mesh import Mesh
import numpy as np

def test_mesh(mesh):
    vf_adj = mesh.vertex_face_adjacency()
    vv_adj = mesh.vertex_vertex_adjacency()
    v_deg = mesh.vertex_degree()
    plotter = mesh.render_wireframe().show()

    scalar_map = mesh.vertex_degree()
    plotter = mesh.render_pointcloud(scalar_map).show()
    scalar_map = np.random.rand(mesh.faces.shape[0])
    mesh.render_surface(scalar_map).show()
    fn = mesh.face_normals(normalized=True)
    f_bc = mesh.face_barycenters()
    fa = mesh.face_areas()
    bc_areas = mesh.barycentric_vertex_areas()
    v_n = mesh.vertex_normals()
    mesh.gaussian_curvature()
    mesh.show_normals(scalar_map).show()
    mesh.show_normals_normalized(scalar_map).show()
    mesh.show_face_areas().show()
    # mesh.show_vertex_areas().show()
    mesh.show_vertex_centroids().show()



print('end')



