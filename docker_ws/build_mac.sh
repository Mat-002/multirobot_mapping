#!/bin/bash

IMAGE_NAME="prj"
IMAGE_TAG="jazzy"
 
echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
 
docker build \
  -t "${IMAGE_NAME}:${IMAGE_TAG}" \
  -f "$(dirname "$0")/Dockerfile.prj" \
  "$(dirname "$0")"
 
if [ $? -eq 0 ]; then
    echo "Build completed: ${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "Build failed."
    exit 1
fi
 
