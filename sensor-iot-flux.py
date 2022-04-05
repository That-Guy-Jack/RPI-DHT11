from tokenize import Hexnumber
import Adafruit_DHT
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

token = "<token>"
org = "<org>"
bucket = "<bucket>"
sensor = Adafruit_DHT.DHT11
sensor_gpio = "4"
measurement = "dht11"
location = "<location>"
url = "https://<endpointURL>"
humidity, celcius = Adafruit_DHT.read_retry(sensor, sensor_gpio)
current_time = time.gmtime()
timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', current_time)

print("Token:", {token})
print("Org:", {org})
print("Bucket:", {bucket})
print("Location:", {location})
print("Celcius:", {celcius})
print("Humidity:", {humidity})
print("Timestamp:", {timestamp})

with InfluxDBClient(url=url, token=token, org=org) as client:
    def main():
        while True:
            humidity, celcius = Adafruit_DHT.read_retry(sensor, sensor_gpio)
            current_time = time.gmtime()
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', current_time)
            data = {"measurement": measurement, "tags": { "location": location,}, "time": timestamp, "fields": {"temperature_c": celcius, "humidity": humidity}}
            write_api = client.write_api(write_options=ASYNCHRONOUS)
            write_api.write(bucket, org, data)
            #client.close()
            print(data)
            time.sleep(int(5))

    if __name__ == '__main__':
        main()