#!/bin/bash
PROJECT=/home/user/repo-check

# Repo Finder
cd $PROJECT/app/Finder
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm Gitstar.py
rm GithubApi.py
rm MySql.py
rm Sqlite.py

# Inspector
cd $PROJECT/app/Inspector
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm LocalRepo.py
rm Mongo.py
rm MySql.py
rm RabbitMq.py

# Queueing
cd $PROJECT/app/Queueing
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm GithubApi.py
rm LocalRepo.py
rm MySql.py
rm RabbitMq.py
