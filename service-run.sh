#!/usr/bin/env bash
# service runner for daemontools
SITE=tictactoe
SITEUSER=$SITE
# PORT is 8 + last 3 numbers of user ID (starting at 1000 on Debian)
PORT=`id -u $SITE`
PORT=8${PORT#1}

SITEDIR=/var/www/${SITE}
DJANGODIR=${SITEDIR}/releases/current/${SITE}
PYTHON=${SITEDIR}/bin/python
LOGDIR=${SITEDIR}/logs
PIDFILE=${LOGDIR}/django.pid
LOGS="outlog=${LOGDIR}/info.log errlog=${LOGDIR}/error.log"

# activate virtualenv
source ${SITEDIR}/bin/activate
cd ${SITEDIR}
# run django FCGI server; daemonize=false is right for daemontools!
#exec setuidgid $SITEUSER $PYTHON $DJANGODIR/manage.py runfcgi method=threaded maxchildren=6 maxspare=4 minspare=2 host=127.0.0.1 port=$PORT pidfile=$PIDFILE daemonize=false $LOGS
# run Gunicorn server
exec setuidgid $SITEUSER $PYTHON $DJANGODIR/manage.py run_gunicorn -c ${SITEDIR}/releases/current/gunicorn-settings.py
