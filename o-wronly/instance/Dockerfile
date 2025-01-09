FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y qemu-system-x86

COPY start.sh /start.sh
COPY artifacts/ /artifacts/
COPY flag /flag

CMD ["/start.sh"]
