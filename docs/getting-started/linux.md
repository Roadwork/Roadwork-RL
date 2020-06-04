# Getting Started - Linux Terminal

It is possible to run this under a terminal environment. For this we have to install a virtual screen through `sudo apt install xvfb` and starting it up with `xvfb-run -s "-screen 0 1400x900x24" bash`.

## Installation

The following script can be utilized to install all the packages on an Ubuntu Distribution:

```bash
# 1. Installing Dependencies
sudo apt install ffmpeg xvfb python-opengl 

# 2. Installing Anaconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p $HOME/miniconda
```


### Installing Libraries

## Running Experiments

### CartPole

```bash
# Start Server
./Scripts/run-server.sh openai /mnt/e/Projects/roadwork-rl/output-server

# Start Experiment
./Scripts/run-experiment.sh python cartpole
```

### Lunar Lander