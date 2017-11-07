#!/usr/bin/env bash
set -eo pipefail

if [[ "$1" == "version" ]];then
    echo $VERSION
    exit 0
elif [[ "$1" == "help" ]];then
    echo """
Goodrain Domain DC-Tools

positional arguments:
  <subcommand>
    init        init domain resolve
    del         del domain resolve
    update      update domain resolve
    """
    exit 0
elif [[ "$1" == "init" ]];then
    echo "init domain -->ip $2"
    echo $(python /tmp/domain.py $1 --ip $2)
elif [[ "$1" == "update" ]];then
    echo $(python /tmp/domain.py $1 --ip $2 --domain $3)
elif [[ "$1" == "del" ]];then
    echo $(python /tmp/domain.py $1 --domain $2)
else
    exec /bin/bash
fi