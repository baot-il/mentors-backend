#!/bin/sh
set -ex

cd development
echo "Start running at $(pwd)"

echo "Running local environment..."
docker-compose up -d --build pgadmin postgres-db