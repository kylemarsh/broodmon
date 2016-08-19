rrdtool create broodtemp.rrd --step 60 \
DS:broodtemp:GAUGE:120:40:120 \
DS:ambienttemp:GAUGE:120:40:120 \
RRA:AVERAGE:0.5:1:60 \
RRA:AVERAGE:0.5:1:1440 \
RRA:AVERAGE:0.5:60:168 \
RRA:AVERAGE:0.5:60:720 \
