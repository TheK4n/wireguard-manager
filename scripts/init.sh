#!/usr/bin/env bash

test -e env.sh && source env.sh || exit 1

psql -U postgres -c "CREATE DATABASE $PG_DATABASE;"
psql -U postgres -c "CREATE USER $PG_USER WITH ENCRYPTED PASSWORD '$PG_PASS';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $PG_DATABASE TO $PG_USER;"
psql -U postgres -c "ALTER DATABASE $PG_DATABASE OWNER TO $PG_USER;"
psql -U postgres -d $PG_DATABASE -c "ALTER ROLE \"$PG_USER\" WITH LOGIN;"
psql -U $PG_USER -d $PG_DATABASE -c "
CREATE TABLE peers(
    pid SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK(length(name) <= 70),
    addr INET NOT NULL UNIQUE CHECK(addr >= INET '10.0.0.2') CHECK(addr <= INET '10.0.0.254'),
    privatekey TEXT NOT NULL CHECK(length(privatekey) = 44),
    publickey TEXT NOT NULL CHECK(length(privatekey) = 44),
    reg DATE NOT NULL DEFAULT now()
);"

mkdir $WG_PREFIX

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
