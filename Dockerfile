FROM python:3 

MAINTAINER John Baird <john_baird@genesys.com>

COPY girhealthcheck.py .

#RUN useradd -r -g users pythonuser

#USER pythonuser

RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install requests --no-cache-dir
	
CMD ["python", "girhealthcheck.py"]
