# base image  
FROM python:3.8.10

# update apt and install sudo and essentials
RUN apt-get update && \
    apt-get -y install sudo && \
    apt-get install build-essential

# set environment variables  
ENV LC_ALL=pt_BR.UTF-8
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV TZ=America/Sao_Paulo

# upgrade pip  
RUN pip install --upgrade pip  

# setup environment variable  
ENV DOCKER_HOME=/home/cbers_cc

# set work directory 
RUN mkdir -p $DOCKER_HOME

# where your code lives  
WORKDIR $DOCKER_HOME

# copy whole project to your docker home directory. 
COPY ./src/cbers_cc $DOCKER_HOME

# copy .env
COPY .env $DOCKER_HOME/cbers_cc

# upgrade pip again 
RUN pip install --upgrade pip  

# run this command to install all dependencies  
RUN pip install -r requirements.txt

# port where the Django app runs  
EXPOSE 5000

# Copy docker entry point
COPY ./docker-entrypoint.sh $DOCKER_HOME

# entrypoint
RUN chmod +x ./docker-entrypoint.sh
CMD ["sh", "./docker-entrypoint.sh"]