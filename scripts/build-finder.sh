#!/bin/bash
PROJECT=/home/user/mndatus

cd $PROJECT/app/Finder
#cp $PROJECT/.dockerignore .
cp $PROJECT/app/Abstract/AbstractApp.py .
cp $PROJECT/app/Interfaces/Github.py .
cp $PROJECT/app/Interfaces/Gitstar.py .
cp $PROJECT/app/Interfaces/GithubApi.py .
cp $PROJECT/app/Interfaces/MySql.py .
cp $PROJECT/app/Interfaces/Sqlite.py .
docker build . --tag 'mndatus-finder:1.0'
rm .dockerignore
rm AbstractApp.py
rm Github.py
rm Gitstar.py
rm GithubApi.py
rm MySql.py
rm Sqlite.py
