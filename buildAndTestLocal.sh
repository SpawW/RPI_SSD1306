#!/bin/bash

IMAGE_NAME="spaww/ssd_1306"
CONTAINER_NAME="display_ssd_1306"

docker build -t ${IMAGE_NAME} .

if [ "$(docker ps -a -f name=${CONTAINER_NAME})" ]; then
    echo "Removing old container..."
    docker rm -f ${CONTAINER_NAME}
fi

docker run -d --restart always -v ./:/app --name ${CONTAINER_NAME} ${IMAGE_NAME}

echo "Container running... Show logs..."

docker logs ${CONTAINER_NAME} -f -n 10
