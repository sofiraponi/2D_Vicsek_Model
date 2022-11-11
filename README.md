# 2D Vicsek Model simulation

The Vicsek model is a self-organized motion model that plays a key role in the study of active matter. This model shows a transition from the disordered movement of individuals within the group to collective behavior, caused only by interindividual forces of alignment, without attraction and repulsion. Many generalizations of the model have been applied to a wide range of problems, such as the collective behavior of large groups of animals. 

The goal of this project is to simulate the 2D Vicsek model and to visualize the phase transition through an animation of the particle system and a real-time plot of the evolution of the order parameter.

The user must use the following syntax to launch the simulation and visualize the animation from command line interface.

1. ```python Simulation.py settings.ini```

2. ```python Animation.py settings.ini```

## Model definition
The model describes the synchronous motion of ![equation](https://latex.codecogs.com/svg.image?N) self-propelled particles, characterized by the position ![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t)) and the velocity ![equation](https://latex.codecogs.com/svg.image?\textbf{v}_i(t)), with constant modulus ![equation](https://latex.codecogs.com/svg.image?v_0) and direction ![equation](https://latex.codecogs.com/svg.image?\textbf{s}_i(t)=(\cos\theta_i(t),\sin\theta_i(t))). The position of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle is updated at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t) according to the following dynamic evolution equation: 

![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t+\Delta&space;t)=\textbf{r}_i(t)&plus;\textbf{v}_i(t)\Delta&space;t=\textbf{r}_i(t)&plus;v_0\textbf{s}_i(t)\Delta&space;t)

Particles tend to move in the same direction as their neighbors, therefore the angle that defines the motion direction of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle ![equation](https://latex.codecogs.com/svg.image?\theta_i(t)) is determined, at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t), by the following update equation:

![equation](https://latex.codecogs.com/svg.image?\theta_i(t+\Delta&space;t)=Arg\left&space;[&space;\sum_{j=1}^{N}&space;n_{ij}(t)\textbf{s}_j(t)\right&space;]&plus;\eta\xi_i(t))

Where the ![equation](https://latex.codecogs.com/svg.image?Arg) function returns the average direction of the velocity of the particles (including the ![equation](https://latex.codecogs.com/svg.image?i)-th) that are within a circle of radius ![equation](https://latex.codecogs.com/svg.image?R_0) centered in the reference particle identified by means of the connectivity matrix ![equation](https://latex.codecogs.com/svg.image?n_{ij}(t)). The alignment is hindered by a noise term ![equation](https://latex.codecogs.com/svg.image?\eta\xi_{i}(t)) with amplitude ![equation](https://latex.codecogs.com/svg.image?\eta\in[0,1]) and ![equation](https://latex.codecogs.com/svg.image?\xi_{i}(t)\in[-\pi,\pi]). If the polar alignment term is strong enough to overcome the noise effect, the system develops a global orientation order and therefore a collective movement. This process can be studied by monitoring the polar order parameter ![equation](https://latex.codecogs.com/svg.image?\varphi(t)), defined as the modulus of the mean direction of motion of the entire system of particles:

![equation](https://latex.codecogs.com/svg.image?\varphi(t)=\frac{1}{N}\left|\sum_{i=1}^{N}&space;\textbf{s}_i(t)\right|)

The order parameter is approximately null if the directions of motion of the individual particles are distributed randomly; while for the phase of coherent motion, with an ordered direction of the velocities, it assumes a finite and approximately unitary value.

## Model simulation
The steps that the user must follow to perform the simulation and visualize both the particles motion and the evolution of the order parameter are the following:

1. The user has to set the model parameters in the [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) file. In particular, the user has to choose: the particle velocity modulus ![equation](https://latex.codecogs.com/svg.image?v_0), the noise amplitude ![equation](https://latex.codecogs.com/svg.image?\eta), the interaction radius ![equation](https://latex.codecogs.com/svg.image?R_0), the time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t), the number of particles ![equation](https://latex.codecogs.com/svg.image?N), the linear dimension of the system ![equation](https://latex.codecogs.com/svg.image?L) and the number of steps ![equation](https://latex.codecogs.com/svg.image?N_s). The user must follow some constraints in setting these parameters in order to observe the transition to collective motion, namely: ![equation](https://latex.codecogs.com/svg.image?v_0>0) since the model concerns particles in motion, ![equation](https://latex.codecogs.com/svg.image?\eta\in[0,1]) by definition, ![equation](https://latex.codecogs.com/svg.image?R_0>0) otherwise the system would be a set of independent random walkers and ![equation](https://latex.codecogs.com/svg.image?N) must be high enough since the model concerns a collective behavior (usually ![equation](https://latex.codecogs.com/svg.image?N\geq10)).

2. The user has to launch the [Simulation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Simulation.py) file which imports the model parameters from the [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) file through the ConfigParser library,simulates the evolution of the particle system according to the model equations starting from a random initial configuration and satisfying the periodic boundary conditions and calculates the order parameter. At the end of the simulation, the coordinates and direction of the particles and the order parameter at each time step are saved in three different files in a data folder through their local paths set in the [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) file. To launch the [Simulation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Simulation.py) file from command line interface the user must type ```python Simulation.py <name of configuration file>```, where in this case the name of the configuration file is *settings.ini*.

3. The user has to launch the [Animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Animation.py) file that loads the data from the data folder and creates a real time figure of the particles motion and the evolution of the order parameter as the transition to collective motion goes on. The figure is then automatically saved in the project folder. To launch the [Animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Animation.py) file from command line interface the user must type ```python Animation.py <name of configuration file>```, where in this case the name of the configuration file is *settings.ini*.

## Project structure

The project is formed by 5 files:

1. [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) is a .ini file that contains the model parameter set by the user and the local paths used to save and load the data to be visualized.

2. [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py) is a .py file in which are defined all the functions needed for the model simulation.

3. [Tests](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Test.py) is a .py file used to test functions defined in [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py).

4. [Simulation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Simulation.py) is a .py file that imports the model paramters from [settings](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/settings.ini) and uses the functions
defined in [Vicsek_Model](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Vicsek_Model.py) file to simulate the model and calculate the order parameter. The arrays of the particles coordinates and orientations and the order parameter at each time step are saved in the data folder.

5. [Animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/Animation.py) is a .py file that imports the data from the data folder and creates, using mathplotlib.animation.FuncAnimated, a figure formed by a real time visualization of the particles motion and a real time plot of the order parameter. The figure is saved as animation.gif in the project folder.

## Simulation examples

Below are shown three examples of the simulation, [animation_1](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_1.gif), [animation_2](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_2.gif) and [animation_3](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_3.gif), obtained with increasing noise amplitude ![equation](https://latex.codecogs.com/svg.image?\eta) and fixed all the other parameters. As expected, as the noise amplitude increases, the transition to the collective motion of particles is more and more hampered.

### Animation 1
Command line syntax: ```python Simulation.py settings_1.ini``` , ```python Animation.py settings_1.ini```


![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_1.gif)

### Animation 2
Command line syntax: ```python Simulation.py settings_2.ini``` , ```python Animation.py settings_2.ini```


![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_2.gif)

### Animation 3
Command line syntax: ```python Simulation.py settings_3.ini``` , ```python Animation.py settings_3.ini```


![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_3.gif)
