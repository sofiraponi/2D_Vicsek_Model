#==============================================================
#Author: Sofia Raponi
#Date: 05 October, 2022
#
#  tests
#
#  Aim: To test funcions in Viscek_Model.py.
#
#==============================================================

import Vicsek_Model
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings


@given(N=st.integers(10,500), L = st.floats(1,50))
def test_InitialConfiguration(N,L):

    x, y, theta = Vicsek_Model.InitialConfiguration(N,L)

    # Test if the lenght of x, y and theta is N
    assert len(x) == len(y) == len(theta) == N

    # Test if all particles are inside the space of linear dimension L
    mod_x = np.abs(x)
    mod_y = np.abs(y)
    assert all(i <= L for i in mod_x)
    assert all(i <= L for i in mod_y)


@given(v0=st.floats(0.,10.,exclude_min=True), theta=st.floats(-np.pi,np.pi))
def test_VelocityUpdate(v0,theta):

    vel = Vicsek_Model.VelocityUpdate(v0,theta)

    # Test that the output has lenght 2
    assert len(vel) == 2

    # Test if the velocity has constant module v0
    mod_square = vel[0]**2+vel[1]**2
    assert np.isclose(mod_square,v0**2)


@given(N=st.integers(10,500), L = st.floats(1,50))
@settings(max_examples = 10, deadline=1000)
def test_NeighborsMeanAngle(N,L):

    # Generate a random particles configuration
    config=Vicsek_Model.InitialConfiguration(N,L)

    np.random.seed(3)

    # Calculate the mean neighbors direction for each particle
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,N,L*np.random.rand())

    # Test if all mean orientations are not out of range
    mod_mean_theta = np.abs(mean_theta)
    assert all(i <= np.pi for i in mod_mean_theta)

    # Test if the lenght of the output is equal to the number of particles
    assert len(mean_theta) == N

    # Test that mean_theta is equal to the particle orientation when R0 is 0
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,N,0.)
    assert np.allclose(mean_theta,config[2])


@given(eta=st.floats(0.,1.), N=st.integers(10,500), L = st.floats(1,50), dt=st.floats(0.,1.,exclude_min=True), v0=st.floats(0.,10.,exclude_min=True), T=st.integers(50,1000))
@settings(max_examples = 1)
def test_ConfigurationUpdate(N,L,v0,eta,dt,T):

    # Generate an initial random particles confoguration
    config = Vicsek_Model.InitialConfiguration(N,L)

    np.random.seed(3)

    # Calculate the particles velocity
    vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    # Calculate the initial order parameter
    initphi = Vicsek_Model.OrderParameter(config[2],N)

    for i in range(T):

        # Update the particles confoguration
        config = Vicsek_Model.ConfigurationUpdate(config,vel,L*np.random.rand(),eta,N,L,dt)

        # Test if all particles are still inside the space of linear dimension L
        mod_x = np.abs(config[0])
        mod_y = np.abs(config[1])
        assert all(i <= L for i in mod_x)
        assert all(i <= L for i in mod_y)

        # Update the particles velocity
        vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    # Calculate the final order parameter
    finalphi = Vicsek_Model.OrderParameter(config[2],N)

    # Test the phase transition
    assert finalphi > initphi


@given(N=st.integers(10,500))
def test_OrderParameter(N):

    np.random.seed(3)

    # Generate all equal orientations for the N particles
    theta_equal=np.repeat(np.pi*(2*np.random.rand()-1),N)

    # Calculate the order parameter
    phi_equal = Vicsek_Model.OrderParameter(theta_equal,N)

    # Test that the order parameter is 1 when all orientations are equal
    assert np.isclose(phi_equal,1.0)

    # Generate random orientations for the N particles
    theta = np.pi*(2*np.random.rand(N)-1)

    # Calculate the order parameter
    phi = Vicsek_Model.OrderParameter(theta,N)

    # Test that the order parameter is between 0 and 1 when orientations are random
    mod_phi = np.abs(phi)
    assert mod_phi <= 1


if __name__ == "main":
    pass
