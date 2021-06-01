#!/bin/bash

cd /home/user/repocheck
export $(xargs < .env)
export $(xargs < .secret.env)
docker-compose up --detach
