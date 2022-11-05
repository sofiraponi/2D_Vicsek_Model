#=======================================================================
# Author: Sofia Raponi
# Date: 05 October, 2022
#
# Vicsek_Model
#
# Aim: To define the functions needed to simulate the 2D Viscek Model.
#=======================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

def InitialConfiguration(num_part,space_dim):

    """
    This function creates random initial positions and orientations of the particles.

    Parameters
        num_part : number of particles
        space_dim : linear dimension of space

    Returns:
        Initial configuration of the particles (config).
    """

    # Generate random coordinates of particles between 0 and space_dim
    x = np.random.rand(num_part)*space_dim
    y = np.random.rand(num_part)*space_dim

    assert all(i < space_dim and i >= 0 for i in x)
    assert all(i < space_dim and i >= 0 for i in y)

    # Generate random orientation of particles between -π and π
    theta = np.pi*(2*np.random.rand(num_part)-1)

    config = np.array([x,y,theta])

    return config

def VelocityCalculation(vel_mod,theta):

    """
    This funtion calculates the particles velocity.

    Parameters
        vel_mod : velocity modulus
        theta: particles orientation

    Returns:
        Velocity components (vx,vy).
    """

    vx = vel_mod*np.cos(theta)
    vy = vel_mod*np.sin(theta)

    vel = np.array([vx,vy])

    return vel

def FindNeighbors(positions,int_radius,particle,space_dim):

    """
    This function finds the neighbors within a circle of radius int_radius aroud a reference particle satisfying periodic boundary conditions.

    Parameters:
        positions: particles positions (N X 2 array)
        int_radius: interaction int_radius
        particle: reference particle position
        space_dim: linear dimension of space

    Returns:
    List of neighbors indeces inds.
    """

    tree=KDTree(positions,boxsize=space_dim)
    inds = tree.query_ball_point(particle,int_radius)
    inds=inds[0]

    return inds

def NeighborsMeanAngle(config,int_radius,space_dim):

    """
    This function calculates the mean orientation of the neighbor partcicles within a circle of radius int_radius around each of the particles.

    Parameters
        config: previous particles configuration
        int_radius: interaction radius
        space_dim: linear dimension of space

    Returns:
        Mean orientation of the particles.
    """

    mean_theta=config[2].copy()

    pos=np.array([config[0],config[1]]).T

    for i in range(0,len(config[2])):

        # Find the neighbors of each particle within the interaction radius int_radius satisfying periodic boundary conditions
        neighbors = FindNeighbors(pos,int_radius,[pos[i]],space_dim)

        mean_sin=np.mean(np.sin(config[2][neighbors]))
        mean_cos=np.mean(np.cos(config[2][neighbors]))

        # Calculate the mean orientation of the neighbor particles within int_radius
        mean_theta[i] = np.arctan2(mean_sin,mean_cos)

    return mean_theta

def ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step):

    """
    This function updates the particles position and orienation.

    Parameters
        config: previous particles configuration
        vel: particles velocity
        int_radius: interaction radius
        noise_ampl: noise amplituse
        space_dim: linear dimension of space
        time_step: time step

    Returns:
        Updated configuration of the particles (config).
    """

    new_config=config.copy()

    # Update particles position
    new_config[0] = config[0] + vel[0]*time_step
    new_config[1] = config[1] + vel[1]*time_step

    # Impose periodic boundary conditions
    new_config[0] = new_config[0] % space_dim
    new_config[1] = new_config[1] % space_dim

    assert all(i < space_dim and i >= 0 for i in new_config[0])
    assert all(i < space_dim and i >= 0 for i in new_config[1])

    # Calculate the mean orientation of particles within int_radius satisfying periodic boundary conditions
    mean_theta =  NeighborsMeanAngle(new_config,int_radius,space_dim)

    # Update particles orientation
    new_config[2] = mean_theta + noise_ampl*(np.random.rand(len(new_config[2]))-0.5)

    return new_config

def OrderParameter(theta):

    """
    This function calculates the order parameter.

    Parameters
        theta: particles orientation

    Returns:
        Order parameter phi.
    """

    sx = np.sum(np.cos(theta))
    sy = np.sum(np.sin(theta))
    phi = ((sx)**2 + (sy)**2)**(0.5)/len(theta)

    phi=round(phi,10)

    assert phi >= 0
    assert phi <= 1

    return phi

def Simulate(config,vel,int_radius,noise_ampl,space_dim,time_step,num_steps,vel_mod):

    """
    This function updates the particles position and orienation and calculates the order parameter num_steps times.

    Parameters
        init_config: previous particles configuration
        vel: particles velocity
        int_radius: interaction radius
        noise_ampl: noise amplituse
        space_dim: linear dimension of space
        time_step: time step
        num_steps: number of steps
        vel_mod: velocity modulus

    Returns:
        Position of the particles (position_updates), orientation of the particles (position_updates) at each step.
    """
    #Initial positions and orientations
    init_config=config.copy()
    position_updates=[[init_config[0],init_config[1]]]
    theta_updates=[init_config[2]]

    # Main loop
    for i in range(num_steps):

        # Configuration update
        config = ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step)
        new_config=config.copy()

        # Update velocity
        vel = VelocityCalculation(vel_mod,new_config[2])

        # Save updated positions and orientations
        position_updates.append([new_config[0],new_config[1]])
        theta_updates.append(new_config[2])

    return position_updates, theta_updates
