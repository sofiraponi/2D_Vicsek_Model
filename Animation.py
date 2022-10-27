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
import sys
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Read configuration file
config=configparser.ConfigParser()
config.read(sys.argv[1])

# Import data and parameters
phi = np.load('./data/phi.npy')
position = np.load('./data/position.npy')
theta = np.load('./data/theta.npy')

v0 = float(config['parameters']['v0'])    # Velocity modulus
eta = float(config['parameters']['eta'])  # Noise amplitude
R0 = float(config['parameters']['R0'])    # Interaction radius
dt = float(config['parameters']['dt'])    # Time step
N = int(config['parameters']['N'])        # Number of particles
L = float(config['parameters']['L'])      # Linear dimension of system space
T = int(config['parameters']['T'])        # Number of steps

# Create figure
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10, 5))
fig.suptitle("v$_0$ = {}, η = {}, R$_0$ = {}, dt = {}, N = {}".format(v0,eta,R0,dt,N))

t = np.linspace(0, T+1, T+1)

# Prepare order parameter real time plot
line, = ax2.plot(t, phi, color='r')
ax2.set_ylim([0,1.1])
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
writer = PillowWriter(fps = T+1)
animation.save('animation.gif', writer = writer)
