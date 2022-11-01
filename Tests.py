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
def test_InitialConfiguration_OutputLenght(num_part,space_dim):

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    assert len(config) == 3

    # Test if the lenght of x, y and theta is num_part
    assert len(config[0]) == num_part
    assert len(config[1]) == num_part
    assert len(config[2]) == num_part


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialPositionRange(num_part,space_dim):

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Test if all particles are inside the space of linear dimension space_dim
    assert all(i < space_dim and i >= 0 for i in config[0])
    assert all(i < space_dim and i >= 0 for i in config[1])


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialOrientationRange(num_part,space_dim):

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Test that theta is between -π and π
    assert all(i <= np.pi and i >= -np.pi for i in config[2])


@given(vel_mod=st.floats(0,10,exclude_min=True))
def test_VelocityCalculation_OutputLenght(vel_mod):

    # Vector of random orientations
    theta = np.array([-1.5,0.5,2.8,1.2,-3.0,1.7,0.3,1.1,-2.7,1.5])

    vel = Vicsek_Model.VelocityCalculation(vel_mod,theta)

    assert len(vel) == 2

    assert len(vel[0]) == len(theta)
    assert len(vel[1]) == len(theta)


@given(vel_mod=st.floats(0,10,exclude_min=True))
def test_VelocityCalculation_ConstantModulus(vel_mod):

    # Vector of random orientations
    theta = np.array([1.6,2.5,-0.8,0.2,3.0,-2.1,0.5,1.2,-1.7,2.9])

    vel = Vicsek_Model.VelocityCalculation(vel_mod,theta)

    # Test if the velocity of each particle has constant module
    mod_square = vel[0]**2+vel[1]**2
    assert all(np.isclose(i,vel_mod**2) for i in mod_square)


def test_FindNeighbors():

    space_dim=10
    int_radius=1.5

    # Set of 10 particles inside the system space
    positions=([[1,4],[1,7],[4,7],[7,5],[8,6],[7,8],[6,8],[6,4],[5,2],[1,8]])

    # Test the neighbors within a the interaction radius
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[0]],space_dim) == [0]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[1]],space_dim) == [1,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[2]],space_dim) == [2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[3]],space_dim) == [3,4,7]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[4]],space_dim) == [3,4]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[5]],space_dim) == [5,6]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[6]],space_dim) == [5,6]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[7]],space_dim) == [3,7]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[8]],space_dim) == [8]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[9]],space_dim) == [1,9]


def test_FindNeighbors_BoundaryConditions():

    space_dim=10
    int_radius=1

    # Set of 4 particles near the boders of the system space
    positions=np.array([[0.5,5],[5,9.5],[9.5,5],[5,0.5]])

    # Test the satisfaction of periodic boundary conditions
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[0]],space_dim) == [0,2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[1]],space_dim) == [1,3]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[2]],space_dim) == [0,2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[3]],space_dim) == [1,3]


def test_FindNeighbors_NullRadius():

    space_dim=10
    int_radius=0

    #Set of 10 particles inside the system space
    positions=([[7,5],[1,8],[7,8],[2,9],[7,7],[7,9],[8,4],[2,6],[4,3],[0,7]])

    # Test that each particles is the only neighbors of itself if the interaction radius is null
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[0]],space_dim) == [0]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[1]],space_dim) == [1]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[2]],space_dim) == [2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[3]],space_dim) == [3]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[4]],space_dim) == [4]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[5]],space_dim) == [5]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[6]],space_dim) == [6]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[7]],space_dim) == [7]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[8]],space_dim) == [8]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[9]],space_dim) == [9]


@given(int_radius=st.floats(0,10,exclude_min=True),num_part=st.integers(10,500), space_dim = st.floats(1,50))
@settings(max_examples = 10, deadline=1000)
def test_NeighborsMeanAngle(num_part,space_dim,int_radius):

    np.random.seed(3)

    # Generate a random particles configuration
    config=Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Calculate the mean neighbors direction for each particle with random interaction radius
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,int_radius,space_dim)

    # Test if the lenght of the output is equal to the number of particles
    assert len(mean_theta) == num_part

    # Test if all mean orientations are between -π and π
    mod_mean_theta = np.abs(mean_theta)
    assert all(i <= np.pi for i in mod_mean_theta)

    # Test that mean_theta is equal to the particle orientation when int_radius = 0
    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,0,space_dim)
    assert np.allclose(mean_theta,config[2])


@given(int_radius=st.floats(0,10,exclude_min=True),noise_ampl=st.floats(0,1), num_part=st.integers(10,500), space_dim = st.floats(1,50), time_step=st.floats(0,1,exclude_min=True), vel_mod=st.floats(0,10,exclude_min=True), num_steps=st.integers(50,1000))
@settings(max_examples = 1, deadline=1000)
def test_ConfigurationUpdate(num_part,space_dim,vel_mod,noise_ampl,time_step,num_steps,int_radius):

    np.random.seed(3)

    # Generate an initial random particles configuration
    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    # Calculate the particles velocity
    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    # Calculate the initial order parameter
    initphi = Vicsek_Model.OrderParameter(config[2])

    for i in range(num_steps):

        # Update the particles configuration with random interaction radius
        config = Vicsek_Model.ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step)

        # Test if all particles are still inside the space of linear dimension space_dim
        mod_x = np.abs(config[0])
        mod_y = np.abs(config[1])
        assert all(i <= space_dim for i in mod_x)
        assert all(i <= space_dim for i in mod_y)

        # Update the particles velocity
        vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    # Calculate the final order parameter
    finalphi = Vicsek_Model.OrderParameter(config[2])

    # Test the phase transition
    assert finalphi >= initphi


def test_OrderParameter_EqualOrientations():

    # All equal orientations
    theta=np.repeat(1.,100)

    # Calculate the order parameter
    phi = Vicsek_Model.OrderParameter(theta)

    # Test that the order parameter is 1 when all orientations are equal
    assert np.isclose(phi,1)


def test_OrderParameter_RandomOrientations():

    # Random orientations
    theta = np.array([-0.5,1.5,1.8,2.2,-1.,0.7,2.3,2.1,-0.7,2.5])

    # Calculate the order parameter
    phi = Vicsek_Model.OrderParameter(theta)

    # Test that the order parameter is a number between 0 and 1 when orientations are random
    assert np.isclose(phi,0.3673557583)


def test_OrderParameter_OppositeOrientations():

    # Opposite orientations
    theta = np.array([-0.5,np.pi-0.5,-1.8,np.pi-1.8,-3.,np.pi-3.,-2.3,np.pi-2.3,-0.7,np.pi-0.7])

    # Calculate the order parameter
    phi = Vicsek_Model.OrderParameter(theta)

    # Test that the order parameter is 0 when the orientations cancel out each other
    assert np.isclose(phi,0)


if __name__ == "main":
    pass
