FROM ubuntu:20.04

RUN apt-get update && apt-get install -y supervisor
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:gnuradio/gnuradio-releases
RUN apt-get install -y gnuradio gnuradio-dev cmake git libboost-all-dev \
	libcppunit-dev liblog4cpp5-dev python3-pygccxml pybind11-dev liborc-dev

# For debugging.
RUN apt-get install -y vim

WORKDIR /app
COPY flag.py /app/flag.py
COPY flag.wav /app/flag.wav
COPY connector_server.py /app/connector_server.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 7821/udp
EXPOSE 6531/tcp
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3/dist-packages"
CMD ["/usr/bin/supervisord"]
