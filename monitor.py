from subprocess import Popen, call, PIPE
from utils import exec_sync

import subprocess
import csv
import os

import interface

#remove any previous runs
if os.path.exists('test-01.csv'):
    os.remove('test-01.csv')
if os.path.exists('test-01.cap'):
    os.remove('test-01.cap')
if os.path.exists('test-01.kismet.netxml'):
    os.remove('test-01.kismet.netxml')
if os.path.exists('test-01.kismet.csv'):
    os.remove('test-01.kismet.csv')

# returns true if an target_interface is already in monitor mode, false otherwise
def check_monitor_mode(target_interface):
    try:
        interface.verify_interface(target_interface + "mon",
                                   msg=False, silent=True, err_silent=True)
        return True
    except Exception as e:
        return False

# switch an target_interface into monitor mode, if not already
def enter_monitor_mode(target_interface):
    target_interface_already_monitor = check_monitor_mode(target_interface)

    if not target_interface_already_monitor:
        exec_sync(['airmon-ng', 'start', target_interface],
                  "Switching {0} to monitor mode... ".format(target_interface),
                  "Error: could not switch {0} to monitor mode using `airmon-ng start {0}`".format(target_interface),
                  "Done.")

# exit monitor mode, if currently in monitor mode
def exit_monitor_mode(target_interface):
    target_interface_in_monitor = check_monitor_mode(target_interface)

    if target_interface_in_monitor:
        exec_sync(['airmon-ng', 'stop', target_interface + "mon"],
                  "Stopping {0} monitor mode... ".format(target_interface + "mon"),
                  "Error: could not stop {0} monitor mode using `airmon-ng stop {0}`".format(target_interface + "mon"),
                  "Done.")

def scan(target_interface):
    # airmon-ng check kill
    exec_sync(["airmon-ng", "check", "kill"],
              "Executing `airmon-ng check kill`... ",
              "Error: failed to kill conflicting processes.",
              "Done.")
    
    enter_monitor_mode(target_interface)

    #run airodump
    print("Scanning for nearby access points... ", end="", flush=True)
    test = subprocess.Popen(['airodump-ng',target_interface + "mon",'-w','test'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out,err = test.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        pass
    print("Done. Scan saved in test-01.csv.", flush=True)

    # parse output in test-01.csv
    #with open('test-01.csv') as csvFile:
    #    csvReader = csv.reader(csvFile)
    #    for row in csvReader:
    #        if (len(row) > 12):
    #            print(row[13])

    exit_monitor_mode(target_interface)

#print(scanned_networks)
#airodump.kill()
