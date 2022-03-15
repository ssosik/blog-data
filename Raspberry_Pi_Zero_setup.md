---
title: Raspberry Pi Zero Weather station setup
description: "Use a Raspberry Pi Zero with a BME280 sensor to track temperature, humidity, and air pressure"
date: "2021-10-10T09:06:29-04:00"
lastmod: "2021-10-10T09:06:29-04:00"
categories:
- home-automation
- home-network
tags:
  - raspberrypi
  - projects
  - home-network
  - weather
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Links

- [Raspberry Pi Zero product page](https://www.raspberrypi.com/products/raspberry-pi-zero/)
- [RaspberryPi Docs](https://www.raspberrypi.com/documentation/)
- [RaspberryPi SSH Keys](https://www.raspberrypi.com/documentation/computers/remote-access.html#passwordless-ssh-access)
- [RaspberryPi freezer monitor write-up](https://medium.com/initial-state/how-to-build-a-raspberry-pi-refrigerator-freezer-monitor-f7a91075c2fd)

# Get Raspbian Lite on an SD Card

Download the imager from https://www.raspberrypi.com/software/

Insert Micro SD card and image it

Once done, eject and then remount the SD card

# Initial Image customization

The SD card should be mounted under 'boot'

## Enable SSH

```bash
# Just touch this file to enable SSH
touch /Volumes/boot/ssh
```

## Setup WIFI

```bash
# Write the boot/wpa_supplicant.conf file with network SSID and Password
SSID="Stupapotamus"
PSK="..."
cat <<EOF > /Volumes/boot/wpa_supplicant.conf
country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
 scan_ssid=1
 ssid="$SSID"
 psk="$PSK"
}
EOF
```

# Unmount SD card boot the raspberry pi from it

Assuming it booted up fine and was able to connect to the network.

Need to find the IP address it has assigned

```
ssh pi@10.10.10.119
```

Find the default password according to this page: https://tutorials-raspberrypi.com/raspberry-pi-default-login-password/

`raspberry`

# Configure the running host

```bash
cat <<EOF > sshd_config
MaxAuthTries 6
MaxSessions 10
PubkeyAuthentication yes
AuthorizedKeysFile      .ssh/authorized_keys
ChallengeResponseAuthentication no
PasswordAuthentication no
UsePAM no
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
EOF
sudo mv sshd_config /etc/ssh/sshd_config

mkdir $HOME/.ssh
cat <<EOF > $HOME/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcnA6LSZbTmBDKWBkoaZ2WKYhAuHqdtPTsjbAKrrpFxeATqqolrpCs4pxLqr2hd/CGvD1ax1HC7x5bIkhpfTu0ysZoSx03A/yLNi0quTcGikD3PCFXDY2Afmdud5DEugrOsxfgwLWSz0xqzXfkVqB42EUOLa71cDQfPt/J/fIhu6ymUttMN9t7lDIhRq9vs5DcOOEsV/FtFYOfUfrUEaOx1qtUNBKGSxKeLZKXcyfI03AK0oaI6HTV37tDAdSHdWX7uqyWCNpzk5KDeJ9m2MAf5A5UcQ4PbtJxzlzR0IG6bzUCC3RsnO4qO2aoDMcPUeb1tq07lYajDHjGLSZCBk0B
EOF

sudo service sshd restart
```

## Configure BME280 temperature/humidity sensor and dependencies

```bash
# Enable I2C in the Interfacing options
# Don't forget to set the timezone!
sudo raspi-config

# Install smbus and i2c-tools
sudo apt-get install -y python-smbus i2c-tools

# Expect `i2c_dev` and `i2c_bcmXXXX`
lsmod | grep i2c_

# Expect `77`
sudo i2cdetect -y 1

sudo apt install python3-pip

sudo pip3 install --upgrade RPi.bme280 google-api-python-client google-auth-httplib2 google-auth-oauthlib pytz
```

Test scripts:
{{< include title="temp-test.py" file="temp-test.py" lang="python" highlight={linenos=table} >}}
{{< include title="environment-sensor-basic.py" file="environment-sensor-basic.py" lang="python" highlight={linenos=table} >}}

# Set up systemd to automatically run

https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

{{< include title="environment-monitor.service" file="environment-monitor.service" lang="toml" open=true highlight={linenos=table} >}}

```bash
# Write the systemd service

sudo mv environment-monitor.service /lib/systemd/system/environment-monitor.service
sudo chmod 644 /lib/systemd/system/environment-monitor.service

# Enable the service
sudo systemctl daemon-reload
sudo systemctl enable environment-monitor.service
sudo systemctl start environment-monitor.service
```

# Automatically publish to google doc

Links:
- [Setting up API keys](https://support.google.com/googleapi/answer/6158862?hl=en)
- [GCP API Credentials Page](https://console.cloud.google.com/apis/credentials)
- [How to Create Google Sheet API key](https://docs.brainstormforce.com/create-google-sheet-api-key/)
- [Google Sheets Python API](https://developers.google.com/sheets/api/quickstart/python)
- [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
- [Enable Google Workspace API for Google Doc](https://developers.google.com/workspace/guides/create-project#enable-api)
- [Google Docs API Dashboard](https://console.cloud.google.com/apis/api/docs.googleapis.com/overview)
- [Google Sheets API Dashboard](https://console.cloud.google.com/apis/api/sheets.googleapis.com/overview)
- [OAuth Scopes](https://developers.google.com/identity/protocols/oauth2/scopes#sheets)
- [Sheets Append API](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append)

--------

## Enable the Google Sheets API

Search for 'Google Sheets API' in search box, select it, then enable it.

Credential should be associated there.

## Create API Credentials

From the GCP API Credentials page above, you'll need to create an *OAuth 2.0
Client ID*; Use the Client ID and Secret from the OAuth Secret for the API
client. Keep these values PRIVATE!!! Use the "Reset Secret" link to rotate the
secret

## Notes on trying to get google API working

Download the credentials JSON from the [Google Sheets API
Dashboard](https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials)
and save as `credentials.json`

```bash
# On Mac
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

python3 google-sheets-api-test.py
# Above will do a browser redirect
```

*Pay Attention* to the email address used for login via the browser redirect

I needed to go to the OAuth Consent Screen and Publish the App

## Publish data

Full script with publishing:
{{< include title="environment-sensor.py" file="environment-sensor.py" lang="python" open=true highlight={linenos=table} >}}

## Reupload rows that failed to publish

Occasionally as the script runs, it will fail to upload data to the Google
sheet. The script will keep a backup of data in a CSV file for upload later on.
Here is the script I use for that.

{{< include title="csv-reupload.py" file="csv-reupload.py" lang="python" open=true highlight={linenos=table} >}}
