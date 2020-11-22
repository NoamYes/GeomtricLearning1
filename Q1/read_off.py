
import numpy as np

def read_off(path):

    with open(path) as f:
        str_lines = f.readlines()
        if str_lines[0] != 'OFF\n':
            print('File is not of OFF type')
            return
        numbers_line = [int(n) for n in (str_lines[1].split())]
        [n_vertices, n_faces, n_edges] = numbers_line
        vertices = [[float(elem) for elem in (line.split())] for line in str_lines[2:n_vertices+2]]
        faces = [[int(elem) for elem in (line.split())] for line in str_lines[n_vertices+2:n_vertices+n_faces+2]]
        v = np.array(vertices)
        f = np.array(faces)

    return v, f