# AWS Instance Types Pricing
This a Flask Rest API exposing prices of AWS instance types per region. Given the region and the instance type, it provides the hourly price.

## Tools
The API has been developed using [Flask](http://flask.pocoo.org/) framework due to the flexibility that it provides. This API supports arguments that are sent as JSON data as well as query params (see Usage). For this reason, [webargs](https://webargs.readthedocs.io/en/latest/) has been adopted to handle this.

## Deployment
A Dockerfile is embedded to the project in order to setup and automate the deployment of the API. 
### *Prerequisites*
- Docker Installed
- Ubuntu 14.04 docker image downloaded

### *Steps*
1- Download and install docker on your computer. For reference, check [Docker](https://docs.docker.com/engine/installation/)

2- Once installed, Pull the Ubuntu 14.04 docker image which will be used as a base image for our deployment
```
 sudo docker pull ubuntu:14.04
```
3- Using the Dockerfile, containerize the application as follows
```
sudo docker build -t instance_pricing .
```

4- Once the build is done, we can start the service
```
sudo docker run --name instance_pricing -i -t instance_pricing
```
By default, Docker launches your containers in the *bridge* network. Check the container IP address:
```
sudo docker network inspect bridge
```

## Usage
By default, The API runs on port 8080
```
curl http://localhost:8080/
OK
```
```
curl http://localhost:8080/v1/pricing?instance_type=m1.large\&region=eu-west-1
0.260
```

```
curl -X POST -H "Content-Type: application/json" -d '{"instance_type":"m1.large","region":"eu-west-1"}' http://localhost:8080/v1/pricing
0.260
```
