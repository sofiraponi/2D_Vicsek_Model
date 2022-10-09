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
import configparser

config=configparser.ConfigParser()
config.read('settings.ini')


@given(N=st.integers(1,int(config['parameters']['N'])), L = st.integers(1,int(config['parameters']['L'])))

def test_InitialConfiguration(N,L):

    x, y, theta = Vicsek_Model.InitialConfiguration(N,L)

    # Test if lenght of x, y and theta is N.

    assert len(x) == len(y) == len(theta) == N

    # Test that all particles are inside the system space

    assert all(i < L and i>=0 for i in x)
    assert all(i < L and i>=0 for i in y)

@given(v0=st.floats(0.,float(config['parameters']['v0'])), theta=st.floats(0.,2*np.pi))

def test_VelocityUpdate(v0,theta):

    vx, vy = Vicsek_Model.VelocityUpdate(v0,theta)

    # Test if the velocity has constant module v0

    mod_square = vx**2+vy**2

    assert np.isclose(mod_square,v0**2)


@given(R0=st.floats(0.5,float(config['parameters']['R0'])),eta=st.floats(0.,1.),N=st.integers(10,int(config['parameters']['N'])), L=st.integers(1,int(config['parameters']['L'])),dt=st.floats(float(config['parameters']['dt']),1.),v0=st.floats(float(config['parameters']['v0']),2.),T=st.integers(100,int(config['parameters']['T'])))
@settings(max_examples = 1)

def test_ConfigurationUpdate(N,L,v0,R0,eta,dt,T):

    config = Vicsek_Model.InitialConfiguration(N,L)

    vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    initphi = Vicsek_Model.OrderParameter(config[2],N)

    for i in range(T):

        config = Vicsek_Model.ConfigurationUpdate(config,vel,R0,eta,N,L,dt)

        # Test the bundary conditions

        assert all(i < L and i>=0 for i in config[0])
        assert all(i < L and i>=0 for i in config[0])

        vel = Vicsek_Model.VelocityUpdate(v0,config[2])

    finalphi = Vicsek_Model.OrderParameter(config[2],N)

    # Test the phase transition to collective order

    assert finalphi > initphi


@given(N=st.integers(1,int(config['parameters']['N'])))

def test_OrderParameter(N):

    theta_equal=np.repeat(2*np.pi*np.random.rand(),N)

    phi_equal = Vicsek_Model.OrderParameter(theta_equal,N)

    # Test if the order parameter is 1 when all orientations are equal

    assert np.isclose(phi_equal,1.0)

    theta_random=2*np.pi*np.random.rand(N)

    phi_random = Vicsek_Model.OrderParameter(theta_random,N)

    # Test if the order parameter is between 0 and 1 when orientations are random

    assert phi_random >= 0
    assert phi_random <= 1
