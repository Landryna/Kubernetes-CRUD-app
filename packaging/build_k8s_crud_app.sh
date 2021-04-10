#!/bin/bash
# copy src files into docker dir
cp -r ../application/src docker/

function import_container_to_containerd {
  docker save $IMAGE_TAG:$IMAGE_VERSION > tmp.tgz
  microk8s ctr image import tmp.tgz
  rm tmp.tgz
}

function remove_container {
  docker kill $IMAGE_TAG
  docker rm $IMAGE_TAG
}

IMAGE_TAG=$1
IMAGE_VERSION=$2
CONTAINER_WORKDIR=/test

# build docker image
docker build -t $IMAGE_TAG:$IMAGE_VERSION -f docker/Dockerfile .

# remove copied src files
rm -r docker/src/

VOLUME_PATH=$PWD
VOLUME_PATH=`dirname $VOLUME_PATH`/application/test

docker run -d --name $IMAGE_TAG --env PYTHONPATH=/src -v $VOLUME_PATH:$CONTAINER_WORKDIR \
       -w $CONTAINER_WORKDIR --entrypoint sleep $IMAGE_TAG:$IMAGE_VERSION 1000

docker exec -u root $IMAGE_TAG pip3 install retry radish radish-bdd
docker exec -u root $IMAGE_TAG radish -b radish features/ --no-ansi --write-steps-once

if [ $? -ne 0 ] ; then
  echo "Tests failed."
  remove_container
  exit 1
fi

import_container_to_containerd
remove_container
echo "Tests passed, image is available on microk8s."

