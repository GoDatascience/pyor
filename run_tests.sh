#!/bin/bash

docker-compose -p mreq-tests run --rm -w /opt/mreq/backend backend python -m unittest /opt/mreq/backend/tests.py