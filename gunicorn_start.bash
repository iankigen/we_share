#!/bin/bash

NAME="we_share"
DJANGODIR=/home/ubuntu/we_share
SOCKFILE=/home/ubuntu/django_env/run/gunicorn.sock
USER=ubuntu
GROUP=ubuntu
NUM_WORKERS=3 #2*CPUs+1
DJANGO_SETTINGS_MODULE=share.settings
DJANGO_WSGI_MODULE=share.wsgi
echo "Starting $NAME as $whoami"

cd $DJANGODIR
source /home/ubuntu/django_env/bin/activate
source /home/ubuntu/we_share/.env
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start django gunicorn

exec gunicorn ${DJANGO_WSGI_MODULE}:application\
	 --name $NAME\
	 --workers $NUM_WORKERS\
	 --user=$USER\
	 --group=$GROUP\
	 --bind=unix:$SOCKFILE\
	 --log-level=debug