#!/bin/sh
docker build -f Dockerfile.build --tag gem5build .
docker run -v ./build:/gem5/build -it gem5build
