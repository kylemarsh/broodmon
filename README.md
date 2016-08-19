# Broodmon -- the Brood Monitor

Broodmon is a system that runs on a raspberry pi using a pair of DS18b20
digital temperature sensors and a webcam to monitor a chicken brooder. It
uses the rPi's GPIO to read the sensors and stores the readings into a
round-robin database that keeps track of running averages.

It can produce graphs from the rrdb tool and upload those to an
S3-compatible object store using boto. Finally there is a little bit of
network monitoring done because the original broodmate had a very tenuous
network connection.

## TODO: describe components
## TODO: describe configuration
