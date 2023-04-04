#!/bin/sh
#
# Slovnikovy server daemon
#
# chkconfig: 345 95 5
# description: slovnikovy server daemon
#

# Source function library.
. /etc/rc.d/init.d/functions

prog="slovnik"
exec="/lib/python3.9"
prog_args="/home/pi/Desktop/ALPHA4/src"
user="root"

[ -x $exec ] || exit 0

start() {
    echo -n $"Starting $prog: "
    daemon --user=$user "$exec $prog_args"
    retval=$?
    echo
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    killproc $prog
    retval=$?
    echo
    return $retval
}

restart() {
    stop
    start
}

# See how we were called.
case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart|reload)
    restart
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac

exit $?
