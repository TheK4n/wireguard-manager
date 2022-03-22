all: init

init:
	mkdir -p $(HOME)/.local/bin
	chmod +x $(PWD)/wg_manager.sh
	ln -s $(PWD)/wg_manager.sh $(HOME)/.local/bin/wg-manager

tg:
	python3 -m virtualenv venv
	$(PWD)/venv/bin/pip install -r requirements.txt
	echo "WG_MANAGER_PATH=$(PWD)/wg-manager.sh" >> .env
	echo "\
[Unit]\n\
Description=wireguard\n\
After=network.target\n\
\n\
[Service]\n\
Type=simple\n\
WorkingDirectory= $(PWD)\n\
ExecStart=$(PWD)/venv/bin/python3 $(PWD)/bot/app.py\n\
Restart=on-failure\n\
[Install]\n\
WantedBy=default.target" > /etc/systemd/system/wg_manager.service
	systemctl enable wg_manager
	systemctl start wg_manager
