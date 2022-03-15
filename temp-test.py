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

