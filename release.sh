#!/bin/bash
set -xe

image_name="ex_domain"

trap 'clean_tmp; exit' QUIT TERM EXIT

function clean_tmp() {
  echo "clean temporary file..."
  [ -f Dockerfile.release ] && rm -rf Dockerfile.release
}

function release(){
  release_name="master"
  release_version="latest"

  if [ "$release_name" == "master" ];then
    branch_name=${release_name}
    git checkout ${branch_name}
  else
    branch_name=${release_name}-${release_version}
    git checkout ${branch_name}
  fi

  echo "Pull newest code..." && sleep 3
  git pull origin master

  # get commit sha
  git_commit=$(git log -n 1 --pretty --format=%h)


  # get git describe info
  version=${release_version}-${git_commit}

  sed "s/__VERSION__/$version/" Dockerfile >Dockerfile.release
  docker build --no-cache -t hub.goodrain.com/dc-deploy/archiver:${image_name} -f Dockerfile.release .
  docker push hub.goodrain.com/dc-deploy/archiver:${image_name}

}

case $1 in
    *)
    release
    clean_tmp
    ;;
esac
