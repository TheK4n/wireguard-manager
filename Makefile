all: init

init:
	true

tg:
	pip3 install -r requirements.txt
	cp ./wg_manager.service /etc/systemd/system/wg_manager.service
	systemct enable wg_manager
	systemct start wg_manager
