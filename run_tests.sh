#!/bin/bash

docker-compose run -w /opt/mreq/backend backend python -m unittest /opt/mreq/backend/tests.py