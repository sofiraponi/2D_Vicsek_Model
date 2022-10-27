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
import math

def InitialConfiguration(N,L):

    """

    This function creates random initial positions and orientations of the N particles.

    Parameters
        N : number of particles
        L : linear dimension of space

    Returns:
        Initial configuration of the N particles.

    Raise:
        ValueError if the initial coordinates (x,y) of the N particles are out of the system space of linear dimension L.

    """

    # Initialization
    np.random.seed(3)

    # Generate random coordinates of particles between 0 and L
    x = np.random.rand(N)*L
    y = np.random.rand(N)*L

    if not all(i < L and i >= 0 for i in x):
        raise ValueError('The x coordinate of each particle must be between 0 and {} but at least one is out of range!'.format(L))

    if not all(i < L and i >= 0 for i in y):
        raise ValueError('The y coordinate of each particle must be between 0 and {} but at least one is out of range!'.format(L))

    # Generate random orientation of particles between -π and π
    theta = np.pi*(2*np.random.rand(N)-1)

    config = np.array([x,y,theta])

    return config

def VelocityUpdate(v0,theta):

    """

    This funtion updates the particles velocity.

    Parameters
        v0 : velocity modulus
        theta: particles orientation

    Returns:
        Velocity components (vx,vy).

    """

    vx = v0*np.cos(theta)
    vy = v0*np.sin(theta)

    vel = np.array([vx,vy])

    return vel

def NeighborsMeanAngle(config,N,R0):

    """

    This function calculates the mean orientation of the neighbor partcicles within a circle of radius R0 around each of the N particles.

    Parameters
        config: previous particles configuration
        N: number of particles
        R0: interaction radius

    Returns:
        Mean orientation of the N particles.

    """

    mean_theta=config[2]

    for i in range(0,N):

        neighbors=[]

        # Find the neighbors of each particle within the interaction radius R0
        for j in range(0,N):
            if (config[0][i] - config[0][j])**2+(config[1][i] - config[1][j])**2 <= R0**2:
                neighbors.append(j)

        # Calculate the mean orientation of the neighbor particles within R0
        mean_cos = np.mean(np.cos(config[2][neighbors]))
        mean_sin = np.mean(np.sin(config[2][neighbors]))
        mean_theta[i] = np.arctan2(mean_sin, mean_cos)

    return mean_theta

def ConfigurationUpdate(config,vel,R0,eta,N,L,dt):

    """

    This function updates the particles position and orienation.

    Parameters
        config: previous particles configuration
        vel: particles velocity
        R0: interaction radius
        eta: noise amplituse
        N: number of particles
        L: linear dimension of space
        dt: time step

    Returns:
        Updated configuration of the N particles.

    Raise:
        ValueError if the updated coordinates (x,y) of the N particles are out of the system space of linear dimension L.

    """

    # Update particles position
    config[0] = config[0] + vel[0]*dt
    config[1] = config[1] + vel[1]*dt

    # Impose periodic boundary conditions
    config[0] = config[0] % L
    config[1] = config[1] % L

    if not all(i < L and i >= 0 for i in config[0]):
        raise ValueError('The x coordinate of each particle must be between 0 and {} but at least one is out of range!'.format(L))

    if not all(i < L and i >= 0 for i in config[1]):
        raise ValueError('The y coordinate of each particle must be between 0 and {} but at least one is out of range!'.format(L))

    # Calculate the mean orientation of particles within R0
    mean_theta =  NeighborsMeanAngle(config,N,R0)

    # Update particles orientation
    config[2] = mean_theta + eta*(np.random.rand(N)-0.5)

    return config

def OrderParameter(theta,N):

    """

    This function calculates the order parameter.

    Parameters
        theta: particles orientation
        N: number of particles

    Returns:
        Order parameter phi.

    Raise:
        ValueError if the order parameter is less than 0 or greater than 1.

    """

    sx = np.sum(np.cos(theta))
    sy = np.sum(np.sin(theta))
    phi = ((sx)**2 + (sy)**2)**(0.5)/N

    if not phi >= 0 and phi <= 1:
        raise ValueError('The order parameter must be between 0 and 1 but is {}!'.format(phi))

    return phi
