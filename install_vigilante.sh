#!/bin/bash
if (( $EUID != 0 )); then
  echo "Please run as root"
  exit
fi

echo "Instaling..."

mkdir /bin/vigilante

cp whatip.py /bin/vigilante/vigilante.py
cp config.json /bin/vigilante/config.json
cp whatip.service /lib/systemd/system/vigilante.service

chmod 644 /lib/systemd/system/vigilante.service

systemctl daemon-reload
systemctl enable vigilante.service
systemctl start vigilante.service

echo "Instalado correctamente"
