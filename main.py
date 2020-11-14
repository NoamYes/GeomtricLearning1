import numpy as np
import scipy.sparse as sparse
import pyvista as pv
from read_off import read_off 


class Mesh:

    def __init__(self, off_path):
        self.v, self.f = read_off(off_path)
    
    def vertex_face_adjacency(self):
        v_idx = 1+np.arange(len(self.v))
        adj = [np.isin(v_idx, f) for f in self.f]
        self.vf_a = sparse.lil_matrix(adj).transpose()
        return sparse.lil_matrix(adj).transpose()

    def vertex_vertex_adjacency(self):
        vf_adj = self.vertex_face_adjacency()
        vf_adj = vf_adj.astype(int)
        common_face_num = np.dot(vf_adj, vf_adj.transpose())
        common_face_bool = common_face_num >= 2 # Triangle sides - 1
        common_face_bool.setdiag(False)
        self.vv_a = common_face_bool
        return self.vv_a

    def vertex_degree(self):
        vv_a = self.vertex_vertex_adjacency()
        res = vv_a.sum(axis=0)
        return res

    def render_wireframe(self):
        plotter = pv.Plotter()
        plotter.add_mesh(self.v, style='wireframe')
        plotter.show()
        return plotter

    def render_pointcloud(self, scalar_func):
        pointcloud = pv.PolyData(self.v)
        plotter = pv.Plotter()
        plotter.add_mesh(pointcloud, render_points_as_spheres=True, cmap=scalar_func)
        plotter.show()
        return plotter
