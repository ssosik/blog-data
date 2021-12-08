---
title: Raspberry Pi Zero setup
description: ""
lead: ""
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
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcnA6LSZbTmBDKWBkoaZ2WKYhAuHqdtPTsjbAKrrpFxeATqqolrpCs4pxLqr2hd/CGvD1ax1HC7x5bIkhpfTu0ysZoSx03A/yLNi0quTcGikD3PCFXDY2Afmdud5DEugrOsxfgwLWSz0xqzXfkVqB42EUOLa71cDQfPt/J/fIhu6ymUttMN9t7lDIhRq9vs5DcOOEsV/FtFYOfUfrUEaOx1qtUNBKGSxKeLZKXcyfI03AK0oaI6HTV37tDAdSHdWX7uqyWCNpzk5KDeJ9m2MAf5A5UcQ4PbtJxzlzR0IG6bzUCC3RsnO4qO2aoDMcPUeb1tq07lYajDHjGLSZCBk0B .ssh/id_rsa.pizero
EOF

sudo service sshd restart
```

## Configure for BME280 temperature and humidity sensor

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

cat <<EOF > temp_test.py
cat temp_test.py
import time
import smbus2
import bme280

# BME280 settings
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

while True:

        #Get Data from Sensor
        bme280data = bme280.sample(bus, address, calibration_params)
        humidity = format(bme280data.humidity, ".1f")
        temp_f = (bme280data.temperature * 9/5) + 32

        #Send Temp and Humidity to Web Dashboard (Initial State)
        print("Temperature(F)", temp_f)
        print("Humidity(%)", humidity)

        #For Testing uncomment the 5-second sleep and console prints.
        time.sleep(5)
        print(temp_f,humidity)

        #For Final Product uncomment use longer sleep and remove prints.
        #time.sleep(60*MINUTES_BETWEEN_READS)
EOF

python3 temp_test.py
```

# Set up systemd to automatically run

https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

```
# Write the python script
cat <<EOF > environment-sensor.py
# bme280 docs https://pypi.org/project/RPi.bme280/
import bme280
import csv
import smbus2
import time

MINUTES_BETWEEN_WRITES = 10

# BME280 settings
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

start = format(time.time(), ".0f")

with open(f"/home/pi/data-{start}.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(("Timestamp", "Temperature (F)", "Humidity %", "Pressure (hPa)"))

    while True:

            # Get Data from Sensor
            bme280data = bme280.sample(bus, address, calibration_params)
            humidity = format(bme280data.humidity, ".1f")
            temp_f = format((bme280data.temperature * 9/5) + 32, ".1f")
            pressure = format(bme280data.pressure, ".1f")

            # Emit row to CSV
            writer.writerow((bme280data.timestamp, temp_f, humidity, pressure))
            csvfile.flush()

            time.sleep(60*MINUTES_BETWEEN_WRITES)
EOF

# Write the systemd service
cat <<EOF > environment-monitor.service
[Unit]
Description=Capture Temperature, Humidity, and Pressure every 10 minutes
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 ./environment-sensor.py

[Install]
WantedBy=multi-user.target
EOF

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

```python
# sudo pip3 install --upgrade pytz RPi.bme280 google-api-python-client google-auth-httplib2 google-auth-oauthlib
#

from __future__ import print_function
import bme280
import csv
import smbus2
import time
import os.path
from pytz import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXXXX'
SHEET_RANGE = 'Environment Readings Upload!A1'

# BME280 settings
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

csv_outfile = f"/home/pi/data.csv"
tz = timezone('US/Eastern')

creds = None

try:
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

except Exception as e:
    print(f"Login error {e}")
    sys.stdout.flush()
    service = None


print("Reading values from environment sensor")
sys.stdout.flush()

# Get Data from Sensor
bme280data = bme280.sample(bus, address, calibration_params)
humidity = format(bme280data.humidity, ".1f")
temp_f = format((bme280data.temperature * 9/5) + 32, ".1f")
pressure = format(bme280data.pressure, ".1f")
now = bme280data.timestamp
local_time = tz.localize(now)

row = (local_time.strftime('%m/%d/%Y %I:%M:%S%p'), temp_f, humidity, pressure)
body = { 'values': [row] }

try:
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()

    updates = result.get('updates')
    if updates is not None and updates.get('updatedRows') == 1:
        # The good case, we updated a row, continue
        print("updated 1 Row")
        sys.stdout.flush()

    else:
        raise Exception(f"update not expected {result}")

except Exception as e:
    # If we fall through here, the google update didn't succeed so write the CSV
    # Emit row to CSV
    print(f"Publish error {e}, defaulting to writing CSV to disk")
    sys.stdout.flush()

    with open(csv_outfile, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)
```

## Reupload rows that failed to publish

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import argparse
import csv
import os
import pdb
import sys

parser = argparse.ArgumentParser(description="Retry uploading failed CSV entries")
parser.add_argument("--file", "-f", help="Specify the file to source CSV rows from", required=True)
args = parser.parse_args()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXXXX'
SHEET_RANGE = 'Environment Readings Upload!A1'

creds = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)

with open(args.file, "r") as f:
    lines = f.readlines()

with open(args.file, "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for line in lines:
        row = line.strip().split(',')

        print(f"Publish row {row}")
        sys.stdout.flush()

        body = { 'values': [row] }

        try:
            result = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=SHEET_RANGE,
                valueInputOption="USER_ENTERED",
                body=body,
            ).execute()

            updates = result.get('updates')
            if updates is not None and updates.get('updatedRows') == 1:
                # The good case, we updated a row, continue
                print("updated 1 Row")
                sys.stdout.flush()

            else:
                raise Exception(f"update not expected {result}")

        except Exception as e:
            # If we fall through here, the google update didn't succeed so write the CSV
            # Emit row to CSV
            print(f"Publish error {e}, keeping row on disk")
            sys.stdout.flush()
            writer.writerow(row)
```
