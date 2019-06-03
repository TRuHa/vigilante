#!/bin/bash
if (( $EUID != 0 )); then
  echo "Please run as root"
  exit
fi

echo "Updating..."

systemctl stop vigilante.service

cp vigilante.py /bin/vigilante/vigilante.py
cp config.json /bin/vigilante/config.json

systemctl daemon-reload
systemctl enable vigilante.service
systemctl start vigilante.service

echo "Actualizado correctamente."
