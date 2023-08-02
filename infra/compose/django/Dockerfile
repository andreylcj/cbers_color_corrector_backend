# base image  
FROM python:3.8.10


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


# update apt and install sudo and essentials
RUN apt-get update \
  && apt-get -y install sudo \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN mkdir -p $/home/cbers_cc
WORKDIR /home/cbers_cc


# upgrade pip  
RUN pip install --upgrade pip


# set environment variables  
ENV LC_ALL=pt_BR.UTF-8
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV TZ=America/Sao_Paulo


# run this command to install all dependencies
COPY ./src/cbers_cc/requirements.txt requirements.txt
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt


COPY ./infra/compose/django/entrypoint entrypoint
RUN sed -i 's/\r$//g' entrypoint
RUN chmod +x entrypoint


COPY ./infra/compose/django/start start
RUN sed -i 's/\r$//g' start
RUN chmod +x start


COPY ./infra/compose/django/celery/worker/start start-celeryworker
RUN sed -i 's/\r$//g' start-celeryworker
RUN chmod +x start-celeryworker


ENTRYPOINT ["/home/cbers_cc/entrypoint"]