# ros_yolov5 ReadMe

## Installation

1. Clone the repository to ```/home/user/catkin_ws/src```

```
cd /home/user/catkin_ws/src
git clone https://github.com/GravastarsUNIWA/ScirocEpisode1.git
cd ScirocEpisode1
git checkout YOLOv5
```
2. 
>Then compile the package and source the workspace
```
cd ..
catkin_make
```

## Install dependencies
### Install anaconda
Yolov5 uses python 3.8. To install go [here](https://tech.serhatteker.com/post/2019-12/upgrade-python38-on-ubuntu/). The installation of the dependencied is done using [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html). 

### Install dependencies
1. Create a new virtual environment named venv
```
conda create -n venv python=3.8 jupyter
```

2. Activate new virtual environment
```
conda activate venv
```
3. Install [pytorch](https://pytorch.org/get-started/locally/).
4. Install other dependencies 
```
sudo apt-get install python3-pip python3-yaml
pip3 install -r requirements.txt
pip3 install rospkg catkin_pkg
```

## Choose python interpreter
Modify the shebang at the top of ros_yolov5.py file at ```ros_yolov5/src/ros_yolov5.py```
e.g. Default: ``` #!/usr/bin/env/python```
Modified: ```#!/usr/bin/env/python3``` or ```#!/home/<name of user>/miniconda3/envs/venv/bin/python```




## Usage
To change the weights that Yolov5 uses open ros_yolov5.launch on ros_yolov5/launch/ros_yolov5.launch and change the value of the parameter weights_path to point to your pt file. 

ros_yolov5 is now ready to run. open a terminal and run ```roslaunch ros_yolov5 ros_yolov5.launch```

For more information see the ReadMe.pdf