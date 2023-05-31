#!/bin/bash

contains()
  # echo contains check $1 in $2
  case "$1" in
    (*"$2"*) true;;
    (*) false;;
  esac


debug() {
  echo "$1"
}

debug "\nAPI Logic Project Runner 1.0 Here ($# arg(s): $1)"
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
      debug ".. Using existing venv -- $VIRTUAL_ENV"
    else
      debug ".. Calling directory - venv from $PWD"
      cd $PWD
      . venv/bin/activate
    fi
  else
    debug " "
    if [ "${APILOGICSERVER_RUNNING}" = "DOCKER" ]; then
      debug ".. Docker - no venv required"
    else
      debug ".. APILOGICSERVER_RUNNING=${APILOGICSERVER_RUNNING} - not Docker/Codespaces - activate venv"
      . venv/bin/activate
    fi
  fi

cd "$(dirname "$0")"
PYTHONHASHSEED=0
python3 api_logic_server_run.py
