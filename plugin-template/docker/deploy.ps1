$volumeID = docker ps -aqf name={{command}}
if ($volumeID -ne "") {
    Write-Host "Removing previous container"

    docker stop -t0 {{command}}
    docker rm -f {{command}}
}

docker run -d --memory=10g --name {{command}} --restart unless-stopped $mounts -e ARGS="$args" {{command}}