#!/bin/bash

# sn - is (s)ocial (n)etwork

# A. Demin

# Настройка окружения: python3-venv

sudo apt install python3-pip python3-venv

SRVDIR=~/homework_srv

[ -z "$SRVDIR" ] && { exit 1; }

[ "x/" == "x$SRVDIR" ] && { exit 1; }

[ -d "$SRVDIR" ] &&
{
  rm    -fR "$SRVDIR"
  mkdir -p  "$SRVDIR"
}

python3 -m venv "$SRVDIR"

pushd "$SRVDIR"
source ./bin/activate

#pip  install  fastapi uvicorn python-jose[cryptography] python-multipart
pip  install  fastapi uvicorn asyncpg sqlalchemy pyjwt[cryptography]

deactivate

popd

tar xvzf generated_app.tar.gz -C "$SRVDIR"

exit 0
