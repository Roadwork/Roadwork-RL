FROM python:3.7.8

WORKDIR /app

# Download dependencies
# Note: we install dependencies first since we don't want to keep reinstalling tensorflow during development
ADD requirements.txt .
RUN pip install -r requirements.txt

# Install Dapr patched for 3.7.8
RUN pip3 install dapr-ext-fastapi-dev

# Install Roadwork
RUN pip install roadwork==0.0.8

# Install src
COPY . .

# Main Entry
CMD [ "python", "train.py" ]