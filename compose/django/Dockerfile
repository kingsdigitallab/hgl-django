FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # curl for node
  && apt-get install -y curl \
  # mysql dependencies
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get install -y python-mysqldb python-dev \
  # lxml depedndencies
  && apt-get install -y libldap2-dev libsasl2-dev ldap-utils \
  && apt-get install -y libxml2-dev libxslt-dev python-dev \
  && apt-get install -y python3-lxml \
  #gdal libraries
  && apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /app
COPY requirements.txt /app
COPY ddhldap-django/requirements.txt /app/ddhldap-django/
COPY wagtailbase/requirements.txt /app/wagtailbase/


RUN pip install -U pip
RUN pip install -r requirements.txt
#COPY . /app/

COPY --chown=django:django ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
COPY --chown=django:django . /app

# todo we may not need this now
# COPY ./libgeos.py /usr/local/lib/python3.6/site-packages/django/contrib/gis/geos/
