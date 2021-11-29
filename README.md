# Motion_Planning_for_Autonomous_Parking

## The Parking Problem
A common path planning problem for autonomous vehicles involves maneuvering in tight spaces and cluttered environments, particularly while parking. To address these issues, non-holonomic constraints of the vehicles must be taken into consideration. At the same time, collision checking algorithm must also be deployed to make sure the vehicle path is collision-free. Considering the above constraints, this project implements path planning for the following types of vehicles:
* A DiWheel Robot
* A car with Akerman Steering
* A car pulling Trailer

## About the environment
The project is implemented using the pygame library of python. The environment for the same is a parking lot in a two dimensional grid world. In each instance, a car starts at the Northwest corner of the bounded two dimensional field. The car is to be parked in a compact space in the southern border, flanked by vehicles both in front of and behind the target space. Additionally, there is an island in the central region. The environment approximately looks like the following:
![](Readme_files/Environment.png)

## DiWheel Kinematics

![](Readme_files/Diwheel.png)



https://user-images.githubusercontent.com/53962958/143936200-ef45402e-b3e2-4845-86d1-c1ec8888e690.mp4


![DiWheet_Path_Depection](https://user-images.githubusercontent.com/53962958/143936224-64f1acbc-0d66-4b89-b88f-d4c5f5865168.png)


## Akerman Steering

![](Readme_files/Akerman.png)


https://user-images.githubusercontent.com/53962958/143936309-f0bab79c-d6de-453b-85d6-061fe1ccf806.mp4



![Akerman_Path_depiction](https://user-images.githubusercontent.com/53962958/143936254-3d83e480-5936-4562-b792-ca077501dfee.png)

## A Car pulling Trailer

![](Readme_files/Trailer.png)



https://user-images.githubusercontent.com/53962958/143936321-e9bff339-687a-46f1-929c-8718e4d58e88.mp4



![Car_pulling_trailer_path_depection](https://user-images.githubusercontent.com/53962958/143936290-ce84a9c4-378b-4db5-a5bb-5a0abd35141e.png)
