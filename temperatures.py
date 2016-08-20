import logging
import os
import time
import subprocess

COLD_THRESHOLD = 80
HOT_THRESHOLD = 105

logging.basicConfig(level=logging.INFO)

dev_dir = '/sys/bus/w1/devices'
ambient_dev = os.path.join(dev_dir, '28-00000460db84', 'w1_slave')
brood_dev = os.path.join(dev_dir, '28-000004617cfb', 'w1_slave') # has tape

temp_log_file = '/home/pi/broodmon/temp.log'

def read_device(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    logging.debug("device contents:")
    logging.debug(lines)
    return lines

def read_fahrenheit(filename, retries=10):
    lines = read_device(filename)
    valid_read = lines[0].strip()[-3:] == 'YES'
    print "valid read is: ", valid_read
    if valid_read == 0:
        logging.warn('error reading %s' % filename)
        if retries:
            logging.warn('%d retries remaining' % retries)
            time.sleep(0.2)
            return read_fahrenheit(filename, retries-1)
        else:
            logging.warn('no more retries; read failed')
            return None

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        logging.debug('read temperature: %s (thou deg C)' % temp_string)
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        logging.debug('read temperature: %s (deg F)' % temp_f)
        return temp_f
    return None

def record_temp(brood_temp, ambient_temp):
    if brood_temp is None:
        logging.debug('no brood temp returned')
        brood_temp = 'U'
    if ambient_temp is None:
        logging.debug('no ambient temp returned')
        ambient_temp = 'U'

    rrdfile = '/home/pi/broodmon/broodtemp.rrd'
    command = ['/usr/bin/rrdtool', 'update', rrdfile, 'N:%s:%s' \
        % (brood_temp, ambient_temp)]
    logging.debug('calling rrdtool: `%s`' % command)
    result = subprocess.call(command)
    if result:
        logging.warn('rrdtool update returned %d' % result)

    with open(temp_log_file, 'a') as f:
        log_string = 'time:%s,brood:%s,ambient:%s\n' \
            % (time.strftime('%Y-%m-%d %H:%M:%S'), brood_temp, ambient_temp)
        f.write(log_string)
        logging.info(log_string)

def warn(brood_temp, ambient_temp):
    # First check the log to see if we've warned yet for this incident
    with open(temp_log_file, 'r') as f:
        import re
        lines = f.readlines()
        if lines:
            line = lines[-1]
            logging.debug('last temp log line was: "%s"' % line)
            prev_temp = re.search('brood:(\d+\.?\d*)', line).group(1)
        else:
            prev_temp = None
        logging.info('last temp read was %s' % prev_temp)
        if prev_temp is not None and (prev_temp < COLD_THRESHOLD or prev_temp > HOT_THRESHOLD):
            logging.info('already warned. not warning again')
            # We've already warned about this incident. Just sit tight.
            return;
        
    logging.info('warning about critical temperature!')
    import smtplib
    import ConfigParser
    from_addr = 'broodmate@quixoticflame.net'
    #to_addrs = ['kyle.l.marsh@gmail.com', 'elizabeth.flannery@gmail.com']
    to_addrs = ['kyle.l.marsh@gmail.com']
    
    message = """From: %s
To: %s
Subject: Brood temperature is %sF

Better check on the chicks; the brood temperatures are critical:
    Brood: %sF
    Ambient: %sF
""" % (from_addr, ', '.join(to_addrs), brood_temp, brood_temp, ambient_temp)

    c = ConfigParser.ConfigParser()
    c.read('/home/pi/.smtp-config')
    smtphost = c.get('Configuration', 'hostname')
    smtpport = c.get('Configuration', 'port')
    smtpuser = c.get('Configuration', 'user')
    smtppass = c.get('Configuration', 'pass')
    s = smtplib.SMTP(smtphost, smtpport, 'broodmon')
    s.starttls()
    s.login(smtpuser, smtppass)
    s.sendmail(from_addr, to_addrs, message)
    s.quit()

    return;


def main():
    logging.info("Reading Brood Temp")
    brood = read_fahrenheit(brood_dev)
    logging.info("  %s F" % brood)

    logging.info("Reading Ambient Temp")
    ambient = read_fahrenheit(ambient_dev)
    logging.info("  %s F" % ambient)

    if brood < COLD_THRESHOLD or brood > HOT_THRESHOLD:
        logging.critical("Brood temperature too cold! Sending warning")
        warn(brood, ambient)

    logging.info("Recording temperatures")
    record_temp(brood, ambient)

if __name__ == '__main__':
    main()

