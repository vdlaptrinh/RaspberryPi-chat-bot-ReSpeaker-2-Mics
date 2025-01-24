curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh | sed 's/\*rpi/*aarch64/' | bash
sudo wifi-connect
