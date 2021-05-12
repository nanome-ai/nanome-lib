#!/bin/bash

cachebust=0
while [ $# -gt 0 ]; do
  case $1 in
    -u | --update ) cachebust=1 ;;
  esac
  shift
done

if [ ! -f ".cachebust" ] || (($cachebust)); then
  date +%s > .cachebust
fi

cachebust=$(cat .cachebust)
docker build -f Dockerfile --build-arg CACHEBUST=$cachebust -t {{command}}:latest ..
