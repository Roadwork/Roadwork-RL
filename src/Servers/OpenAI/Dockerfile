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
       python-opengl

# # Virtual Frame Buffer - needed as X11 display target where no monitor exists.
# RUN apt-get -y install xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps
# ADD docker/xvfb_init.sh /etc/init.d/xvfb
# RUN chmod a+x /etc/init.d/xvfb

# Output Dir
RUN mkdir -p /mnt/output-server

# Download dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy Source Code
COPY . .

# Main Entry
RUN chmod a+xr docker/start.sh

CMD [ "./docker/start.sh" ]
# CMD [ "python", "server.py" ]