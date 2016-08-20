# Broodmon -- the Brood Monitor

Broodmon is a system that runs on a raspberry pi using a pair of DS18b20
digital temperature sensors and a webcam to monitor a chicken brooder. It
uses the rPi's GPIO to read the sensors and stores the readings into a
round-robin database that keeps track of running averages.

It can produce graphs from the rrdb tool and upload those to an
S3-compatible object store using boto. Finally there is a little bit of
network monitoring done because the original broodmate had a very tenuous
network connection.

## Components
### temperatures.py
Read from the DS18B20 sensors and log the data. If the temperatures are too
far out of nominal send an e-mail warning out telling us to check on the
brood.

### broodtemp_graph.sh
Generate hourly, daily, weekly, and monthly trend graphs from the
round-robin database.

### upload_broodmate.py
Upload graphs to S3-compatible object store.

### mkbroodtempdb.sh
Create the round robin database file

## Configuration
### Crontab

Root's crontab looks like this (sudo crontab -e):

```
# Network Monitoring
#* * * * * /home/pi/netmon.sh
* * * * * date >> /home/pi/monitoring/pingmon.log; ping 192.168.1.1 -c10 |
* tail -2 | head -1 >> /home/pi/monitoring/pingmon.log

# Temperatures
* * * * * python /home/pi/broodmon/temperatures.py
* * * * * /home/pi/broodmon/broodtemp_graph.sh
*/2 * * * * /home/pi/broodmon/upload_broodmate.py
```

### Boto
/etc/boto.cfg needs to exist with your credentials:

```
[Credentials]
aws_access_key_id = **access key**
aws_secret_access_key = **secret key**
```

## Hardware
### Temperature Sensors
This project uses two DS18B20 temperature sensors (available from adafruit).
Connect pin 1 to ground, pin 3 to the 3.3v power rail, and pin 2 to the pi's
GPIO pin #4. connect a 4.7k resistor between the DS18B20's pins 2 and 3.

Multiple sensors can share the same data pin, and only need a single pull-up
resistor.

### Webcam
