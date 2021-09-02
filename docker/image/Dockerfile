FROM registry.gitlab.com/competitions4/sciroc/dockers/sciroc

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

# Build and source your ros packages 
RUN bash -c "source /opt/pal/ferrum/setup.bash \
    && catkin build \
    && echo 'source /opt/pal/ferrum/setup.bash' >> ~/.bashrc"
    # Add below line to automatically source your packages
    # && echo 'source $REPO_WS/devel/setup.bash' >> ~/.bashrc

ENTRYPOINT ["bash"]
