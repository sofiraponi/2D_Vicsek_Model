# 2D Vicsek Model simulation

The Vicsek model is a self-organized motion model that plays a key role in the study of active matter. This model shows a transition from the disordered movement of individuals within the group to collective behavior, caused only by interindividual forces of alignment, without attraction and repulsion. Its simple dynamic rule has been adopted as a starting point for many generalizations and variations that have been applied to a wide range of different problems, such as the collective behavior of large groups of animals. The goal of this project is to simulate the two-dimensional Vicsek model.

# Model definition
The model describes the synchronous motion of a set of ![equation](https://latex.codecogs.com/svg.image?N) self-propelled Particles, i.e. provided with autonomous movement possibilities. These particles are represented by points in continuous motion on the plane, characterized by the position ![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t)) and the velocity ![equation](https://latex.codecogs.com/svg.image?\textbf{v}_i(t)), with constant modulus ![equation](https://latex.codecogs.com/svg.image?v_0) and direction ![equation](https://latex.codecogs.com/svg.image?\textbf{s}_i(t)=(\cos(\theta_i(t)),\sin(\theta_i(t)))). The position of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle is updated at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t) according to the following dynamic evolution equation: 

![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t+\Delta&space;t)=\textbf{r}_i(t)&plus;\textbf{v}_i(t)\Delta&space;t=\textbf{r}_i(t)&plus;v_0\begin{pmatrix}\cos(\theta_i(t))&space;\\\sin(\theta_i(t))\end{pmatrix}\Delta&space;t)

According to the basic idea of the model, particles tend to move in the same direction as their neighbors, therefore the angle that defines the direction of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle ![equation](https://latex.codecogs.com/svg.image?\theta_i(t)) motion is determined, at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t), by the following update equation:

![equation](https://latex.codecogs.com/svg.image?\theta_i(t+\Delta&space;t)=Arg\left&space;[&space;\sum_{j=1}^{N}&space;n_{ij}(t)\textbf{s}_j(t)\right&space;]&plus;\eta_i(t))

Where the ![equation](https://latex.codecogs.com/svg.image?Arg) function returns the angle that defines the average direction of the velocity of the particles (including the ![equation](https://latex.codecogs.com/svg.image?i)-th) that are within a circle of radius ![equation](https://latex.codecogs.com/svg.image?R_0) centered in the reference particle. The connectivity matrix ![equation](https://latex.codecogs.com/svg.image?n_{ij}(t)) is in fact defined as:

![equation](https://latex.codecogs.com/svg.image?n_{ij}(t)=\begin{cases}&&space;1&space;\text{&space;if&space;}|\textbf{r}_i(t)-\textbf{r}_j(t)|<R_0\\\\&&space;0&space;\text{&space;if&space;}|\textbf{r}_i(t)-\textbf{r}_j(t)|>R_0\end{cases}&space;)

The alignment is hindered by a noise term ![equation](https://latex.codecogs.com/svg.image?\eta_{i}(t)) uniformly distributed in the interval ![equation](https://latex.codecogs.com/svg.image?[-\eta/2,\eta/2]), with amplitude ![equation](https://latex.codecogs.com/svg.image?\eta\in[0,1]).

If the polar alignment term is strong enough to overcome the noise effect, the system develops a global orientation order and therefore a collective movement. This process can be studied by monitoring the polar order parameter ![equation](https://latex.codecogs.com/svg.image?\varphi(t)), defined as the modulus of the mean direction of motion of the entire system of particles:

![equation](https://latex.codecogs.com/svg.image?\varphi(t)=\frac{1}{N}\left|\sum_{i=1}^{N}&space;\textbf{s}_i(t)\right|)

The order parameter is approximately null if the directions of motion of the individual particles are distributed randomly, as the latter tend to cancel each other out in the sum; while for the phase of coherent motion, with an ordered direction of the velocities, it assumes a finite and approximately unitary value.

# Model simulation
The aim of this project is to simulate the 2D Vicsek model in order to visualize the phase transition from random to ordered motion of particles. To do this, once the parameters of the model have been set, the initial coordinates and orientation of each particle are randomly generated respecting the periodic boundary conditions. Subsequently, at each time step, the position and direction of the particles is updated according to the model equations and the order parameter is calculated.

The steps that the user must follow to perform the simulation and obtain a visualization of both the particles motion and the evolution over time of the order parameter are listed below:

1. The user has to set the model parameters in the file [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini). In particular, the user has to choose: the particle velocity module ![equation](https://latex.codecogs.com/svg.image?v_0), the noise amplitude ![equation](https://latex.codecogs.com/svg.image?\eta), the interaction radius ![equation](https://latex.codecogs.com/svg.image?R_0), the time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t), the number of particles ![equation](https://latex.codecogs.com/svg.image?N), the linear dimension of the system ![equation](https://latex.codecogs.com/svg.image?L) and the total time ![equation](https://latex.codecogs.com/svg.image?T). There are some constraints that the user must follow in setting these parameters in order to observe the transition to collective motion, namely: ![equation](https://latex.codecogs.com/svg.image?v_0) must be greater than ![equation](https://latex.codecogs.com/svg.image?0) since the model concerns self-propelled particles in motion, ![equation](https://latex.codecogs.com/svg.image?\eta) must be between ![equation](https://latex.codecogs.com/svg.image?0) and ![equation](https://latex.codecogs.com/svg.image?1) by definition, ![equation](https://latex.codecogs.com/svg.image?R_0) must be greater than ![equation](https://latex.codecogs.com/svg.image?0) otherwise we would have a set of independent random walkers (usually ![equation](https://latex.codecogs.com/svg.image?R_0&space;=&space;1.0)) and ![equation](https://latex.codecogs.com/svg.image?N) must be high enough since we want to study a collective behavior (usually ![equation](https://latex.codecogs.com/svg.image?N&space;>&space;10&space;)).

2. The user has to launch the [Simulation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Simulation.py) file which imports the model parameters from the [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) file through the ConfigParser library and simulates the evolution of the particle system according to the model equations and calculates the order parameter. At the end of the simulation, the coordinates and direction of the particles and the order parameter at each time step are saved in three different files in a data folder through their local paths set in the [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) file.

3. The user has to launch the [Animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Animation.py) file that loads the data from the data folder and creates a real time figure of the particles motion and the evolution of the order parameter as the transition to collective motion goes on. The figure is then automatically saved in the project folder.

# Project structure

The project is formed by 5 files:

1. [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) is a .ini file that contains the model parameter set by the user and the local paths used to save and load the data to be visualized.

2. [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py) is a .py file in which are defined all the functions needed for the model simulation. In particular, there is a function that generates the initial configuration (coordinates and direction) of the particles, a function that calculates the velocity components of each particle, a function that updates the particles configuration and a function that calculates the order parameter.

3. [Tests](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Test.py) is a .py file used to test functions defined in [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py).

4. [Simulation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Simulation.py) is a .py file that imports the model paramters from [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) and uses the functions
defined in [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py) file to simulate the model and calculate the order parameter. In this file the arrays of the particles coordinates and orientations and the order parameter at each time step are saved in the data folder.

5. [Animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Animation.py) is a .py file that imports the data from the data folder and creates, using mathplotlib.animation.FuncAnimated, a figure formed by a real time visualization of the particles motion and a real time plot of the order parameter. The figure is saved as animation.gif in the project folder.

# Simulation examples

Below are shown three examples of simulation obtained with different noise amplitude ![equation](https://latex.codecogs.com/svg.image?\eta) and fixed ![equation](https://latex.codecogs.com/svg.image?v_0&space;=&space;0.2), ![equation](https://latex.codecogs.com/svg.image?R_0&space;=&space;1.0), ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t&space;=&space;1.0), ![equation](https://latex.codecogs.com/svg.image?N&space;=&space;200) and ![equation](https://latex.codecogs.com/svg.image?T&space;=&space;250).
In particular [animation_1.gif](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_1.gif) is obtained by setting ![equation](https://latex.codecogs.com/svg.image?\eta&space;=&space;0.1), [animation_2.gif](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_2.gif) is characterized by ![equation](https://latex.codecogs.com/svg.image?\eta&space;=&space;0.5) and in [animation_3.gif](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_3.gif) ![equation](https://latex.codecogs.com/svg.image?\eta&space;=&space;0.9).
As expected, as the noise amplitude increases, the transition to the collective motion of particles is increasingly hampered. In fact, it is noted that for greater ![equation](https://latex.codecogs.com/svg.image?\eta) the order parameter reaches more slowly an almost unitary value and it is subject to greater fluctuations caused by the presence of a strong noise component.

![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_1.gif)
![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_2.gif)
![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_3.gif)
