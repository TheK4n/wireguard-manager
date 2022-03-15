#!/usr/bin/env bash

test -e envvars.sh && source envvars.sh || exit 1

client_name="$1"

grep -A 4 -E "^#\\s$client_name\$" /etc/wireguard/wg0.conf
