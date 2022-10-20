#!/bin/bash

# ru

contains()
  # echo contains check $1 in $2
  case "$1" in
    (*"$2"*) true;;
    (*) false;;
  esac

if [ $# -eq 1 ] 
  then
    if contains "help" $1; then
      echo "\nRuns API Logic Project, using venv in:"
      echo "   - project folder (no args)"
      echo "   - calling folder (arg 1)\n"
      exit 0
    fi
    . venv/bin/activate
  else
    cd "$(dirname "$0")"
    . venv/bin/activate
  fi

cd "$(dirname "$0")"
python3 api_logic_server_run.py