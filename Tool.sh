#!/bin/bash

run() {
    sudo pip3 install gunicorn
    gunicorn -w 4 -t 600 -b 0.0.0.0:5000 app:app
}

pull() {
    git fetch --all
    git reset --hard origin/master
}

push() {
    clear
    git add .
    git commit -m "update"
    git push origin
}

clear() {
    rm nohup.out 
    rm app/nohup.out
    rm -fr __pycache__
    rm -fr app/__pycache__
}

if [ "$1" == "pull" ]; then
    pull

elif [ "$1" == "push" ]; then
    push

elif [ "$1" == "clear" ]; then
    clear

elif [ "$1" == "run" ]; then
    run

elif [ "$1" == "" ]; then
    echo "
run
pull
push
clear
"

fi
