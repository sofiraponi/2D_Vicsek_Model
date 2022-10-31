#==============================================================
#Author: Sofia Raponi
#Date: 05 October, 2022
#
#  Tests
#
#  Aim: To test funcions in Viscek_Model.py.
#
#==============================================================

import Vicsek_Model
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialConfiguration(num_part,space_dim):

    np.random.seed(3)

    x, y, theta = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Test if the lenght of x, y and theta is num_part
    assert len(x) == len(y) == len(theta) == num_part

    # Test if all particles are inside the space of linear dimension space_dim
    mod_x = np.abs(x)
    mod_y = np.abs(y)
    assert all(i <= space_dim for i in mod_x)
    assert all(i <= space_dim for i in mod_y)


@given(vel_mod=st.floats(0,10,exclude_min=True), theta=st.floats(-np.pi,np.pi))
def test_VelocityCalculation(vel_mod,theta):

    vel = Vicsek_Model.VelocityCalculation(vel_mod,theta)

    # Test that the output lenght is 2
    assert len(vel) == 2

    # Test if the velocity has constant module v0
    mod_square = vel[0]**2+vel[1]**2
    assert np.isclose(mod_square,vel_mod**2)


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
@settings(max_examples = 10, deadline=1000)
def test_NeighborsMeanAngle(num_part,space_dim):

    np.random.seed(3)

    # Generate a random particles configuration
    config=Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Calculate the mean neighbors direction for each particle with random interaction radius in [0,space_dim]
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,num_part,space_dim*np.random.rand())

    # Test if the lenght of the output is equal to the number of particles
    assert len(mean_theta) == num_part

    # Test if all mean orientations are between -π and π
    mod_mean_theta = np.abs(mean_theta)
    assert all(i <= np.pi for i in mod_mean_theta)

    # Test that mean_theta is equal to the particle orientation when R0 = 0
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,num_part,0)
    assert np.allclose(mean_theta,config[2])


@given(noise_ampl=st.floats(0,1), num_part=st.integers(10,500), space_dim = st.floats(1,50), time_step=st.floats(0,1,exclude_min=True), vel_mod=st.floats(0,10,exclude_min=True), num_steps=st.integers(50,1000))
@settings(max_examples = 1)
def test_ConfigurationUpdate(num_part,space_dim,vel_mod,noise_ampl,time_step,num_steps):

    np.random.seed(3)

    # Generate an initial random particles configuration
    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Calculate the particles velocity
    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    # Calculate the initial order parameter
    initphi = Vicsek_Model.OrderParameter(config[2],num_part)

    for i in range(num_steps):

        # Update the particles configuration with random interaction radius in [0,space_dim]
        config = Vicsek_Model.ConfigurationUpdate(config,vel,space_dim*np.random.rand(),noise_ampl,num_part,space_dim,time_step)

        # Test if all particles are still inside the space of linear dimension L
        mod_x = np.abs(config[0])
        mod_y = np.abs(config[1])
        assert all(i <= space_dim for i in mod_x)
        assert all(i <= space_dim for i in mod_y)

        # Update the particles velocity
        vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    # Calculate the final order parameter
    finalphi = Vicsek_Model.OrderParameter(config[2],num_part)

    # Test the phase transition
    assert finalphi > initphi


@given(num_part=st.integers(10,500))
def test_OrderParameter(num_part):

    np.random.seed(3)

    # Generate all equal orientations for the N particles
    theta_equal=np.repeat(np.pi*(2*np.random.rand()-1),num_part)

    # Calculate the order parameter
    phi_equal = Vicsek_Model.OrderParameter(theta_equal,num_part)

    # Test that the order parameter is 1 when all orientations are equal
    assert np.isclose(phi_equal,1)

    # Generate random orientations for the N particles
    theta = np.pi*(2*np.random.rand(num_part)-1)

    # Calculate the order parameter
    phi = Vicsek_Model.OrderParameter(theta,num_part)

    # Test that the order parameter is between 0 and 1 when orientations are random
    mod_phi = np.abs(phi)
    assert mod_phi <= 1


if __name__ == "main":
    pass
