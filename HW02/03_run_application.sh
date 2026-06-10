#!/bin/bash

# sn - is (s)ocial (n)etwork

PORT_APP=8090

SRVDIR=~/homework_srv

[ -z "$SRVDIR" ] && { exit 1; }

pushd "$SRVDIR"
source ./bin/activate

cd ./generated_app/src

uvicorn openapi_server.main:app --host 0.0.0.0 --port $PORT_APP --reload

deactivate

popd

exit 0
