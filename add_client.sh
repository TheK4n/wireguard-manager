#!/usr/bin/env bash


WG_ID=wg0
WG_CONF=/etc/wireguard/$WG_ID.conf
SERVER_PUB_KEY_FILE=/etc/wireguard/publickey
WG_PORT=51830

new_priv_key=$(wg genkey)
new_pub_key=$(echo "$new_priv_key" | wg pubkey)

old_peer=$(grep -A 2 '\[Peer\]' $WG_CONF | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | tr '.' ' ' | awk '{printf $4"\n"}' | sort -nr | head -n 1)

test old_peer -gt 253 && exit 1  # 24 subnet

test -z "$old_peer" && new_ip=10.0.0.2 || new_ip=10.0.0.$(("$old_peer" + 1))

echo -e "\n# $1\n[Peer]\nPublicKey = $new_pub_key\nAllowedIPs = $new_ip/32" >> $WG_CONF

systemctl restart wg-quick@$WG_ID

echo "[Interface]"
echo "PrivateKey = $new_priv_key"
echo "Address = $new_ip/32"
echo -e "DNS = 8.8.8.8\n"
echo "[Peer]"
echo "PublicKey = $(cat $SERVER_PUB_KEY_FILE)"
echo "Endpoint = $(curl ipinfo.io/ip 2>/dev/null):$WG_PORT"
echo "AllowedIPs = 0.0.0.0/0"
echo "PersistentKeepalive = 20"
