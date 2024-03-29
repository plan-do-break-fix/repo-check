#!/bin/bash
PROJECT=/home/user/repo-check

# Repo Finder
cd $PROJECT/app/Finder
#cp $PROJECT/.dockerignore .
cp $PROJECT/app/Abstract/AbstractApp.py .
cp $PROJECT/app/Interfaces/Github.py .
cp $PROJECT/app/Interfaces/GithubApi.py .
cp $PROJECT/app/Interfaces/MySql.py .
cp $PROJECT/app/Interfaces/Sqlite.py .
docker build . --tag 'repo-check-finder:1.0'
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm Gitstar.py
rm GithubApi.py
rm MySql.py
rm Sqlite.py

# Inspector
cd $PROJECT/app/Inspector
#cp $PROJECT/.dockerignore .
cp $PROJECT/app/Abstract/AbstractApp.py .
cp $PROJECT/app/Interfaces/Github.py .
cp $PROJECT/app/Interfaces/LocalRepo.py .
cp $PROJECT/app/Interfaces/Mongo.py .
cp $PROJECT/app/Interfaces/MySql.py .
cp $PROJECT/app/Interfaces/RabbitMq.py .
docker build . --tag 'repo-check-inspector:1.0'
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm LocalRepo.py
rm Mongo.py
rm MySql.py
rm RabbitMq.py

# Queueing
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

# Message Queue
cd $PROJECT/app/MessageQueue
docker build . --tag 'repo-check-rabbitmq:1.0'

cd /home/user/repo-check
docker pull mysql:5.7
docker pull mongo:4.4-bionic
