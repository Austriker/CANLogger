# Setup

To start the logger at startup under Debian 8

## Adding a service to Systemd

First copy the config file :
```sh
sudo mkdir /usr/lib/systemd/system
sudo cp /home/pi/GPSLogger/autostart/canlogger.service /usr/lib/systemd/system/canlogger.service
```

Then refresh the systemd :
```sh
sudo systemctl daemon-reload
```

Now you can start the service :
```sh
sudo systemctl start canlogger
```

You can check if it's working :
```sh
sudo systemctl status canlogger
```

Finaly you need to enable the service at startup :
```sh
sudo systemctl enable canlogger
```

