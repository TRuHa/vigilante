#!/usr/bin/env python3
from multiprocessing import Process, Manager
import subprocess
import requests
import json
import time
import re
import os


class Vigilante:
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(self.dir, 'config.json')
        self.manager = Manager()
        self.read()

    def read(self):
        f = open(self.filename, 'r')
        content = f.read()
        f.close()
        data = json.loads(content)
        keys = data['config']
        self.token = keys['token']
        self.channel_id = keys['channel_id']
        self.devices = data['network']

    def get_mac_address(self, ip):
        try:
            proc = subprocess.Popen(['arp', '-n', ip], stdout=subprocess.PIPE)
            out, err = proc.communicate()
            ans = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', out.decode(), re.I).group()
        except:
            ans = 'Unknown'
        return ans

    def check_host(self, ip):
        ret_code = subprocess.call(['ping', '-c1', '-W20', ip],
                                   stdout=subprocess.PIPE)
        if ret_code == 0:
            self.data[ip] = self.get_mac_address(ip)
        else:
            self.data[ip] = "down"

    def send_warning(self, message):
        url = 'https://api.telegram.org/bot{0}/sendMessage'.format(self.token)
        data = {'chat_id': self.channel_id, 'text': message}
        r = requests.post(url, data)

    def vigila(self):
        self.data = self.manager.dict()
        outsider = []
        range_ip = "Put your range IP"
        while True:
            jobs = []
            start = time.time()
            for i in range(1, 255):
                ip = '{0}.{1}'.format(range_ip, i)
                job = Process(target=self.check_host, args=(ip,))
                jobs.append(job)
                job.start()
            for job in jobs:
                job.join()

            for ip in self.data.keys():
                if self.data[ip] != 'down':
                    if ip not in self.devices:
                        if self.data[ip] not in outsider:
                            outsider.append(self.data[ip])
                            message = "{0} - Detectado intruso con IP {1} y MAC {2}".format(
                                time.strftime("%d-%m-%Y %H:%M:%S"), ip, self.data[ip])
                            print(message)
                            self.send_warning(message)

                    elif self.data[ip] == 'Unknown':
                        if self.devices[ip]["state"] != "warning":
                            self.devices[ip]["state"] = "warning"
                            message = "{0} - Dispositivo desconocido con IP {1}".format(
                                time.strftime("%d-%m-%Y %H:%M:%S"), ip, self.data[ip])
                            print(message)
                            self.send_warning(message)

                    elif self.devices[ip]['mac'] != self.data[ip]:
                        if self.devices[ip]["state"] != "outsider":
                            self.devices[ip]["state"] = "outsider"
                            message = "{0} - Detectado  intruso con IP {1} y MAC {2}".format(
                                time.strftime("%d-%m-%Y %H:%M:%S"), ip, self.data[ip])
                            print(message)
                            self.send_warning(message)

                    else:
                        if self.devices[ip]["state"] != "up":
                            self.devices[ip]["state"] = "up"
                            if self.devices[ip]["notify"] == "YES":
                                message = "{0} - Dispositivo {1} conectado.".format(
                                    time.strftime("%d-%m-%Y %H:%M:%S"), self.devices[ip]["host"])
                                print(message)
                                self.send_warning(message)

                else:
                    if ip in self.devices:
                        if self.devices[ip]["state"] == "up":
                            self.devices[ip]["state"] = "prealert"
                            self.devices[ip]["last_view"] = time.time()

                        elif self.devices[ip]["state"] == "prealert":
                            if self.devices[ip]["last_view"] < time.time() + 200:
                                self.devices[ip]["state"] = "alert"
                                if self.devices[ip]["notify"] == "YES":
                                    message = "{0} - Dispositivo {1} desconectado.".format(
                                        time.strftime("%d-%m-%Y %H:%M:%S"), self.devices[ip]["host"])
                                    print(message)
                                    self.send_warning(message)

                        elif self.devices[ip]["state"] == "alert":
                            if self.devices[ip]["last_view"] < time.time() + 500:
                                self.devices[ip]["state"] = "down"
                                if self.devices[ip]["notify"] == "YES":
                                    message = "{0} - ALERTA!! Dispositivo {1} lleva caido mas de 5min.".format(
                                        time.strftime("%d-%m-%Y %H:%M:%S"), self.devices[ip]["host"])
                                    print(message)
                                    self.send_warning(message)


if __name__ == '__main__':
    vigilante = Vigilante()
    vigilante.vigila()
