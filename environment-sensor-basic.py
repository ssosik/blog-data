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

