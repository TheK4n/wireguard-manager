#!/usr/bin/env bash

test -e envvars.sh && source envvars.sh || exit 1

new_priv_key=$(wg genkey)
new_pub_key=$(echo "$new_priv_key" | wg pubkey)

# write to postgres database
arr=($(psql -U postgres -d wg --csv -c "INSERT INTO peers(name, addr, privatekey, publickey) VALUES('$1', (SELECT max(addr) + 1 FROM peers), '$new_private_key', '$new_pub_key')RETURNING addr, privatekey, publickey;" | head -n 2 |  tail -n +2 | tr ',' ' '))

new_ip=arr[1]

echo -e "\n# $1\n[Peer]\nPublicKey = $new_pub_key\nAllowedIPs = $new_ip/32" >> $WG_CONF

systemctl restart wg-quick@$WG_ID

echo "[Interface]"
echo "PrivateKey = $new_priv_key"
echo "Address = $new_ip/32"
echo -e "DNS = 8.8.8.8\n"
echo "[Peer]"
echo "PublicKey = $(cat $PUB_KEY_FILE)"
echo "Endpoint = $(curl ipinfo.io/ip 2>/dev/null):$WG_PORT"
echo "AllowedIPs = 0.0.0.0/0"
echo "PersistentKeepalive = 20"
