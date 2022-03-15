#!/usr/bin/env bash

test -e envvars.sh && source envvars.sh || exit 1

cp $WG_CONF ./$(basename $WG_CONF).bak
