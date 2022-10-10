# 2D Vicsek Model simulation

The Vicsek model is a self-organized motion model that plays a key role in the study of active matter, similar to that played by the Ising model for ferromagnetism. This model shows a transition from the disordered movement of individuals within the group to collective behavior, caused only by interindividual forces of alignment, without attraction and repulsion. Its simple dynamic rule has been adopted as a starting point for many generalizations and variations that have been applied to a wide range of different problems, such as the collective behavior of large groups of animals. The goal of this project is to simulate the two-dimensional Vicsek model.

# Model definition
The model describes the synchronous motion of a set of ![equation](https://latex.codecogs.com/svg.image?N) self-propelled Particles, i.e. provided with autonomous movement possibilities. These particles are represented by points in continuous motion on the plane, characterized by the position ![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t)) and the velocity ![equation](https://latex.codecogs.com/svg.image?\textbf{v}_i(t)), with constant modulus ![equation](https://latex.codecogs.com/svg.image?v_0) and direction ![equation](https://latex.codecogs.com/svg.image?\textbf{s}_i(t)=(\cos(\theta_i(t)),\sin(\theta_i(t)))). The index ![equation](https://latex.codecogs.com/svg.image?i) is the particle index ![equation](https://latex.codecogs.com/svg.image?i=1,...,N). The position of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle is updated at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t) according to the following dynamic evolution equation: 

![equation](https://latex.codecogs.com/svg.image?\textbf{r}_i(t+\Delta&space;t)=\textbf{r}_i(t)&plus;\textbf{v}_i(t)\Delta&space;t=\textbf{r}_i(t)&plus;v_0\begin{pmatrix}\cos(\theta_i(t))&space;\\\sin(\theta_i(t))\end{pmatrix}\Delta&space;t)

According to the basic idea of the model, particles tend to move in the same direction as their neighbors, therefore the angle that defines the direction of motion of the ![equation](https://latex.codecogs.com/svg.image?i)-th particle ![equation](https://latex.codecogs.com/svg.image?\theta_i(t)) is determined, at each time step ![equation](https://latex.codecogs.com/svg.image?\Delta&space;t), by the following update equation:

![equation](https://latex.codecogs.com/svg.image?\theta_i(t+\Delta&space;t)=Arg\left&space;[&space;\sum_{j=1}^{N}&space;n_{ij}(t)\textbf{s}_j(t)\right&space;]&plus;\eta_i(t))

Where the ![equation](https://latex.codecogs.com/svg.image?Arg) function returns the angle that defines the average direction of the velocity of the particles (including the ![equation](https://latex.codecogs.com/svg.image?i)-th) that are within a circle of radius ![equation](https://latex.codecogs.com/svg.image?R_0) centered in the reference particle. The connectivity matrix ![equation](https://latex.codecogs.com/svg.image?n_{ij}(t)) is in fact defined as:

![equation](https://latex.codecogs.com/svg.image?n_{ij}(t)=\begin{cases}&&space;1&space;\text{&space;if&space;}|\textbf{r}_i(t)-\textbf{r}_j(t)|<R_0\\\\&&space;0&space;\text{&space;if&space;}|\textbf{r}_i(t)-\textbf{r}_j(t)|>R_0\end{cases}&space;)

The alignment is hindered by a noise term ![equation](https://latex.codecogs.com/svg.image?\eta_{i}(t)) uniformly distributed in the interval ![equation](https://latex.codecogs.com/svg.image?[-\eta/2,\eta/2]), with amplitude ![equation](https://latex.codecogs.com/svg.image?\eta\in[0,1]), which plays a role similar to that of the temperature in equilibrium systems.

If the polar alignment term is strong enough to overcome the noise effect, the system develops a global orientation order and therefore a collective movement. This process can be studied by monitoring the polar order parameter ![equation](https://latex.codecogs.com/svg.image?\varphi(t)), analogue of the total magnetization in spin systems, defined as the modulus of the mean direction of motion of the entire system of particles:

![equation](https://latex.codecogs.com/svg.image?\varphi(t)=\frac{1}{N}\left|\sum_{i=1}^{N}&space;\textbf{s}_i(t)\right|)

The order parameter is approximately null if the directions of motion of the individual particles are distributed randomly, as the latter tend to cancel each other out in the sum; while for the phase of coherent motion, with an ordered direction of the velocities, it assumes a finite and approximately unitary value.

#
![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_1.gif)
![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_2.gif)
![animation](https://github.com/sofiraponi/2D_Vicsek_Model/blob/main/animation_3.gif)


