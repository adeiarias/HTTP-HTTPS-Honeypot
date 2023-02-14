FROM alpine:3.16

RUN apk --no-cache -U add \
        libcap \
	    openssl \
        py3-pip \
        python3

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./code /app
RUN mkdir -p /app/logs /app/ssl
RUN touch /app/logs/honeypot.log
RUN chmod 777 /app/logs/honeypot.log
RUN openssl req \
        -nodes \
        -x509 \
        -newkey rsa:2048 \
        -keyout "/app/ssl/key.pem" \
        -out "/app/ssl/cert.pem" \
        -days 365 \
        -subj '/C=ES/ST=Arrasate/O=Manufacturing S.A.' && \
    addgroup -g 2000 ubuntu && \
    adduser -S -H -s /bin/ash -u 2000 -D -g 2000 ubuntu && \
    chown -R ubuntu:ubuntu /app && \
    setcap cap_net_bind_service=+ep /usr/bin/python3.10 && \
    apk del --purge openssl && \
    rm -rf /root/* && \
    rm -rf /var/cache/apk/*

STOPSIGNAL SIGINT
USER root
CMD ["/usr/bin/python3", "application.py"]
