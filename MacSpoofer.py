import random
import os
import subprocess 
import time
import argparse
import sys

parser= argparse.ArgumentParser(description="Usage")
parser.add_argument("-t",dest="time",help="The time between each Mac change in seconds",default=100)
# Get interface name 
parser.add_argument("-I",dest="interface",help="the connection interface",default="eth0")
# is cron 
parser.add_argument("-C",dest="cron",help="if started from corn job",default=0)
parsed_args= parser.parse_args()

def get_rand():
    return random.choice("0123456789abcdef") 

def new_mac():
    new_ = "" 
    for i in range(0,5):
        new_ += get_rand() + get_rand() + ":"  
    new_ += get_rand() + get_rand() 
    return new_

# get current mac address
def get_current_mac():
    return subprocess.check_output("ip addr show {:s} | grep ether  |sed -e 's/^[ \t]*//' |cut -d ' ' -f 2".format(parsed_args.interface),shell=True)

currentMacAdd = get_current_mac()

# check if interface exist
if not currentMacAdd:
    print "Interface not found"
    sys.exit()

print "Current Mac Address :", currentMacAdd

rotate = 1;
while rotate:
    get_current_mac()
    subprocess.call(["sudo", "ip","link","set",parsed_args.interface,"down"]) 
    # stop network manager
    subprocess.call(["sudo", "service","network-manager","stop"]) 
    err = os.system("sudo ip link set dev {:s} address {:s} 2> /dev/null".format(parsed_args.interface, new_mac()))
    if err == 256:
        continue
    subprocess.call(["sudo", "ip","link","set",parsed_args.interface,"up"]) 
    # restart network interface on debian based kernel 
    subprocess.call(["sudo", "service","network-manager","restart"]) 

    print "New Mac Address :", get_current_mac()
    rotate -= int(parsed_args.cron)
    if not rotate: sys.exit()
    time.sleep(float(parsed_args.time))


