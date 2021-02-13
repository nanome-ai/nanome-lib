export PLUGINS=plugins.nanome.ai

plugin() {
  if [ $# -eq 0 ]; then
  args="-a $PLUGINS -p 9999 -v -debug"
  else
  args=$*
  fi
  echo python run.py -r $args
  python3 run.py -r $args
}

pip-save() {
  pip install $1 && pip freeze | grep $1 >> requirements.txt
}

function dipop() {
  docker rmi -f $(docker image ls -aq | head -n 1)
}

function dcpop() {
  docker rm -f $(docker ps -aq | head -n 1)
}

function dcreset() {
  docker rm -f $(docker ps -aq)
}

function direset() {
  docker image rm -f $(docker image ls -aq) && dkreset
}