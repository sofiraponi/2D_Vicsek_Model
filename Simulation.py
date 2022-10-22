#=======================================================================
# Author: Sofia Raponi
# Date: 06 October, 2022
#
# Simulation
#
# Aim: To simulate the 2D Viscek Model.
#=======================================================================

import configparser
import numpy as np
import matplotlib.pyplot as plt
import Vicsek_Model

# Read configuration file
config=configparser.ConfigParser()
config.read('settings.ini')

# Import model parameters
v0 = float(config['parameters']['v0'])    # Velocity modulus
eta = float(config['parameters']['eta'])  # Noise amplitude
R0 = float(config['parameters']['R0'])    # Interaction radius
dt = float(config['parameters']['dt'])    # Time step
N = int(config['parameters']['N'])        # Number of particles
L = int(config['parameters']['L'])        # Dimension of space
T = int(config['parameters']['T'])        # Number of steps

# Import local paths
phi_path = config['paths']['phi']
position_path = config['paths']['position']
theta_path = config['paths']['theta']

# Define data arrays
phi_data=np.empty(T+1)
position_data=np.empty([T+1,2,N])
theta_data=np.empty([T+1,1,N])

# Calculate initial configuration (position and orientation)
config = Vicsek_Model.InitialConfiguration(N,L)

# Calculate initial velocity
vel = Vicsek_Model.VelocityUpdate(v0,config[2])

# Save initial configuration
position_data[0] = config[0], config[1]
theta_data[0] = config[2]

# Calculate initial order parameter
phi_data[0] = Vicsek_Model.OrderParameter(config[2],N)

# Main loop
for i in range(T):

    # Update configuration
    config = Vicsek_Model.ConfigurationUpdate(config,vel,R0,eta,N,L,dt)

    # Update velocity
    vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    # Calculate order parameter
    phi_data[i+1]=Vicsek_Model.OrderParameter(config[2],N)

    # Save current configuration
    position_data[i+1] = config[0], config[1]
    theta_data[i+1]= config[2]

# Save particles configuration and order parameter evolution
np.save(position_path,position_data)
np.save(theta_path,theta_data)
np.save(phi_path,phi_data)
