FROM python:3.7
MAINTAINER Rachael Tordoff

RUN pip3 -q install gunicorn==19.9.0 eventlet==0.24.1

COPY / /opt/

RUN pip3 install -q -r /opt/requirements.txt && \
    pip3 install -q -r /opt/requirements_test.txt

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]
