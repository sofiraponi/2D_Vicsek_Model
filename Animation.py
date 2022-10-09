#==============================================================
#Author: Sofia Raponi
#Date: 07 October, 2022
#
#  Animation
#
#  Aim: Model animation
#
#==============================================================

import configparser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Read configuration file

config=configparser.ConfigParser()
config.read('settings.ini')

phi = np.load('./data/phi.npy')
pos = np.load('./data/pos.npy')
theta = np.load('./data/theta.npy')

T = int(config['parameters']['T'])
L = int(config['parameters']['L'])

fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10, 5))

t = np.linspace(0, T+1, T+1)

line, = ax2.plot(t, phi, color='r')
ax2.set_title("Order Parameter")
ax2.set_ylabel("φ")
ax2.set_xlabel("Frame")
ax2.grid()


def animate(i):

    ax1.clear()
    ax1.quiver(pos[i,0],pos[i,1],np.cos(theta[i]),np.sin(theta[i]))
    ax1.set_xlim([0,L])
    ax1.set_ylim([0,L])

    line.set_data(t[:i], phi[:i])

animation = FuncAnimation(fig, animate, frames=T+1, interval=50, repeat=False)
plt.show()
animation.save('animation.gif',writer = 'pillow', fps = T+1)
