import meshio
import numpy

def read_off(path):

    with open(path) as f:

        lines = f.read().split()
    v = numpy.array([n_vertices,3],dtype=double)
    f = numpy.array([n_faces,3],dtype=int)
    return mesh