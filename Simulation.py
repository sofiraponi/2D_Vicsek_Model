#==============================================================
#Author: Sofia Raponi
#Date: 06 October, 2022
#
# Simulation
#
#  Aim: To simulate Viscek Model for 2 dimensions.
#
#==============================================================

import configparser
import numpy as np
import matplotlib.pyplot as plt
import Vicsek_Model

# Read configuration file

config=configparser.ConfigParser()
config.read('settings.ini')

# Model parameters

v0 = float(config['parameters']['v0'])    # Constant velocity of particles
eta = float(config['parameters']['eta'])  # Constant noise amplitude [0,1]
R0 = float(config['parameters']['R0'])    # Interaction radius
dt = float(config['parameters']['dt'])    # Time step
N = int(config['parameters']['N'])        # Number of particles
L = int(config['parameters']['L'])        # Dimension of system
T = int(config['parameters']['T'])        # Number of steps

phi_path = config['paths']['phi']
pos_path = config['paths']['pos']
vel_path = config['paths']['vel']

phi=np.empty(T+1)
data_pos=np.empty([T+1,2,N])
data_vel=np.empty([T+1,2,N])

# Initial configuration

config = Vicsek_Model.InitialConfiguration(N,L)

# Initial velocity

vel = Vicsek_Model.VelocityUpdate(v0,config[2])

data_pos[0] = config[0], config[1]
data_vel[0] = vel

# Initial order parameter

phi[0] = Vicsek_Model.OrderParameter(config[2],N)

# Main loop

for i in range(T):

    config = Vicsek_Model.ConfigurationUpdate(config,vel,R0,eta,N,L,dt)

    vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    phi[i+1]=Vicsek_Model.OrderParameter(config[2],N)

    data_pos[i+1] = config[0], config[1]
    data_vel[i+1]= vel

# Save particles confoguration and order parameter evolution

np.save(pos_path,data_pos)
np.save(vel_path,data_vel)
np.save(phi_path,phi)
