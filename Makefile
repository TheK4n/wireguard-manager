all: init

init:
	mkdir -p ~/.local/bin
	PATH=$(PATH):$(HOME)/.local/bin
	chmod +x $(PWD)/wg_manager.sh ~/.local/bin/wg-manager

tg:
	python3 -m virtualenv venv
	pip3 install -r requirements.txt
	echo "\
[Unit]\
Description=wireguard\
After=network.target\
\
[Service]\
Type=simple\
WorkingDirectory= $(PWD)\
ExecStart=$(PWD)/venv/bin/python3 $(PWD)/tg.py\
Restart=on-failure\
[Install]\
WantedBy=default.target" > /etc/systemd/system/wg_manager.service
	systemct enable wg_manager
	systemct start wg_manager
