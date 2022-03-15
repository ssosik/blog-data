import csv
import json
from sense_energy import Senseable
import pdb
import pprint
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Pull stats for Pellet Stove use from Sense')
parser.add_argument('-f', '--file', default="out.csv", help="CSV file to write out")

args = parser.parse_args()

sense = Senseable()
sense.authenticate("sense@little-fluffy.cloud", "XXXXX") # Sense Username/Password

# A specific device in my home. Discover device id via the home.sense.com
# Devices page, i.e. https://home.sense.com/devices/3cb2ad4c
devId = '3cb2ad4c'


#for i in range(13,32):
for i in range(1,4):
    d = sense.api_call(f'app/history/trends?monitor_id={sense.sense_monitor_id}&device_id={devId}&scale=DAY&start=2021-11-{i}T00%3A00%3A00.000Z')

    try:
        for dev in d['consumption']['devices']:
            if dev['id'] == devId:
                print(f"total time on {dev['total_time_on']}")

                with open(args.file, "a") as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow((f"2021-11-{i}", dev['total_time_on']))
    except Exception as e:
        print(e)
        pdb.set_trace()
