FROM ubuntu:22.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY . /home/user/

USER user
CMD ["sh", "-c", "cd /home/user && /home/user/vuln"]

