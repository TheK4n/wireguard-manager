#!/usr/bin/env bash

WG_ID=wg0
WG_PREFIX=/etc/wireguard
WG_CONF=$WG_PREFIX/$WG_ID.conf
WG_PARAMS=$WG_PREFIX/params
WG_PEERS=$WG_PREFIX/peers
WG_SUBNET=10.0.0.
WG_ADDR="$WG_SUBNET"1
CLIENT_DNSs=208.67.222.222,208.67.220.220


bye() {
    echo "$0: error: $1"
    exit 1
}

is_root() {
    if [ "${EUID}" -ne 0 ]; then
        bye "You need to run this script as root"
    fi
}

is_exists() {
    which $1 >/dev/null || bye "'$1' not found"
}

check_requirements() {
    is_exists "psql"
    is_exists "wg"
}

check_all() {
    is_root
    check_requirements
}

write_params() {
    source .env || bye "'.env' not found"

    echo "WG_PORT=$WG_PORT" > "$WG_PARAMS"
    echo "SERVER_PRIVATE_KEY=$SERVER_PRIVATE_KEY" >> "$WG_PARAMS"
    echo "SERVER_PUBLIC_KEY=$SERVER_PRIVATE_KEY" >> "$WG_PARAMS"
}

generate_server_keys() {
    SERVER_PRIVATE_KEY=$(wg genkey)
    SERVER_PUBLIC_KEY=$(echo "$SERVER_PRIVATE_KEY" | wg pubkey)
}

create_config_file() {
    echo "[Interface]" > $WG_CONF
    echo "PrivateKey = $SERVER_PRIVATE_KEY" >> $WG_CONF
    echo "Address = $WG_ADDR/24" >> $WG_CONF
    echo "ListenPort = $WG_PORT" >> $WG_CONF
    echo "PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE" >> $WG_CONF
    echo "PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE" >> $WG_CONF
}

enable_service() {
    systemctl enable wg-quick@$WG_ID.service
    systemctl start wg-quick@$WG_ID.service
    systemctl status wg-quick@$WG_ID.service
}

restart_service() {
    systemctl restart wg-quick@$WG_ID || bye "Check 'systemctl status wg-quick@$WG_ID.service'"
}

enable_ip_forwarwing() {
    test -z "$(grep "net.ipv4.ip_forward=1" /etc/sysctl.conf)" && \
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && sysctl -p
}

get_global_ipv4() {
    ip -4 addr | sed -ne 's|^.* inet \([^/]*\)/.* scope global.*$|\1|p' | awk '{print $1}' | head -1
}

add_client() {
    client_private_key=$(wg genkey)
    client_public_key=$(echo "$client_private_key" | wg genkey)
    oldest_client_ip=$(grep -A 2 '\[Peer\]' $WG_CONF | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | awk -F '.' '{printf $4"\n"}' | sort -nr | head -n 1)

    test $oldest_client_ip -gt 253 && bye "Only 253 peers" # 24 subnet
    test -z "$oldest_client_ip" && client_ip=$WG_SUBNET"2" || client_ip=$WG_SUBNET$(("$oldest_client_ip" + 1))
    echo -e "\n### $1\n[Peer]\nPublicKey = $client_public_key\nAllowedIPs = $client_ip/32" >> $WG_CONF
    restart_service

    echo "[Interface]
PrivateKey = $client_private_key
Address = $client_ip/32
DNS = $CLIENT_DNSs

[Peer]
PublicKey = $SERVER_PUBLIC_KEY
Endpoint = $(get_global_ipv4):$WG_PORT
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20" | tee $WG_PEERS/"$1".conf
}

get_client() {
    cat $WG_PEERS/"$1".conf
}

get_client_qrcode_png() {
    qrencode -l L -r $WG_PEERS/"$1".conf
}

show_client_qrcode() {
    qrencode -t ansiutf8 -l L -r $WG_PEERS/"$1".conf
}

cmd_add_client() {
    add_client "$1" >/dev/null
    show_client_qrcode "$1"
}

cmd_init() {
    mkdir -p $WG_PEERS
    chmod 600 -R $WG_PREFIX
    generate_server_keys
    write_params
    create_config_file
    enable_ip_forwarwing
    enable_service
    add_client "Initial" >/dev/null
}

source $WG_PARAMS
case "$1" in
    init) shift;               cmd_init    "$@" ;;
    add) shift;                cmd_add_client  "$@" ;;
    get) shift;                show_client_qrcode  "$@" ;;
    get_client_qrcode) shift;  get_client_qrcode_png "$@" ;;
    get_client_config) shift;  get_client "$@" ;;
    *)                         bye "Need command" ;;
esac
exit 0
