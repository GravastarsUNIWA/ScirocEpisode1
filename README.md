# ScirocEpisode1
---

This is the official Github repo of the GravaStars team of University of West Attica, for the remote participation in the Second SciRoc Challenge 2021, Episode 1, [E01: Coffee Shop](https://sciroc.org/e01-coffee-shop/). This work was awarded with the second place in the SciRoc Challenge 2021 competition.

All the members *contributed equally* in the following project. The members of the team are the following in alphabetical order:

- Antikatzidis Angelos
- Chamiti Tzoulio
- Chatzithanos Paris 
- Kaloterakis Evangelos
- Panagopoulos Dimitris
- Pappas Pantelis
- Petousakis Giannis
- Tsagkournis Evangelos
- Nikolaou Grigoris

## General Description
In this episode the robot will assist the staff of a coffee shop to take care of their customers. The robot is required to recognise and report the status of all tables inside the shop, to take orders from customers and to deliver objects to and from the customers’ tables. The main functionalities that are evaluated in this episode are **people perception** and **object perception** .


## Installation Guide

### 1. Create a directory for the Tiago workspace

  `mkdir ~/tiago_public_ws && cd ~/tiago_public_ws`
  
### 2. Download [tiago_public.rosinstall](https://raw.githubusercontent.com/pal-robotics/tiago_tutorials/kinetic-devel/tiago_public-melodic.rosinstall) (right-click and save link as...) and put it inside the workspace created before.

### 3. With this command, every needed repo is downloaded inside a src folder.

  `rosinstall src /opt/ros/melodic tiago_public-melodic.rosinstall`

  `Update the rosdep`

  `rosdep update`
  
### 4. Install all the dependencies for Tiago

`rosdep install --from-paths src --ignore-src -y --rosdistro melodic --skip-keys="opencv2 opencv2-nonfree pal_laser_filters speed_limit_node sensor_to_cloud hokuyo_node libdw-dev python-graphitesend-pip python-statsd pal_filters pal_vo_server pal_usb_utils pal_pcl pal_pcl_points_throttle_and_filter pal_karto pal_local_joint_control camera_calibration_files pal_startup_msgs pal-orbbec-openni2 dummy_actuators_manager pal_local_planner gravity_compensation_controller current_limit_controller dynamic_footprint dynamixel_cpp tf_lookup opencv3 joint_impedance_trajectory_controller"`

### 5. Git clone the UNIWA repo

  `git clone https://github.com/GravastarsUNIWA/ScirocEpisode1.git`
  
### 6. Submodule initialization

`git submodule init`

`git submodule update`

### 7. Source ROS with the newly installed dependencies and compile the packages

  `source /opt/ros/melodic/setup.bash`
  
  `catkin_make`
  
## Execute

`roslaunch uniwa_nav_stack main.launch `

  
