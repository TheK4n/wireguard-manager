mkdir /etc/wireguard
WG_ID=wg0
WG_CONF=/etc/wireguard/$WG_ID.conf
PRIV_KEY_FILE=/etc/wireguard/privatekey
PUB_KEY_FILE=/etc/wireguard/publickey
WG_PORT=51830

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
test -z $(grep "net.ipv4.ip_forward=1" /etc/sysctl.conf) && \
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && sysctl -p

# configurate service
systemctl enable wg-quick@$WG_ID.service
systemctl start wg-quick@$WG_ID.service
systemctl status wg-quick@$WG_ID.service
