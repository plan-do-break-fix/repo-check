#!/bin/bash
PROJECT=/home/user/repo-check

cd $PROJECT/app/Queueing
#cp $PROJECT/.dockerignore .
cp $PROJECT/app/Abstract/AbstractApp.py .
cp $PROJECT/app/Interfaces/Github.py .
cp $PROJECT/app/Interfaces/GithubApi.py .
cp $PROJECT/app/Interfaces/LocalRepo.py .
cp $PROJECT/app/Interfaces/MySql.py .
cp $PROJECT/app/Interfaces/RabbitMq.py .
docker build . --tag 'repo-check-orchestrator:1.0'
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm GithubApi.py
rm LocalRepo.py
rm MySql.py
rm RabbitMq.py
