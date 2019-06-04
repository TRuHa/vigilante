# vigilante

Monitors to network and prevents intruders with Python and your Rasbperry Pi

In this new version it incorporates some variations and maintaining the essence of the original.

  > · Receive notification when a known device is connected or disconnected.
  
  > · Receive notification when an intruder connects.


#### Install

Installation procedure.

``` bash
git clone https://github.com/TRuHa/vigilante.git
cd vigilante
./install_vigilante.sh
```

#### Update

Update procedure for futures.

``` bash
git clone https://github.com/TRuHa/vigilante.git
cd vigilante
./update_vigilante.sh
```

#### Config

Edit the configuration file and enter the **TOKEN** and **Chanel_ID** of telegram.

Add the known devices in your network with IP, important for a greater presicion must be configured with static IP.
Add the MAC address of the same and you want to be notified or not (**YES** / **NO**). The Host option is simply to add a number in the messages and is easily recognizable.

```bash
sudo nano /bin/vigilante/config.json
```
```json
{"config": {
  "token": "Put your TOKEN",
  "channel_id": "Put your Channel ID"
},
  "network": {
  "192.168.1.1": {"mac": "00:11:22:33:44:55", "state": "down", "last_view": 0, "notify": "YES", "host": "Router"},
  "192.168.1.10": {"mac": "00:11:22:33:44:55", "state": "down", "last_view": 0, "notify": "YES", "host": "Desktop"},
  "192.168.1.20": {"mac": "00:11:22:33:44:55", "state": "down", "last_view": 0, "notify": "YES", "host": "SmartPhone"},
}
```

#### Futuro

- [ ] Customizable messages.
- [ ] Add the option to modify the configuration directly from the telegram for greater convenience when adding a new device. (Actually working on it)
