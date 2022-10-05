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
from hypothesis import given


@given(N=st.integers(1,1000), L = st.integers(1,10))

def test_InitialPosition(N,L):

    x0,y0=Vicsek_Model.InitialPosition(N,L)

    # test if lenght of x and y is N and system space dimension is 2.

    assert len(x0) == len(y0) == N

    # test that all particles are inside the system space

    assert all(i < L and i>=0 for i in x0)
    assert all(i < L and i>=0 for i in y0)


@given(v0=st.floats(0.,10.), N=st.integers(1,1000))

def test_InitialVelocity(N,v0):

    vx0, vy0, theta0 =Vicsek_Model.InitialVelocity(N,v0)

    # test if lenght of vx, vy and theta is N.

    assert len(vx0) == len(vy0) == len(theta0) == N

    # test if all velocities have constant module v0

    mod_square = vx0**2+vy0**2

    assert all(np.isclose(i,v0**2) for i in mod_square)
