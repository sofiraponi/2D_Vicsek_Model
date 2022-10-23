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

    This function creates random initial position and orientation of particles.

    Parameters
        N : number of particles
        L : linear dimension of space

    Returns:
        Initial configuration of the particles.

    """
    # Initialization
    np.random.seed(3)

    # Generate random position of particles between 0 and L
    x = np.random.rand(N)*L
    y = np.random.rand(N)*L

    # Generate random orientation of particles between -π and π
    theta = np.pi*(2*np.random.rand(N)-1)

    initconfig = np.array([x,y,theta])

    return initconfig


def VelocityUpdate(v0,theta):

    """

    This funtion updates the particles velocity.

    Parameters
        v0 : velocity modulus
        theta: particles orientation

    Returns:
        Velocity (vx,vy) of the N particles.

    """

    vx = v0*np.cos(theta)
    vy = v0*np.sin(theta)

    vel = np.array([vx,vy])

    return vel

def NeighborsMeanAngle(config,N,R0):

    """

    This function calculates the mean orientation of the particles within the intarction radius R0

    Parameters
        config: previous particles configuration
        vel: particles velocity
        N: number of particles
        R0: interaction radius

    Returns:
        Updated configuration.

    """

    mean_theta=config[2]

    for i in range(0,N):

        neighbors=[]

        for j in range(0,N):

            if (config[0][i] - config[0][j])**2 + (config[1][i] - config[1][j])**2 <= R0**2:

                neighbors.append(j)

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
        Updated configuration.

    """

    # Update particles position
    config[0] = config[0] + vel[0]*dt
    config[1] = config[1] + vel[1]*dt

    # Impose periodic boundary conditions
    config[0] = config[0] % L
    config[1] = config[1] % L

    # Calculate the mean orientation of particles within R0

    mean_theta =  NeighborsMeanAngle(config,N,R0)

    # Update particles orientation
    config[2] = mean_theta + eta*(np.random.rand(N)-0.5)

    return config


def OrderParameter(theta,N):

    """

    This function calculates the order parameter.

    Parameters
        theta: particle orientation
        N: number of particles

        Returns:
        Order parameter.

    """

    sx = np.sum(np.cos(theta))
    sy = np.sum(np.sin(theta))
    phi = ((sx)**2 + (sy)**2)**(0.5)/N

    return phi
