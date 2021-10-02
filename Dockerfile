FROM registry.gitlab.com/competitions4/sciroc/dockers/sciroc:1.4

LABEL maintainer="Daniel López Puig <daniel.lopez@pal-robotics.com>"

ARG REPO_WS=/ws
RUN mkdir -p $REPO_WS/src
WORKDIR /home/user/$REPO_WS

# TODO: Put inside ./ws your ROS packges
COPY ./ws /home/user/ws

# TODO: add here the debians you need to install
#RUN apt install -y ros-melodic-<pkg_name> pal-ferrum-<pkg_name> <apt-pkg>

# TODO: check if these steps simplify the build process 
# COPY requirements.txt /opt/app/requirements.txt
# WORKDIR /opt/app
#RUN pip install -r requirements.txt


RUN apt install python3-pip -y
RUN apt install python3-pip python3-yaml -y
RUN apt install libportaudio2 -y
RUN apt install espeak -y
# SMACH Installation
RUN apt install ros-melodic-smach -y
RUN apt install ros-melodic-smach-ros -y
RUN apt install ros-melodic-executive-smach -y 
RUN apt install ros-melodic-smach-viewer -y

#RUN pip3 install -r requirements.txt

# Install libs that the waitbot package depends on

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir rospkg catkin_pkg
RUN pip3 install --no-cache-dir vosk
RUN pip3 install --no-cache-dir sounddevice
RUN pip3 install --user -U nltk
RUN pip3 install --no-cache-dir word2number
RUN pip3 install --no-cache-dir cdifflib
RUN pip3 install --no-cache-dir python-Levenshtein
RUN pip3 install --no-cache-dir fuzzywuzzy
RUN pip3 install --no-cache-dir fuzzywuzzy[speedup] 
RUN pip3 install --no-cache-dir pyttsx3

RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader averaged_perceptron_tagger
#RUN python3 -c "import nltk; nltk.download('punkt')"

# YOLOv5 installation
RUN pip3 install torch==1.8.2+cpu torchvision==0.9.2+cpu torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

RUN pip3 install --no-cache-dir matplotlib>=3.2.2
RUN pip3 install --no-cache-dir numpy>=1.18.5
RUN pip3 install --no-cache-dir opencv-python>=4.1.2
RUN pip3 install --no-cache-dir Pillow
RUN pip3 install --no-cache-dir PyYAML>=5.3.1
RUN pip3 install --no-cache-dir scipy>=1.4.1
RUN pip3 install --no-cache-dir tqdm>=4.41.0
RUN pip3 install --no-cache-dir tensorboard>=2.4.1
RUN pip3 install --no-cache-dir seaborn>=0.11.0
RUN pip3 install --no-cache-dir pandas
RUN pip3 install --no-cache-dir thop 

#RUN pip3 install -r yolo_requirements.txt

#
# Build and source your ros packages 
RUN bash -c "source /opt/pal/ferrum/setup.bash \
    && catkin build \
    && echo 'source /opt/pal/ferrum/setup.bash' >> ~/.bashrc" \
    && export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/user/ws/src/Sciroc2EP1-SimulatedEnv/models"
    # Add below line to automatically source your packages
    # && echo 'source $REPO_WS/devel/setup.bash' >> ~/.bashrc

WORKDIR /home/user/ws/src
RUN git clone https://github.com/GravastarsUNIWA/ScirocEpisode1.git
RUN git checkout docker-branch
RUN bash -c "cd /home/user/ws && catkin build && source /home/user/ws/devel/setup.bash"
ENTRYPOINT ["bash"]
