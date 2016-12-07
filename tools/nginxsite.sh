#!/bin/bash
# Start or stop one site running on fcgi

DEBUG=""

if [ -n "$1" ]
# site name
then
	SITE=$1
else
	echo "Usage: $0 sitename start/stop [debug]"
	echo "Server will run on port 8+last 3 of UID (e.g. 8001)"
	exit 1
fi

if [ ! -d "/var/www/$SITE" ]
# site directory
then
	echo "Site $SITE doesn't exist!"
	echo "(must be a directory in /var/www)"
	exit 2
fi

if [ -n "$2" ]
# start/stop command
then
	COMMAND=$2
else
	COMMAND=start
fi

if [ -n "$3" ]
# Debug?
then
	echo "DEBUG mode active! Stop server with ^C!"
	DEBUG="daemonize=false maxrequests=1"
fi

PYTHON=/var/www/${SITE}/bin/python
SITEUSER=$SITE
PIDFILE=/var/www/${SITE}/logs/django.pid
DJANGODIR=/var/www/${SITE}/releases/current/${SITE}
# PORT is 8 + last 3 numbers of user ID (starting at 1000 on Debian)
PORT=`id -u $SITE`
PORT=8${PORT#1}

if [ $COMMAND == "stop" ]
then
	echo "Stopping $SITE..."
	kill `cat -- $PIDFILE`
	rm -f -- $PIDFILE
else
	export SERVER_PROTOCOL=http
	echo "Starting $SITE on port $PORT..."
	cd $DJANGODIR; $PYTHON $DJANGODIR/manage.py runfcgi method=threaded maxchildren=6 maxspare=4 minspare=2 host=127.0.0.1 port=$PORT pidfile=$PIDFILE $DEBUG
	/etc/init.d/nginx reload
fi


