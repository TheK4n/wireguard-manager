#!/usr/bin/env bash

test -e env.sh && source env.sh || exit 1
test -z "$1" && exit 1

new_priv_key=$(wg genkey)
new_pub_key=$(echo "$new_priv_key" | wg pubkey)

# write to postgres database and return addr, privatekey, publickey as shell array
arr=($(psql -U $PG_USER -d $PG_DATABASE --csv -c "INSERT INTO peers(name, addr, privatekey, publickey) VALUES('$1', (SELECT max(addr) + 1 FROM peers), '$new_priv_key', '$new_pub_key')RETURNING addr, privatekey, publickey;" | head -n 2 |  tail -n +2 | tr ',' ' '))

new_ip=${arr[0]}
test -z $new_ip && exit 1

echo -e "\n# $1\n[Peer]\nPublicKey = $new_pub_key\nAllowedIPs = $new_ip/32" >> $WG_CONF

systemctl restart wg-quick@$WG_ID || exit 1

echo "[Interface]"
echo "PrivateKey = $new_priv_key"
echo "Address = $new_ip/32"
echo -e "DNS = 8.8.8.8\n"
echo "[Peer]"
echo "PublicKey = $(cat $PUB_KEY_FILE)"
echo "Endpoint = $(curl ipinfo.io/ip 2>/dev/null):$WG_PORT"
echo "AllowedIPs = 0.0.0.0/0"
echo "PersistentKeepalive = 20"
