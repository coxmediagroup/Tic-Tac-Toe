#!/bin/sh
# Start/stop/restart all enabled Nginx sites

PROG=/path/to/nginxsite.sh
WEBSITES=`ls -AbBU --color=never /etc/nginx/sites-enabled`
PARAM=start

test -f $PROG || exit 0
case "$1" in
    start)
        echo "Starting Sites"
        ;;
    stop)
        echo "Stopping Sites"
        PARAM=stop
        ;;
    restart)
        echo "Restart Sites"
        $0 stop
        $0 start
        exit 0
        ;;
    *)
        echo "usage:
 $0 start | stop | restart"
        exit 1
        ;;
esac

for WS in $WEBSITES
do
	$PROG $WS $PARAM
done

