if [ "$(docker ps -aq -f name={{command}})" != "" ]; then
    # cleanup
    echo "removing exited container"
    docker rm -f {{command}}
fi

docker run -d \
--name {{command}} \
--restart unless-stopped \
-e ARGS="$*" \
{{command}}
