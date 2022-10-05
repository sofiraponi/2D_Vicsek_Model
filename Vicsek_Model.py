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

def InitialPosition(N,L):

    """

    This function creates a random particles initial position configuration.

    Parameters
        N : number of particles
        L : linear dimension of space

    Returns:
        Position (x,y) of the N particles.

    """

    x = np.random.rand(N)*L
    y = np.random.rand(N)*L

    return x,y


def InitialVelocity(N,v0):

    """

    This function creates a random particles initial velocity configuration.

    Parameters
        N : number of particles
        v0 : velocity modulus

    Returns:
        Velocity (vx,vy) and orientation theta of the N particles.

    """

    theta = 2*np.pi*np.random.rand(N) # Random orientation per each particle
    vx = v0*np.cos(theta)
    vy = v0*np.sin(theta)

    return vx, vy, theta
