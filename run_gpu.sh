#!/bin/bash

# prod
export BASE_IMAGE=nvidia/cuda:8.0-cudnn7-devel
export ENV=prod

docker-compose up -d