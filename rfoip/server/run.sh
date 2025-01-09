#!/bin/bash
docker run --rm -it -dt -p 7821:7821/udp -p 6531:6531 rfoip-server
