import numpy as np
import scipy.sparse as sparse
from read_off import read_off 

class Mesh:

    def __init__(self, off_path):
        self.v, self.f = read_off(off_path)
    
    def vertex_face_adjacency(self):
        v_idx = 1+np.arange(len(self.v))
        adj = [np.isin(v_idx, f) for f in self.f]
        return sparse.csr_matrix(adj).transpose()

    def vertex_vertex_adjacency(self):
        v_idx = 1+np.arange(len(self.v))
        adj = [np.isin(v_idx, f) for f in self.f]
        return sparse.csr_matrix(adj).transpose()