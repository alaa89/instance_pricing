############################################################
# Dockerfile to build Flask Application Containers
# Based on Ubuntu 14.04
############################################################

# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Alaa Chatti

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y git curl wget build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python-dev python-pip

# Copy the application folder inside the container
RUN git clone https://github.com/alaa89/instance_pricing.git /instance_pricing

# Get pip to download and install requirements:
RUN pip install -r /instance_pricing/requirements.txt

# Expose ports
EXPOSE 8080

# Set the default directory where CMD will execute
WORKDIR /instance_pricing

RUN wget https://a0.awsstatic.com/pricing/1/deprecated/ec2/pricing-on-demand-instances.json

RUN python setup.py install

CMD python run.py
