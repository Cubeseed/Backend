#!/bin/sh

set -o allexport
. docker/.env
set +o allexport

exec $@

