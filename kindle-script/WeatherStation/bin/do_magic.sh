#!/bin/sh
REFRESH_TIME=10
sleep 4
eips -c
echo > key
while [ 1 ]; do
    eips -g /mnt/us/extensions/mirror/bin/screen.png
    waitforkey > key
    PID=$!
    sleep $REFRESH_TIME
    kill $PID
    if [ `head -n1 key | cut -c1` == "1" ]; then
        rm key
        exit 0
    fi
done
