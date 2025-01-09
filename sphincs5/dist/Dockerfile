FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag /
RUN apt-get update && apt-get install -y build-essential libssl-dev python3 socat
COPY sphincsplus/ /home/user/sphincsplus/
RUN cd /home/user/sphincsplus && make

CMD cd /home/user/sphincsplus && socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"python3 -u challenge.py"
