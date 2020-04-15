import random
import os
import subprocess 
import time
import argparse

parser= argparse.ArgumentParser(description="Usage")
parser.add_argument("-t",dest="time",help="The time between each Mac change in seconds",required=True)
parsed_args= parser.parse_args()


def get_rand():
    return random.choice("0123456789abcdef") 

def new_mac():
    new_ = "" 
    for i in range(0,5):
        new_ += get_rand() + get_rand() + ":"  
    new_ += get_rand() + get_rand() 
    return new_

print "Current Mac Address :",subprocess.check_output("ifconfig eth0 | grep ether | cut -d ' ' -f 10",shell=True)

while 1:
    subprocess.check_output("ifconfig eth0 | grep ether | cut -d ' ' -f 10",shell=True)
    subprocess.call(["sudo","ifconfig","eth0","down"]) 
    new_m = new_mac()
    err = os.system("sudo ifconfig eth0 hw ether %s 2> /dev/null" %new_m)
    if err == 256:
        continue

    subprocess.call(["sudo","ifconfig","eth0","up"])
    print "New Mac Address :", subprocess.check_output("ifconfig eth0 | grep ether | grep -oE [0-9abcdef:]{17}",shell=True)
    time.sleep(float(parsed_args.time))


