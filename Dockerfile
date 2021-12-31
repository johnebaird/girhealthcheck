FROM python:3 

MAINTAINER John Baird <john.baird@genesys.com>

RUN useradd -m -r -g users pythonuser

USER pythonuser

WORKDIR /home/pythonuser

COPY girhealthcheck.py .

RUN pip install requests --no-cache-dir --no-warn-script-location
	
CMD ["python", "girhealthcheck.py"]




