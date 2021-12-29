FROM python:3 

MAINTAINER John Baird <john_baird@genesys.com>

COPY girhealthcheck.py .

RUN useradd -m -r -g users pythonuser

USER pythonuser

RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install requests --no-cache-dir
	
CMD ["python", "girhealthcheck.py"]

ENV RWS_HOSTS=http://192.168.45.81:8080
ENV RWS_USER=jbaird
ENV RWS_PASS=iihbdidj

ENV ES_HOSTS=http://192.168.45.81:9200,http://192.168.45.83:9200

ENV WEBDAV_HOSTS=http://192.168.45.81
ENV WEBDAV_USER=webdav
ENV WEBDAV_PASS=webdav

ENV RPS_HOSTS=http://192.168.45.81:8889

ENV RCS_HOSTS=http://192.168.45.81:8008



