param($wkflw_dir, $grid_dir, $knime_path, $output_dir, $preferences_dir)

$volumeID = docker ps -aqf name=nanome-knime-windows
if ($volumeID -ne "") {
    Write-Host "Removing previous container"

    docker stop -t0 nanome-knime-windows
    docker rm -f nanome-knime-windows
}


$mounts = ""
foreach ($mount in $PSBoundParameters.GetEnumerator()) {
    $mounts += "--mount type=bind,source=`"$($mount.Value)`",target=$($mount.Value) "
}

docker run -d --memory=10g --name nanome-knime-windows --restart unless-stopped $mounts -e ARGS="$args" nanome-knime-windows