#!/bin/sh
set -ex

cd development
echo "Start running at $(pwd)"

echo "Running local environment..."
docker-compose pull && docker-compose build && docker-compose up