#=======================================================================
# Author: Sofia Raponi
# Date: 07 October, 2022
#
# Animation
#
# Aim: Model animation
#=======================================================================

import configparser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Read configuration file
config=configparser.ConfigParser()
config.read('settings.ini')

# Import data and parameters
phi = np.load('./data/phi.npy')
position = np.load('./data/position.npy')
theta = np.load('./data/theta.npy')

T = int(config['parameters']['T'])
L = int(config['parameters']['L'])

# Create figure
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10, 5))

fig.suptitle("v$_0$ = 0.2, η = 0.1, R$_0$ = 1.0, dt = 1.0, N = 200")

# Prepare order parameter real time plot
t = np.linspace(0, T+1, T+1)

line, = ax2.plot(t, phi, color='r')
ax2.set_ylabel("Order Parameter")
ax2.set_xlabel("Frame")
ax2.grid()

# Create animation
def animate(i):

    ax1.clear()
    ax1.quiver(position[i,0],position[i,1],np.cos(theta[i]),np.sin(theta[i]))
    ax1.set_xlim([0,L])
    ax1.set_ylim([0,L])

    line.set_data(t[:i], phi[:i])

animation = FuncAnimation(fig, animate, frames=T+1, interval=50, repeat=False)

plt.show()

# Save animation
animation.save('animation.gif', writer = 'pillow', fps = T+1)
