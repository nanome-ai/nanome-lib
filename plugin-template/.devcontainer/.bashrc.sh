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

nanome-source() {
  (
    cd .. && git clone https://github.com/nanome-ai/nanome-lib.git && cd nanome-lib &&\
    if [[ $1 == latest ]]; then
      git checkout $(git describe --tags `git rev-list --tags --max-count=1`)
    elif [[ $1 != "" ]]; then
      git checkout $1
    fi &&\
    (cd plugin-template && zip -9r ../nanome/plugin-template.zip .) &&\
    pip install --upgrade . &&\
    rm -rf ../nanome-lib
  )
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
  docker image rm -f $(docker image ls -aq) && dcreset
}