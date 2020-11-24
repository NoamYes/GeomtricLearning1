import pyvista as pv
import numpy as np

# Make data
u = np.arange(-25, 25, 0.05)
v = np.arange(-25, 25, 0.05)
u, v = np.meshgrid(u, v)

div = (u**2 + v**2 +1)
x = 2*u/div
y = 2*v/div
z = (u**2 + v**2 - 1)/div

points = np.array([x, y, z]).T

mesh = pv.StructuredGrid(x, y, z)

plotter = pv.Plotter()
plotter.add_mesh(mesh, color="orange")
plotter.show()