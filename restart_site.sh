#!/bin/bash

WEBSITE="/escnfs/home/jblake4/db/never_delayers/website.py" 

#change venv path for other machines
VENV_PATH="/escnfs/home/jblake4/db/never_delayers/dbenv"

source "$VENV_PATH/bin/activate"

PID=$(pgrep -f "$WEBSITE")
if [ -n "$PID" ]; then
echo "Stopping $WEBSITE with PID $PID"
kill -9 $PID
else
echo "$WEBSITE is not running"
fi

echo "Starting $WEBSITE"
nohup python3 $WEBSITE &>/dev/null &

deactivate