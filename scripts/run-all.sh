#!/bin/bash

cd /home/user/repo-check
export $(xargs < .env)
export $(xargs < .secret.env)
docker-compose up --detach
