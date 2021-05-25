#!/bin/bash

cd /home/user/mndatus
export $(xargs < .env)
export $(xargs < .secret.env)
docker-compose up --detach
