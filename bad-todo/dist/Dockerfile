FROM node:22 AS chroot
WORKDIR /src

COPY src/*.js src/*.json ./
COPY src/.env ./
COPY src/views ./views

CMD /home/user/entry.sh
