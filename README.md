# Mujoco_walkingRobots

## Simple walking implementation using RL

### 0. Requirements : GYM, MUJOCO, stablebaselines3 + (Linux)

PATH : 

URDF : All links and joints are manually reverse engineered from assembly file from GRABCAD
https://grabcad.com/library

## 
### 1. MiniCheetah

#### 1.1. [Solidworks] re-assembly process :
https://youtu.be/irAciVODtpI


#### 1.2. [URDF] Hitbox design :
 using basic shape (Box, cylinder, sphere..)
![Hitbox](https://user-images.githubusercontent.com/74540268/169758719-4ecca46f-24fb-4cca-b3a1-0682afbeb4c0.PNG)


#### 1.3. [MUJOCO,GYM,sb3] Training results :
you can see the code for specific MDP setting(S,A,R..) info
   ![ezgif com-gif-maker (5)](https://user-images.githubusercontent.com/74540268/169943131-9eccfde6-9127-4d72-a83f-b7c9df6ee2b6.gif)

 
## 


### 2. Hexapod

#### 2.1. [Solidworks] re-assembly : 
![hexy_SW6](https://user-images.githubusercontent.com/74540268/169776703-d9660b52-a81e-4ba5-ab9a-c01d76072a12.PNG)



#### 2.2. [URDF] Hitbox design : 
![hexy_heat2](https://user-images.githubusercontent.com/74540268/169944721-46a89900-eaed-4b17-b6cb-a4496fd48ab6.PNG)




#### 2.3. [MUJOCO,GYM,sb3] Training results : 
you can see the code for specific MDP setting(S,A,R..) info
![hexy](https://user-images.githubusercontent.com/74540268/169943892-e235b3e9-8a02-46d0-a128-d9366a4c8f75.gif)



