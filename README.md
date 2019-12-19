# Collision Avoidance through Evloutionary Machine Learning.

In this project, agents/robots, learn to avoid both static and dynamic obstacles, with no prior knowledge of the enviornment that they operate in. Each robot is controlled by a neural network, the weights of the neural network are modified using a genetic algorithm. Over several generations, the robots achieve impressive behaviour.

<img src="images/demo.gif" width="400">

# The Simulation

This simulation is built using the 2d python game fraemwork Pygame. The simulation is simple, it can be thought of as a map, a thin white border marks the boundary of the map. The goal of the robot is to reach a small red target which is obstructed by some obstacle, such that the only way to reach the target is to avoid/manevoure around it.

The robot's lifespan ends when one of three conditions is met:
* The robot collides with an obstacle
* The robot collides with the boundaries of the map
* The time that the robot is alive exceedes a preset threshold
* The robot collides with the target

The third condition is put in place to prevent a situation where the robot achieves a speed of zero indefinitely and is therefore unable to move. The threshold is set such that is larget than the time required for sucessfully reaching the target. This means that it should onyl eliminate robots that get stuck.

The fourth and final conditions can be considered as the robot succesfully achieving the desired goal of reaching the target.

#### Static Case
In this project, two scenarios are tackled the first of which being a static case. This involves two stationary obstacles placed one after another and before the target. The robot's then spawn before the obstacle with the goal of reaching the target.

#### Dynamic Case
The dynamic scenario consists of a single obstacle which continuously moves up and down in a linear reciprocating motion with the target on the other side of the obstacle. This is much tougher since even if the robot is successful on a single attempt, this does not mean that it will succeed in future attempts as the obstacle may be in a different position which causes problems.

## The Robot

The robot has nine sensors which are placed around its circumference and equally spaced. These sensors measure distance to any nearby obstacles and it is these sensor readings that serve as input to the neural network. The neural network then outputs two continous values, one controlling the speed and the other controlling the direction of the robot. This process happens continuously all the time the robot is alive. It is these sensors that give the robot reactive behaviour - that is based on changing sensor readings the robot can adjust its speed and direction in real time. As a pose to similar project involving genetic algorithms which use a preselected set of direction vectors to map an agent's trajectory.


## The Neural Network
The Neural network used in this project is a vanilla feed forward neural network. It contains nine input neurons, since it takes readings from the nine sensor readings provided from the robot, three hidden layers each consisting of sixteen neurons, and an output layer consisting of two neurons, controlling the speed and direction of the robot respectively.

## The Genetic Algorithm
We initialise a robot population and they will all interact with the envrionemnt until their eventual deaths. A genetic algoirthm needs a way to evaluate the candidate solutions put forward, this is achieved using a fitness function. This is a function that reflects how well an individual peformed on the given task, with higher values meaning better performance. For example, an intuitve choice of fitness function for this project could be, the closest distance that the robot achieved to the target during its lifetime. Hence, robots who reached further towards the target would be assigned a higher score from the fitness function. Once the entire popluation has died each individual is evaluated according the fitness function. After this, the three key genetic operates are applied in order to form the next generation. These are, selection, crossover and mutation. In short, selection aims to select the fittest indivduals, crossover produces new individuals by combining the genes from two parents from the previous generation and mutation randomly modifies a childs genes with the purpose of injecting genetic diversity into the population.

## Combining a Neural Network and Genetic Algorithm
At this stage, you may be wondering how the two are related in this project. The neural networks weights essentially represent the candidate solution itself, and its these numerical values of the weights that the genetic algorithm operates on directly.









