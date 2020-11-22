import numpy as np
import scipy.sparse as sparse
import pyvista as pv
from read_off import read_off 



class Mesh:

    def __init__(self, off_path):
        self.v, self.f = read_off(off_path)
        self.f_v_map = np.array([[self.v[v_idx] for v_idx in face] for face in self.f[:,1:]])

    
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

    def compute_face_edges(self):
        self.f_edges_map = [[vertices[2]-vertices[1], vertices[1]-vertices[0]] for vertices in self.f_v_map]
        return self.f_edges_map

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
        plotter.add_mesh(pointcloud, render_points_as_spheres=True, color='blue') # TODO add valid colormap
        plotter.show()
        return plotter


    def render_surface(self, scalar_func):
        mesh = pv.PolyData(self.v, self.f)
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="blue", show_edges=True) # TODO add valid colormap
        plotter.show()
        return

    def face_normals(self, normalized=True):
        f_edges_map = self.compute_face_edges()
        fn = [np.cross(face[0], face[1])for face in f_edges_map]
        if normalized:
            fn = normalize_rows(fn)
        self.fn = fn
        return fn

    def face_barycenters(self):
        f_v_map = self.f_v_map
        f_bc = f_v_map.mean(1)
        self.f_bc = f_bc
        return f_bc

    def face_areas(self):
        face_normals = self.face_normals(normalized=False)
        f_areas = [L2_norm(row) for row in face_normals]
        self.f_areas = f_areas
        return f_areas

    def barycentric_vertex_areas(self):
        face_areas = self.face_areas()
        f_v_adj = self.vertex_face_adjacency()
        bc_v_areas = (1/3)*np.dot(f_v_adj.toarray(), face_areas)
        self.bc_v_areas = bc_v_areas
        return bc_v_areas

    def vertex_normals(self, normalized=True):
        face_areas = self.face_areas()
        face_normals = self.face_normals(normalized=True)
        f_v_adj = self.vertex_face_adjacency()
        face_areas = np.array(face_areas)
        face_normals = np.array(face_normals)
        f_v_adj = np.array(f_v_adj) # TODO use sparse optimize matrix

        vertex_normals = f_v_adj.dot(face_areas).dot(face_areas.T).dot(face_normals)
        if normalized:
            vertex_normals = normalize_rows(vertex_normals)
        self.v_n = vertex_normals
        return vertex_normals

def normalize_rows(arr):
    return [row/L2_norm(row) for row in arr]

def L2_norm(arr):
    return np.sqrt((arr * arr).sum(axis=0))