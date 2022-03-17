#!/usr/bin/env bash

test -e envvars.sh && source envvars.sh || exit 1

psql -U postgres -c 'CREATE DATABASE wg;'
psql -U postgres -c "CREATE USER wg_admin WITH ENCRYPTED PASSWORD '1234';"
psql -U postgres -c 'GRANT ALL PRIVILEGES ON DATABASE wg TO wg_admin;'
psql -U postgres -c 'ALTER DATABASE wg OWNER TO wg_admin;'
psql -U postgres -d wg -c 'ALTER ROLE "wg_admin" WITH LOGIN;'
psql -U wg_admin -d wg -c "
CREATE TABLE peers(
    pid SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK(length(name) <= 70),
    addr INET NOT NULL UNIQUE CHECK(addr >= INET '10.0.0.2') CHECK(addr <= INET '10.0.0.254'),
    privatekey TEXT NOT NULL CHECK(length(privatekey) = 44),
    publickey TEXT NOT NULL CHECK(length(privatekey) = 44),
    reg DATE NOT NULL DEFAULT now()
);"

mkdir /etc/wireguard

# generate server keys
wg genkey | tee $PRIV_KEY_FILE | wg pubkey > $PUB_KEY_FILE
chmod 600 $PRIV_KEY_FILE


echo "[Interface]" > $WG_CONF
echo "PrivateKey = $(cat $PRIV_KEY_FILE)" >> $WG_CONF
echo "Address = 10.0.0.1/24" >> $WG_CONF
echo "ListenPort = $WG_PORT" >> $WG_CONF
echo "PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE" >> $WG_CONF
echo "PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE" >> $WG_CONF


# ip forwarding
test -z "$(grep "net.ipv4.ip_forward=1" /etc/sysctl.conf)" && \
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && sysctl -p

# configurate service
systemctl enable wg-quick@$WG_ID.service
systemctl start wg-quick@$WG_ID.service
systemctl status wg-quick@$WG_ID.service
