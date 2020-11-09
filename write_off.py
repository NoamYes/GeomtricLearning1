import meshio

def write_off(path):
    mesh = meshio.read(path)
    return mesh