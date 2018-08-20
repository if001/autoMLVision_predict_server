#!/bin/sh
docker run -it -p 8181:80 -v ./src:/usr/local/auto_ml_server -d ubuntu:17.04
