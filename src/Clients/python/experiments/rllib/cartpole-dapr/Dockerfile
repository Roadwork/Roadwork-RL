FROM python:latest

WORKDIR /app

# Download dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy Source Code
COPY . .
RUN cd /app/Lib/python/roadwork; pip install -e .; cd /app

# Main Entry
CMD [ "python", "main.py" ]