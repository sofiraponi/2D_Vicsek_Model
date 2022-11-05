#==============================================================
#Author: Sofia Raponi
#Date: 05 October, 2022
#
#  Tests
#
#  Aim: To test funcions in Viscek_Model.py.
#==============================================================

import Vicsek_Model
import numpy as np
import hypothesis
from hypothesis import strategies as st
from hypothesis import given, settings


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialConfiguration_OutputLenght(num_part,space_dim):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. The lenght of the output is 3
    4. The lenght of the output components (coordinates x, y and orietations of the particles) is num_part
    """

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    assert len(config) == 3

    assert len(config[0]) == num_part
    assert len(config[1]) == num_part
    assert len(config[2]) == num_part


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialPositionRange(num_part,space_dim):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. All the particles coordinates (x, y) are in [0, space_dim)
    """

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    assert all(i < space_dim and i >= 0 for i in config[0])
    assert all(i < space_dim and i >= 0 for i in config[1])


@given(num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_InitialOrientationRange(num_part,space_dim):

    """
    Procedure:
    1. Initialization random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    ---------
    Verification:
    3. All the particles orientations are in [-π, π]
    """

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    assert all(i <= np.pi and i >= -np.pi for i in config[2])


@given(vel_mod=st.floats(0,10,exclude_min=True),num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_VelocityCalculation_OutputLenght(vel_mod):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    3. Calculate the velocity of the particles given a certain velocity modulus (vel_mod)
    ---------
    Verification:
    4. The lenght of the output is 2
    5. The lenght of the output components (vx, vy) is num_part
    """

    np.random.seed(3)

    config = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    assert len(vel) == 2

    assert len(vel[0]) == num_part
    assert len(vel[1]) == num_part


@given(vel_mod=st.floats(0,10,exclude_min=True))
def test_VelocityCalculation_ConstantModulus(vel_mod):

    """
    Procedure:
    1. Create a vector of different orientations of 10 particles in [-π, π]
    2. Calculate the velocity of the particles given a certain velocity modulus (vel_mod)
    3. Calculate the modulus of the velocity of the particles
    ---------
    Verification:
    4. The calculated modulus of the velocity of each particle is equal to the square of vel_mod
    """

    theta = np.array([1.6,2.5,-0.8,0.2,3.0,-2.1,0.5,1.2,-1.7,2.9])

    vel = Vicsek_Model.VelocityCalculation(vel_mod,theta)

    mod_square = vel[0]**2+vel[1]**2

    assert all(np.isclose(i,vel_mod**2) for i in mod_square)


def test_FindNeighbors():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the interaction radius in (0, √2*space_dim)
    3. Create a vector of positions of 10 particles inside the system space
    ---------
    Verification:
    4. The neighbors of each particle within the interaction radius are identified correctly
    """

    space_dim=10

    int_radius=1.5

    positions=np.array([[1,4],[1,7],[4,7],[7,5],[8,6],[7,8],[6,8],[6,4],[5,2],[1,8]])

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

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the interaction radius in (0, √2*space_dim)
    3. Create a vector of the positions of 4 particles inside the system space and close to the borders
    ---------
    Verification:
    4. The neighbors of each particle within the interaction radius are identified by satisfying the periodic boundary conditions
    """

    space_dim=10

    int_radius=2

    positions=np.array([[1,5],[5,9],[9,5],[5,1]])

    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[0]],space_dim) == [0,2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[1]],space_dim) == [1,3]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[2]],space_dim) == [0,2]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[3]],space_dim) == [1,3]


def test_FindNeighbors_NullRadius():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the interaction radius equal to 0
    3. Create a vector of positions of 10 particles inside the system space
    ---------
    Verification:
    4. Each particles is the only neighbor of itself
    """

    space_dim=10

    int_radius=0

    positions=np.array([[7,5],[1,8],[7,8],[2,9],[7,7],[7,9],[8,4],[2,6],[4,3],[0,7]])

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


def test_FindNeighbors_AllNeighbors():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the interaction radius equal to √2*space_dim
    3. Create a vector of random positions of 10 particles inside the system space
    ---------
    Verification:
    4. All particles are neighbors of each other
    """

    space_dim=10

    int_radius=10*np.sqrt(2)

    positions=np.array([[4,2],[3,5],[2,8],[1,9],[0,3],[2,0],[7,1],[9,2],[8,4],[6,7]])

    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[0]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[1]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[2]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[3]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[4]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[5]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[6]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[7]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[8]],space_dim) == [0,1,2,3,4,5,6,7,8,9]
    assert Vicsek_Model.FindNeighbors(positions,int_radius,[positions[9]],space_dim) == [0,1,2,3,4,5,6,7,8,9]


@given(int_radius=st.floats(0,1,exclude_min=True),num_part=st.integers(10,500), space_dim = st.floats(1,50))
def test_NeighborsMeanAngle_OutputLenghtandRange(num_part,space_dim,int_radius):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    3. Set that the interaction radius is a given float in [0, √2*space_dim]
    4. Calculate the mean angle of neighbors of each particle
    ---------
    Verification:
    5. The lenght of the output is num_part
    6. The mean angle of neighbors of each particle is in [-π, π]
    """

    np.random.seed(3)

    config=Vicsek_Model.InitialConfiguration(num_part,space_dim)

    int_radius = int_radius*space_dim*np.sqrt(2)

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,int_radius,space_dim)

    assert len(mean_theta) == num_part

    assert all(i <= np.pi and i>=-np.pi for i in mean_theta)


@given(int_radius=st.floats(0,1))
def test_NeighborsMeanAngle_EqualOrientations(int_radius):

    """
    Procedure:
    1. Set the space linear dimension
    2. Set that the interaction radius is a given float in [0, √2*space_dim]
    3. Create a configration of 10 particles all with equal orientation
    4. Calculate the mean angle of neighbors of each particle
    ---------
    Verification:
    5. The mean angle of neighbors is for each particle equal to the orientation of the particles
    """

    space_dim=10

    int_radius=int_radius*10*np.sqrt(2)

    config = np.array([[1, 4, 5, 1, 6, 6, 1, 6, 5, 3], [2, 3, 4, 8, 4, 2, 6, 0, 2, 9], [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]])

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,int_radius,space_dim)

    assert np.allclose(mean_theta,1.)


def test_NeighborsMeanAngle_NullRadius():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set that the interaction radius is 0
    3. Create a configration of 10 particles all with different orientations
    4. Calculate the mean angle of neighbors of each particle
    ---------
    Verification:
    5. The mean angle of neighbors is for each particle equal to its orientation (vector of neighbors mean angles equal to vector of orientations)
    """

    space_dim=10

    int_radius=0

    config = np.array([[5, 5, 9, 6, 6, 8, 2, 5, 8, 1], [2, 7, 0, 8, 3, 1, 0, 3, 2, 3], [0.5,-1.0,2.2,1.8,-0.3,1.4,2.7,-3.1,1.2,0.6]])

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,int_radius,space_dim)

    assert np.allclose(mean_theta,config[2])


def test_NeighborsMeanAngle_AllNeighbors():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the interaction radius equal to √2*space_dim
    3. Create a configration of 10 particles with different orientations
    4. Calculate the mean angle of neighbors of each particle
    ---------
    Verification:
    5. The mean angle of neighbors is equal for each particle
    """

    space_dim=10

    int_radius=10*np.sqrt(2)

    config = np.array([[4, 6, 8, 4, 8, 1, 9, 5, 4, 2], [3, 4, 7, 6, 6, 8, 0, 3, 5, 6], [-0.7,2.0,0.3,-1.5,0.9,2.0,-3.0,-1.9,2.8,-0.3]])

    mean_theta = Vicsek_Model.NeighborsMeanAngle(config,int_radius,space_dim)

    assert np.allclose(mean_theta,mean_theta[0])


@given(int_radius=st.floats(0,10,exclude_min=True),num_part=st.integers(10,500), space_dim=st.floats(1,50),vel_mod=st.floats(0,10,exclude_min=True),noise_ampl=st.floats(0,1),time_step=st.floats(0,1,exclude_min=True))
def test_ConfigurationUpdate_OutputLenght(num_part,int_radius,noise_ampl,space_dim,time_step,vel_mod):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    3. Set that the interaction radius is a given float in [0, √2*space_dim]
    4. Calculate the velocity of the particles given a certain velocity modulus (vel_mod)
    5. Update the particles configuration given a certain noise amplitude (noise_ampl) and time step (time_step)
    ---------
    Verification:
    6. The lenght of the output is 3
    7. The lenght of the output components (coordinates x, y and orietations of the particles) is num_part
    """

    np.random.seed(3)

    config=Vicsek_Model.InitialConfiguration(num_part,space_dim)

    int_radius = int_radius*space_dim*np.sqrt(2)

    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    config = Vicsek_Model.ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step)

    assert len(config) == 3

    assert len(config[0]) == num_part
    assert len(config[1]) == num_part
    assert len(config[2]) == num_part


@given(int_radius=st.floats(0,1,exclude_min=True),num_part=st.integers(10,500), space_dim=st.floats(1,50),vel_mod=st.floats(0,10,exclude_min=True),noise_ampl=st.floats(0,1),time_step=st.floats(0,1,exclude_min=True))
def test_ConfigurationUpdate_OutputRange(num_part,int_radius,noise_ampl,space_dim,time_step,vel_mod):

    """
    Procedure:
    1. Initialize random seed
    2. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    3. Set that the interaction radius is a given float in [0, √2*space_dim]
    4. Calculate the velocity of the particles given a certain velocity modulus (vel_mod)
    5. Update the particles configuration given a certain noise amplitude (noise_ampl) and time step (time_step)
    ---------
    Verification:
    6. All the updated particles coordinates (x, y) are in [0, space_dim)
    7. All the updated particles orientations are in [-π-0.5, π+0-5]
    """

    np.random.seed(3)

    config=Vicsek_Model.InitialConfiguration(num_part,space_dim)

    int_radius = int_radius*space_dim*np.sqrt(2)

    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    config = Vicsek_Model.ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step)

    assert all(i < space_dim and i >= 0 for i in config[0])
    assert all(i < space_dim and i >= 0 for i in config[1])

    assert all(i <= np.pi+0.5 and i >= -np.pi-0.5 for i in config[2])


def test_ConfigurationUpdate_BoundaryConditions():

    """
    Procedure:
    1. Set the space linear dimension
    2. Set the velocity modulus
    3. Set the interaction radius equal to 0
    4. Set the noise amplitude equal to 0
    5. Set the time step
    6. Create the configuration of 4 particles near the space borders that move in the direction out of the system
    7. Calculate the velocity of the particles
    8. Update the particles configuration
    ---------
    Verification:
    9. The updated configuration satisfies the periodic boundary conditions
    """

    space_dim=10

    vel_mod=2.

    int_radius=0.

    noise_ampl=0.

    time_step=1.

    config = np.array([[1, 5, 9, 5],[5, 9, 5, 1],[np.pi, np.pi/2, 0, -np.pi/2]])

    vel = Vicsek_Model.VelocityCalculation(vel_mod,config[2])

    config = Vicsek_Model.ConfigurationUpdate(config,vel,int_radius,noise_ampl,space_dim,time_step)

    assert np.allclose(config[0],[[9, 5, 1, 5]])
    assert np.allclose(config[1],[[5, 1, 5, 9]])


@given(int_radius=st.floats(0,10,exclude_min=True),num_part=st.integers(10,500),space_dim=st.floats(1,50),vel_mod=st.floats(0,10,exclude_min=True),noise_ampl=st.floats(0,1),time_step=st.floats(0,1,exclude_min=True),num_steps=st.integers(100,500))
@settings(max_examples=1)
def test_PhaseTransition(int_radius,noise_ampl,space_dim,time_step,num_steps,vel_mod,num_part):

    """
    Procedure:
    1. Initialize random seed
    2. Set that the interaction radius is a given float in [0, √2*space_dim]
    3. Generate initial configuration given a certain number of particles (num_part) and linear dimension of space (space_dim)
    4. Calculate the velocity of the particles given a certain velocity modulus (vel_mod)
    5. Update a certain number of steps (num_steps) the particles configuration given a certain noise amplitude (noise_ampl) and time step (time_step)
    ---------
    Verification:
    6. The final order parameter is greater or equal than the initial one
    """

    np.random.seed(3)

    int_radius = int_radius*space_dim*np.sqrt(2)

    initconfig = Vicsek_Model.InitialConfiguration(num_part,space_dim)

    initvel = Vicsek_Model.VelocityCalculation(vel_mod,initconfig[2])

    position, theta = Vicsek_Model.Simulate(initconfig,initvel,int_radius,noise_ampl,space_dim,time_step,num_steps,vel_mod)

    assert Vicsek_Model.OrderParameter(theta[num_steps]) >= Vicsek_Model.OrderParameter(theta[0])


def test_OrderParameter_EqualOrientations():

    """
    Procedure:
    1. Create vector of 100 equal orientations
    2. Calculate the order parameter
    ---------
    Verification:
    3. The order parameter is close to 1
    """

    theta=np.repeat(1.,100)

    phi = Vicsek_Model.OrderParameter(theta)

    assert np.isclose(phi,1)


def test_OrderParameter_RandomOrientations():

    """
    Procedure:
    1. Create vector of 10 different orientations
    2. Calculate the order parameter
    ---------
    Verification:
    3. The order parameter is close a certain number between in [0,1]
    """

    theta = np.array([-0.5,1.5,1.8,2.2,-1.,0.7,2.3,2.1,-0.7,2.5])

    phi = Vicsek_Model.OrderParameter(theta)

    assert np.isclose(phi,0.3673557583)


def test_OrderParameter_OppositeOrientations():

    """
    Procedure:
    1. Create vector of 10 orientations that cancel out each other
    2. Calculate the order parameter
    ---------
    Verification:
    3. The order parameter is close to 0
    """

    theta = np.array([-0.5,np.pi-0.5,-1.8,np.pi-1.8,-3.,np.pi-3.,-2.3,np.pi-2.3,-0.7,np.pi-0.7])

    phi = Vicsek_Model.OrderParameter(theta)

    assert np.isclose(phi,0)


if __name__ == "main":
    pass
