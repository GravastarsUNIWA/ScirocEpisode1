# ros_yolov5 ReadMe

## Installation

1. Put the ros_yolov5 folder inside your ros workspace/src folder and rebuild the workspace
ex.

```mv ros_yolov5 /home/user/catkin_ws/src
roscd
cd ..
catkin_make
source devel/setup.bash
```
2. Install dependencies (see PDF)

## Usage
To change the weights that Yolov5 uses open ros_yolov5.launch on ros_yolov5/launch/ros_yolov5.launch and change the value of the parameter weights_path to point to your pt file

ros_yolov5 is now ready to run. open a terminal and run ```roslaunch ros_yolov5 ros_yolov5.launch```
