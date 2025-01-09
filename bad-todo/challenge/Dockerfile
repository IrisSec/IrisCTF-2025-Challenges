FROM node:22 AS chroot
WORKDIR /src

COPY src/*.js src/*.json ./
COPY src/.env ./
COPY src/views ./views

RUN /usr/sbin/useradd -u 2137 user
COPY entry.sh /home/user/entry.sh
RUN chmod +x /home/user/entry.sh

RUN npm install

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/
CMD kctf_setup && kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/entry.sh