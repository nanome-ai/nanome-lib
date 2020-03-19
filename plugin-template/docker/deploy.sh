#!/bin/bash

if [ -n "$(docker ps -aqf name={{command}})" ]; then
    echo "removing exited container"
    docker rm -f {{command}}
fi

docker run -d \
--name {{command}} \
--restart unless-stopped \
-e ARGS="$*" \
{{command}}
