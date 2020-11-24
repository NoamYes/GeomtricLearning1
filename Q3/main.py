import numpy as np
import os
import matplotlib.pyplot as plt

TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'sphinx_giz.jpeg')
im = plt.imread(TEST_FILENAME)
im_gray = im
u = np.zeros(im.shape[0:2])
print('ended')
