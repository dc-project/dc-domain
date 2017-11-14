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
  docker build --no-cache -t projectdc/${image_name}:${release_name} -f Dockerfile.release .

}

function encode_release(){
  release_name="dev"
  release_version="latest"

  if [ "$release_name" == "dev" ];then
    branch_name=${release_name}
    git checkout ${branch_name}
  else
    branch_name=${release_name}-${release_version}
    git checkout ${branch_name}
  fi

  echo "Pull newest code..." && sleep 3
  git pull origin dev

  # get commit sha
  git_commit=$(git log -n 1 --pretty --format=%h)


  # get git describe info
  version=${release_version}-${git_commit}

  sed "s/__VERSION__/$version/" Dockerfile.encode >Dockerfile.release

  cat > ./.gitignore <<EOF
.release/
release.sh
.idea/
.env/
__pycahche__/
*.pyc
ex_domain.py
Dockerfile
Dockerfile.release
EOF

  docker build --no-cache -t projectdc/${image_name}:${release_name} -f Dockerfile.release .
}

case $1 in
    encode)
        encode_release
        clean_tmp
    ;;
    *)
    release
    clean_tmp
    ;;
esac
