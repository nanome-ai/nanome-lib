param ([switch] $u, [switch] $update)

if ($u -or $update) {
  $contents = Get-Date
  Out-File -FilePath .\.cachebust -InputObject $contents -Encoding ASCII
}

$cachebust = Get-Content -Path .\.cachebust
docker build -f windows.Dockerfile --build-arg CACHEBUST=$cachebust -t nanome-knime-windows:latest ..
