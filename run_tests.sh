#!/usr/bin/env bash

docker-compose -p pyor-tests run --rm -w /opt/pyor/backend backend python -m unittest /opt/pyor/backend/tests.py