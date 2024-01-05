# set of instructions to build the image
 
FROM python:3.11-alpine
 
WORKDIR /app
 
ENV PYTHONUNBUFFERED 1
 
COPY requirements.txt /app
 
RUN pip3 install -r requirements.txt --no-cache-dir
 
COPY . /app
 
EXPOSE 8000
 
ENTRYPOINT ["gunicorn", "device_server.wsgi:application"]
 
 
CMD ["--workers", "4","--thread", "3", "--bind","0.0.0.0:8000","--access-logfile", "access.log", "--error-logfile", "error.log"]