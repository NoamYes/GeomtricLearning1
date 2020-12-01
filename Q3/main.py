import numpy as np
import math
from scipy import signal
import os
import matplotlib.pyplot as plt
from array2gif import write_gif


def gradient_descent(u0, N, dx, dy, dt):

    img_list = []

    un = u0

    for n in range (0,N):

        img_list.append(un)
        un_1 = np.array(un)

        for x in range(sizex-1):
            for y in range(sizey-1):
                grad_x = un[x+1,y]-2*un[x,y]+un[x-1,y]
                grad_y = un[x,y+1]-2*un[x,y]+un[x,y-1]
                un_1[x,y] = un[x,y] + dt*(grad_x/dx**2 + grad_y/dy**2)

        un = un_1
    
    return np.array(img_list)


def heat_conv(u0, k_dim, itr, dt):

    img_list = []
    ut = u0

    for t in range(itr):

        img_list.append(ut)
        h_dim = 2*k_dim+1
        h = np.zeros((h_dim, h_dim))

        for x in range(0,h_dim):
            for y in range(0,h_dim):
                x_norm = (x-k_dim)**2+(y-k_dim)**2
                h[x, y] = (1/(math.sqrt(2*math.pi*((t+1)*dt))**2))*math.exp(-x_norm/(4*(t+1)*dt))

        # normalize h

        h = h/sum(sum(h))
        ut = signal.convolve2d(u0, h, mode='same')

    return np.array(img_list)

# def create_gif():





if __name__ == "__main__":
    
    # TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'cameraman.jpg')
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'sphinx_giz.jpeg')
    
    im = plt.imread(TEST_FILENAME)
    im_copy = np.copy(im)
    im_gray = im_copy[:,:,0] # Take only red value
    # im_gray.resize((320,320))

    [sizex, sizey] = np.shape(im_gray)

    dx = 2
    dy = 2
    N = 30
    dt = 0.2

    img_arr = gradient_descent(im_gray, N, dx, dy, dt)
    img_arr = np.repeat(img_arr[:,:,:,np.newaxis], 3, axis=3)
    OUT_FILENAME = os.path.join(os.path.dirname(__file__), 'sphinx_giz_gradient_surf.gif')
    write_gif(img_arr, OUT_FILENAME, fps=5)

    k_dim = 2
    dt = 0.1
    itr = 30

    img_arr = heat_conv(im_gray, k_dim, itr, dt)
    img_arr = np.repeat(img_arr[:,:,:,np.newaxis], 3, axis=3)
    OUT_FILENAME = os.path.join(os.path.dirname(__file__), 'sphinx_giz_conv_time.gif')
    write_gif(img_arr, OUT_FILENAME, fps=5)


# def heat_conv():
    

# u = np.zeros(im.shape[0:2])

