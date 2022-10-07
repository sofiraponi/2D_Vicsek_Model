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

pos = np.load('./data/pos.npy')
theta = np.load('./data/theta.npy')

T = int(config['parameters']['T'])
L = int(config['parameters']['L'])

fig, ax = plt.subplots()

def animate(i):

    ax.clear()
    ax.quiver(pos[i,0],pos[i,1],np.cos(theta[i]),np.sin(theta[i]))
    ax.set_xlim([0,L])
    ax.set_ylim([0,L])


animation = FuncAnimation(fig, animate, frames=T+1, interval=1, repeat=False)
plt.show()
