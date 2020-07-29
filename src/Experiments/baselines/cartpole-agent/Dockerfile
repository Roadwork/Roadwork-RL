FROM python:3.7.8

WORKDIR /app

# Download dependencies
# Note: we install dependencies first since we don't want to keep reinstalling tensorflow during development
ADD requirements.txt .
RUN pip install -r requirements.txt

# @todo: should be removed if dapr supports 3.7
# Install Dapr patched for 3.7.8
RUN git clone https://github.com/dapr/python-sdk.git dapr-python-sdk
RUN cd dapr-python-sdk; sed -i 's/python_requires = >=3.8/python_requires = >=3.7/g' setup.cfg; pip install -e .; cd ..;

# Install and Patch Flask Dapr (is in dapr-python-sdk/ext/flask_dapr)
RUN cd dapr-python-sdk/ext/flask_dapr; sed -i 's/python_requires = >=3.8/python_requires = >=3.7/g' setup.cfg; pip install -e .; cd ../../../;

# Install Roadwork
RUN pip install roadwork==0.0.8

# Install src
COPY . .

# Main Entry
CMD [ "python", "train.py" ]