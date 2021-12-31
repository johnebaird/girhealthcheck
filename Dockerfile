FROM python:3 

MAINTAINER John Baird <john.baird@genesys.com>

COPY girhealthcheck.py .

RUN apt-get update

RUN useradd -m -r -g users pythonuser

USER pythonuser

WORKDIR /home/pythonuser

RUN python -m pip install --upgrade pip --no-warn-script-location 

RUN pip install requests --no-cache-dir --no-warn-script-location
	
CMD ["python", "girhealthcheck.py"]




