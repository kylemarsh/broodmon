#!/bin/sh
# Hacky little script to check if the network connection is working and
# kick the wifi interface if it's not. Hopefully this fixes some of the
# dropout issues I see sometimes.

if ! ping 192.168.1.1 -c2
then
	echo "Network down at `date`" >> /home/pi/monitoring/pingmon.log;
	ifdown wlan0
	ifup wlan0
fi

#### Notes ####
#ping 192.168.1.1 -c2 | tail -2 | head -1 >> /home/pi/monitoring/pingmon.log
#ping 192.168.1.1 -c2 || (ifdown wlan0; ifup wlan0)
#tail -1 monitoring/pingmon.log  | grep '0% packet loss' && echo foo

