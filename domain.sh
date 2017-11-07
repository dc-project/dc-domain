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
    init --ip <ip>        init domain resolve
    del --domain <www.google.com>        del domain resolve
    update --ip <ip> --domain <www.google.com>     update domain resolve
    """
    exit 0
elif [[ "$1" == "init" ]];then
    IP=${2:-127.0.0.1}
    exec /usr/local/bin/python /tmp/domain.py $1 --ip ${IP}
elif [[ "$1" == "update" ]];then
    exec /usr/local/bin/python /tmp/domain.py $1 --ip $2 --domain $3
elif [[ "$1" == "del" ]];then
    /usr/local/bin/python /tmp/domain.py $1 --domain $2
else
    exec /bin/bash
fi