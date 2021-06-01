#!/bin/bash
PROJECT=/home/user/repo-check

cd $PROJECT/app/LaunchPad
#cp $PROJECT/.dockerignore .
cp $PROJECT/app/Interfaces/Mongo.py .
cp $PROJECT/app/Interfaces/MySql.py .
docker build . --tag 'repo-check-launchpad:1.0'
#rm .dockerignore
rm Mongo.py
rm MySql.py
