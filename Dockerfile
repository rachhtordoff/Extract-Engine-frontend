FROM python:3.9
MAINTAINER Rachael Tordoff


RUN apt-get install -y libpq-dev

# copy and install requirements before the rest of the sourcecode to allow docker caching to work
copy requirements.txt /opt/requirements.txt
copy requirements_test.txt /opt/requirements_test.txt
RUN pip3 install -q -r /opt/requirements.txt && \
    pip3 install -q -r /opt/requirements_test.txt
    

COPY / /opt/

EXPOSE 8000

WORKDIR /opt


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--pythonpath", "/opt", "--timeout", "100000", "--access-logfile", "-", "manage:manager", "--reload"]
