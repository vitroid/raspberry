deploy:
	sudo install unicorn-clock.service /lib/systemd/system/
	sudo systemctl enable unicorn-clock
	sudo systemctl start unicorn-clock
restart:
	sudo systemctl restart unicorn-clock
prepare:
	pip install unicornhathd pillow