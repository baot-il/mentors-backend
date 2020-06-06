#!/bin/sh
set -ex

cd development
echo "Start running at $(pwd)"

echo "Cleaning local environment..."
docker-compose down --remove-orphans 