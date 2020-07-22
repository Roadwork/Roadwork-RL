FROM python:latest

WORKDIR /app

# Install System Dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apt-utils \
       build-essential \
       curl \
       xvfb \
       ffmpeg \
       xorg-dev \
       libsdl2-dev \
       swig \
       cmake \
       python-opengl \
       dos2unix

# # Virtual Frame Buffer - needed as X11 display target where no monitor exists.
# RUN apt-get -y install xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps
# ADD docker/xvfb_init.sh /etc/init.d/xvfb
# RUN chmod a+x /etc/init.d/xvfb

# Output Dir
RUN mkdir -p /mnt/output-server

# Download dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# @todo: should be removed if dapr supports 3.7
# Install Dapr patched for 3.7.8
RUN git clone https://github.com/dapr/python-sdk.git dapr-python-sdk
RUN cd dapr-python-sdk; sed -i 's/python_requires = >=3.8/python_requires = >=3.7/g' setup.cfg; pip install -e .; cd ..;

# Install and Patch Flask Dapr (is in dapr-python-sdk/ext/flask_dapr)
RUN cd dapr-python-sdk/ext/flask_dapr; sed -i 's/python_requires = >=3.8/python_requires = >=3.7/g' setup.cfg; pip install -e .; cd ../../../;

# Copy Source Code
COPY . .

# Fix line endings on our start script
RUN dos2unix docker/start.sh

# Main Entry
RUN chmod a+xr docker/start.sh

CMD [ "./docker/start.sh" ]
# CMD [ "python", "server.py" ]