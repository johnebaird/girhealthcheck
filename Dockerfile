FROM ubuntu:latest

COPY girhealthcheck.py .

RUN apt-get update && apt-get install -y \
    python \
	&& rm -rf /var/lib/apt/lists/*
	

