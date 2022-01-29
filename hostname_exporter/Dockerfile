FROM prom/node-exporter

COPY run.sh /run.sh

USER root

RUN mkdir /textfile && chmod 777 /textfile

USER nobody

ENTRYPOINT ["/bin/sh", "/run.sh", "--collector.textfile.directory=/textfile"]
