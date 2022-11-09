#!/bin/bash

contains()
  # echo contains check $1 in $2
  case "$1" in
    (*"$2"*) true;;
    (*) false;;
  esac

echo "\nAPI Logic Project Runner 1.0 Here ($# arg(s): $1)"
if [ $# -eq 1 ]
  then
    if contains "help" $1; then
      echo "\nRuns API Logic Project"
      echo "  sh run.sh [ calling | $ | help ]"
      echo "    no args - use project venv"
      echo "    calling - use venv from calling script (for internal tests)"
      echo "    $ - use the current venv\n"
      exit 0
    elif [ "$1" == "$" ]; then
      echo ".. Using existing venv -- $VIRTUAL_ENV"
    else
      echo ".. Calling directory - venv from $PWD"
      cd $PWD
      . venv/bin/activate
    fi
  else
    echo " "
    if [ "${APILOGICSERVER_RUNNING}" = "DOCKER" ]; then
      echo ".. Docker - no venv required"
    else
      echo ".. APILOGICSERVER_RUNNING=${APILOGICSERVER_RUNNING} - not Docker/Codespaces - activate venv"
      . venv/bin/activate
    fi
  fi

cd "$(dirname "$0")"
python3 api_logic_server_run.py
