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
import sys
from sys import argv
import matplotlib.pyplot as plt
import Vicsek_Model

# Read configuration file
config=configparser.ConfigParser()
config.read(sys.argv[1])

# Import model parameters
v0 = float(config['parameters']['vel_mod'])       # Velocity modulus
eta = float(config['parameters']['noise_ampl'])   # Noise amplitude
R0 = float(config['parameters']['int_radius'])    # Interaction radius
dt = float(config['parameters']['time_step'])     # Time step
N = int(config['parameters']['num_part'])         # Number of particles
L = float(config['parameters']['space_dim'])      # Linear dimension of system space
Ns = int(config['parameters']['num_steps'])       # Number of steps
seed = int(config['parameters']['seed'])          # Random seed

# Import local paths
phi_path = config['paths']['order_param']
position_path = config['paths']['position']
theta_path = config['paths']['orientation']

# Initialization
np.random.seed(seed)

# Define data arrays
phi_data=np.empty(Ns+1)
position_data=np.empty([Ns+1,2,N])
theta_data=np.empty([Ns+1,1,N])

# Calculate initial configuration (position and orientation)
config = Vicsek_Model.InitialConfiguration(N,L)

# Calculate initial velocity
vel = Vicsek_Model.VelocityCalculation(v0,config[2])

# Save initial configuration
position_data[0] = config[0], config[1]
theta_data[0] = config[2]

# Calculate initial order parameter
phi_data[0] = Vicsek_Model.OrderParameter(config[2])

# Main loop
for i in range(Ns):

    # Update configuration
    config = Vicsek_Model.ConfigurationUpdate(config,vel,R0,eta,N,L,dt)

    # Update velocity
    vel = Vicsek_Model.VelocityCalculation(v0,config[2])

    # Calculate order parameter
    phi_data[i+1]=Vicsek_Model.OrderParameter(config[2])

    # Save current configuration
    position_data[i+1] = config[0], config[1]
    theta_data[i+1]= config[2]

# Save particles configuration and order parameter evolution
np.save(position_path,position_data)
np.save(theta_path,theta_data)
np.save(phi_path,phi_data)
