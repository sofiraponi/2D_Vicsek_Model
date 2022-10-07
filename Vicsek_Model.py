#==============================================================
#Author: Sofia Raponi
#Date: 05 October, 2022
#
#  Vicsek_Model
#
#  Aim: To define the functions needed to simulate the Viscek Model for 2 dimensions.
#
#==============================================================

import numpy as np
import matplotlib.pyplot as plt
import math

def InitialConfiguration(N,L):

    """

    This function creates random particles initial position and orientation.

    Parameters
        N : number of particles
        L : linear dimension of space

    Returns:
        Initial configuration.

    """

    np.random.seed(10)

    x = np.random.rand(N)*L

    y = np.random.rand(N)*L

    theta = 2*np.pi*np.random.rand(N)

    initconfig=np.array([x,y,theta])

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

    vel=np.array([vx,vy])

    return vx, vy

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

    config[0] = config[0] + vel[0]*dt
    config[1] = config[1] + vel[1]*dt

    # Bundary conditions

    config[0] = config[0] % L
    config[1] = config[1] % L

    # Mean orientation of the neighbors within R0

    mean_theta=np.empty(N)

    for i in range(0,N):

        neighbors=[]

        for j in range(0,N):

            if (config[0][i] - config[0][j])**2 + (config[1][i] - config[1][j])**2 <= R0**2:
                neighbors.append(j)

        mean_cos = np.mean(np.cos(config[2][neighbors]))
        mean_sin = np.mean(np.sin(config[2][neighbors]))
        mean_theta[i] = np.arctan2(mean_sin, mean_cos)

    # Orientation update

    config[2] = mean_theta + eta*(np.random.rand(N)-0.5)

    return config


def OrderParameter(theta,N):

    """

    This function calculates the order parameter.

    Parameters
        theta: particle orientation
        N: number of particles

        Returns:
        Order parameter phi.

    """

    sx = np.sum(np.cos(theta))
    sy = np.sum(np.sin(theta))
    phi = ((sx)**2 + (sy)**2)**(0.5)/N

    return phi
