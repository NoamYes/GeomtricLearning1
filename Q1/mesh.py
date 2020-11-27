import numpy as np
from matplotlib.pyplot import cm
import scipy.sparse as sparse
import pyvista as pv
from pyvista import examples
from read_off import read_off 



class Mesh:

    def __init__(self, off_path):
        self.v, self.faces = read_off(off_path)
        self.f = self.faces[:,1:]
        self.f_v_map = np.array([[self.v[v_idx] for v_idx in face] for face in self.f])

    
    def vertex_face_adjacency(self):
        v_idx = 1+np.arange(len(self.v))
        adj = [np.isin(v_idx, f) for f in self.f]
        self.vf_a = np.array(adj).transpose()
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
        return np.array(res)

    def render_wireframe(self):
        surf = pv.PolyData(self.v, self.faces)
        plotter = pv.Plotter()
        plotter.add_mesh(surf, style='wireframe', color='blue')
        plotter.show(auto_close=False)
        return plotter

    def render_pointcloud(self, scalar_func, cmap_name=None):
        pointcloud = pv.PolyData(self.v)
        plotter = pv.Plotter()
        plotter.add_mesh(pointcloud, render_points_as_spheres=True, scalars=scalar_func, cmap=cm.get_cmap(cmap_name)) 
        plotter.show(auto_close=False)
        return plotter


    def render_surface(self, scalar_func, cmap_name=None):
        mesh = pv.PolyData(self.v, self.faces)
        plotter = pv.Plotter()
        # scalar_map = scalar_func(np.max(self.faces, axis=1))
        plotter.add_mesh(mesh, show_edges=True, scalars=scalar_func, cmap=cm.get_cmap(cmap_name)) 
        plotter.show(auto_close=False)
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
        f_areas = [0.5*L2_norm(row) for row in face_normals]
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

    def gaussian_curvature(self):
        self.gauss_curv = np.zeros((self.v.shape[0],))
        vf_a = self.vertex_face_adjacency()
        v_areas = self.barycentric_vertex_areas()

        for i in range (self.v.shape[0]):
            f_inds = sparse.find(vf_a[i,:])[1]
            v_inds = self.f[f_inds]
            v = self.v[i]
            v_coords = self.v[v_inds[v_inds != i+1].reshape((-1,2)),:]
            my_v = self.v[i].reshape((1,1,v.shape[0]))
            f_edges = v_coords - my_v
            sum_angles = sum([compute_angle(edges[0], edges[1]) for edges in f_edges])
            self.gauss_curv[i] = (2*np.pi - sum_angles)/v_areas[i]
        
        print('achieved')
            
    def show_normals(self):
        face_normals = self.face_normals()
        face_bc = self.face_barycenters()
        
        

def normalize_rows(arr):
    return [row/L2_norm(row) for row in arr]

def L2_norm(arr):
    return np.sqrt((arr * arr).sum(axis=0))

def compute_angle(vec1, vec2):
    cos_ang = np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
    return np.arccos(cos_ang)