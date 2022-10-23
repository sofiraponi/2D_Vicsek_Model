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

    # Test that all particles are inside the system space

    assert all(i < L and i >= 0 for i in x)
    assert all(i < L and i >= 0 for i in y)


@given(v0=st.floats(0.,10.,exclude_min=True), theta=st.floats(0.,2*np.pi))
def test_VelocityUpdate(v0,theta):

    vel = Vicsek_Model.VelocityUpdate(v0,theta)

    # Test if the velocity has constant module v0

    mod_square = vel[0]**2+vel[1]**2

    assert np.isclose(mod_square,v0**2)


@given(N=st.integers(10,500), L = st.floats(1,50))
@settings(max_examples = 10, deadline=1000)
def test_NeighborsMeanAngle(N,L):

    config=Vicsek_Model.InitialConfiguration(N,L)

    np.random.seed(3)

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,N,L*np.random.rand())

    # Test that the mean angle is between -π and π

    assert all(i >= -np.pi and i <= np.pi for i in mean_theta)

    # Test that mean_theta is equal to the particle orientation when R0 is 0

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,N,0.)

    assert np.allclose(mean_theta,config[2])


@given(eta=st.floats(0.,1.), N=st.integers(10,500), L = st.floats(1,50), dt=st.floats(0.,1.,exclude_min=True), v0=st.floats(0.,10.,exclude_min=True), T=st.integers(50,1000),R0=st.floats(0.,L))
@settings(max_examples = 1)
def test_ConfigurationUpdate(N,L,v0,eta,dt,T,R0):

    config = Vicsek_Model.InitialConfiguration(N,L)

    np.random.seed(3)

    vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    initphi = Vicsek_Model.OrderParameter(config[2],N)

    for i in range(T):

        config = Vicsek_Model.ConfigurationUpdate(config,vel,L*np.random.rand(),eta,N,L,dt)

        # Test the periodic bundary conditions

        assert all(i < L and i>=0 for i in config[0])
        assert all(i < L and i>=0 for i in config[0])

        vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    finalphi = Vicsek_Model.OrderParameter(config[2],N)

    # Test the phase transition

    assert finalphi > initphi


@given(N=st.integers(10,500))
def test_OrderParameter(N):

    np.random.seed(3)

    theta_equal=np.repeat(np.pi*(2*np.random.rand()-1),N)

    phi_equal = Vicsek_Model.OrderParameter(theta_equal,N)

    # Test that the order parameter is 1 when all orientations are equal

    assert np.isclose(phi_equal,1.0)

    theta_random= np.pi*(2*np.random.rand(N)-1)

    phi_random = Vicsek_Model.OrderParameter(theta_random,N)

    # Test that the order parameter is between 0 and 1 when orientations are random

    assert phi_random >= 0
    assert phi_random <= 1
