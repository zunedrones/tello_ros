FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update && apt-get install -y \
    sudo \
    cmake \
    git \
    pkg-config \
    libpython3-dev \
    libegl1-mesa-dev \
    libgl1-mesa-dev \
    libglew-dev \
    libepoxy-dev \
    libxkbcommon-dev \
    libopencv-dev \
    libboost-all-dev \
    libssl-dev \
    python3-pip \
    python3-opencv \
    ros-humble-cv-bridge \
    ros-humble-foxglove-bridge \
    ros-humble-rviz2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -ms /bin/bash --uid $USER_UID --gid $USER_GID $USERNAME \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME

RUN python3 -m pip install --user --no-cache-dir tello-zune

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["bash"]
