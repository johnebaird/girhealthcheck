FROM python:3 

MAINTAINER John Baird <john.baird@genesys.com>

COPY girhealthcheck.py .

RUN apt-get update

RUN useradd -m -r -g users pythonuser

USER pythonuser

RUN python -m pip install --upgrade pip \
    && pip install requests --no-cache-dir
	
CMD ["python", "girhealthcheck.py"]




