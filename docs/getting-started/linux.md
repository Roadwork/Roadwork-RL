# Getting Started - Linux Terminal

It is possible to run this under a terminal environment. For this we have to install a virtual screen through `sudo apt install xvfb` and starting it up with `xvfb-run -s "-screen 0 1400x900x24" bash`.

## Installation

The following script can be utilized to install all the packages on an Ubuntu Distribution. Execute this from the root directory.

```bash
# 1. Installing Dependencies
sudo apt install ffmpeg xvfb python-opengl 
sudo apt install swig # Required for OpenAI Box2D Environment
sudo apt install xorg-dev libglu1-mesa libgl1-mesa-dev xvfb libxinerama1 libxcursor1 # Virtual Screens
sudo apt install nvidia-384 nvidia-modprobe # Add NVIDIA Support

# 2. Installing Anaconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p $HOME/miniconda

# 3. Install Python Library
# Note: currently not in the Pip repo yet
pip install -e ./src/Lib/python/roadwork
```

## Running Experiments

### CartPole

```bash
# Start Server
./Scripts/linux/run-server.sh openai $(pwd)/../output-server/cartpole

# Start Experiment
./Scripts/linux/run-experiment.sh python cartpole
```

### Lunar Lander

```bash
# Start Server
./Scripts/linux/run-server.sh openai $(pwd)/../output-server/lunar-lander

# Start Experiment
./Scripts/linux/run-experiment.sh python lunar-lander
```