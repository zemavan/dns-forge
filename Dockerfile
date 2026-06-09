FROM ubuntu/bind9

RUN apt-get update && \
    apt-get install -y nano && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    bind9 \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY python-script.py .

RUN chmod +x python-script.py

EXPOSE 1053/tcp 1053/udp

CMD ["./python-script.py"]