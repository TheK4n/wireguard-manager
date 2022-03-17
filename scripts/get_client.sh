#!/usr/bin/env bash

test -e envvars.sh && source envvars.sh || exit 1

arr=($(psql -U postgres -d wg --csv -c "select name, addr, privatekey from peers where name = '$1'"| head -n 2 |  tail -n +2 | tr ',' ' '))


echo "[Interface]"
echo "PrivateKey = ${arr[2]}"
echo "Address = ${arr[1]}/32"
echo -e "DNS = 8.8.8.8\n"
echo "[Peer]"
echo "PublicKey = $(cat $PUB_KEY_FILE)"
echo "Endpoint = $(curl ipinfo.io/ip 2>/dev/null):$WG_PORT"
echo "AllowedIPs = 0.0.0.0/0"
echo "PersistentKeepalive = 20"
