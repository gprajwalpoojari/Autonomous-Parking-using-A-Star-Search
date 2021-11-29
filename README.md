# Motion_Planning_for_Autonomous_Parking

## The Parking Problem
A common path planning problem for autonomous vehicles involves maneuvering in tight spaces and cluttered environments, particularly while parking. To address these issues, non-holonomic constraints of the vehicles must be taken into consideration. At the same time, collision checking algorithm must also be deployed to make sure the vehicle path is collision-free. Considering the above constraints, this project implements path planning for the following types of vehicles:
* A DiWheel Robot
* A car with Akerman Steering
* A car pulling Trailer

## About the environment
The project is implemented using the pygame library of python. The environment for the same is a parking lot in a two dimensional grid world. In each instance, a car starts at the Northwest corner of the bounded two dimensional field. The car is to be parked in a compact space in the southern border, flanked by vehicles both in front of and behind the target space. Additionally, there is an island in the central region. The environment approximately looks like the following:
![](Readme_files/Environment.png)
