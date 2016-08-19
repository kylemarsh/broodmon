#!/bin/bash

RRDPATH="/home/pi/broodmate"
RRDFILE=$RRDPATH/broodtemp.rrd
AMBIENTRAW="#0000FF"
AMBIENTTREND="#8888FF"

BROODRAW="#FF0000"
BROODTREND="#FF8888"

#hour
rrdtool graph $RRDPATH/graphs/hour.png --start -6h \
DEF:broodtemp=$RRDFILE:broodtemp:AVERAGE \
CDEF:broodtrend=broodtemp,1800,TREND \
DEF:ambienttemp=$RRDFILE:ambienttemp:AVERAGE \
CDEF:ambienttrend=ambienttemp,1800,TREND \
LINE2:ambienttrend$AMBIENTTREND:"30 min ambient average" \
LINE2:broodtrend$BROODTREND:"30 min brood average" \
LINE1:ambienttemp$AMBIENTRAW:"Hourly Ambient Temperature" \
LINE1:broodtemp$BROODRAW:"Hourly Brood Temperature" \

#day
rrdtool graph $RRDPATH/graphs/day.png --start -1d \
DEF:broodtemp=$RRDFILE:broodtemp:AVERAGE \
CDEF:broodtrend=broodtemp,21600,TREND \
DEF:ambienttemp=$RRDFILE:ambienttemp:AVERAGE \
CDEF:ambienttrend=ambienttemp,21600,TREND \
LINE2:ambienttrend$AMBIENTTREND:"6h ambient average" \
LINE2:broodtrend$BROODTREND:"6h brood average" \
LINE1:ambienttemp$AMBIENTRAW:"Daily Ambient Temperature" \
LINE1:broodtemp$BROODRAW:"Daily Brood Temperature" \

#week
rrdtool graph $RRDPATH/graphs/week.png --start -1w \
DEF:broodtemp=$RRDFILE:broodtemp:AVERAGE \
DEF:ambienttemp=$RRDFILE:ambienttemp:AVERAGE \
LINE1:ambienttemp$AMBIENTRAW:"Weekly Ambient Temperature" \
LINE1:broodtemp$BROODRAW:"Weekly Brood Temperature" \

#month
rrdtool graph $RRDPATH/graphs/month.png --start -1m \
DEF:broodtemp=$RRDFILE:broodtemp:AVERAGE \
DEF:ambienttemp=$RRDFILE:ambienttemp:AVERAGE \
LINE1:ambienttemp$AMBIENTRAW:"Monthly Ambient Temperature" \
LINE1:broodtemp$BROODRAW:"Monthly Brood Temperature" \

