# Build go app
FROM golang:1.23 AS golang
WORKDIR /src

COPY src/go.mod src/go.sum ./
COPY src/*.go ./

RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o /tmp/app

# MySQL server
FROM ubuntu:22.04 AS chroot

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update
RUN apt-get install mysql-server -y

COPY setup.sql /home/user/
RUN bash -c "mysqld_safe &" && sleep 5 && mysql < /home/user/setup.sql
RUN cp -r /var/lib/mysql /home/user/data
RUN chown -R user:user /home/user/data
COPY entrypoint.sh /home/user/
COPY src/users.json /home/user/
RUN chmod +x /home/user/entrypoint.sh
COPY /src/pages /home/user/pages
COPY --from=golang /tmp/app /home/user/app

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/entrypoint.sh