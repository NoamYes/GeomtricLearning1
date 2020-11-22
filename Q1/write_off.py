
import numpy as np

def write_off(path, v, f):

    with open(path, "w") as file:

        lines = ['OFF\n']
        n_vertices = len(v)
        n_faces = len(f)
        lines += [" ".join([str(elem) for elem in [n_vertices, n_faces, 0]]) + '\n']
        v_lines = [" ".join([str(e) for e in vertice]) for vertice in v]
        f_lines = [" ".join([str(len(face))] + [str(e) for e in face]) for face in f]
        lines += [vertice_str + '\n' for vertice_str in v_lines]
        lines += [face_str + '\n' for face_str in f_lines]
        file.writelines(lines)
