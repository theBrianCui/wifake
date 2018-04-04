from subprocess import Popen, call, PIPE
from utils import exec_sync
import subprocess
import csv
import os

#remove any previous runs
if os.path.exists('test-01.csv'):
    os.remove('test-01.csv')
if os.path.exists('test-01.cap'):
    os.remove('test-01.cap')
if os.path.exists('test-01.kismet.netxml'):
    os.remove('test-01.kismet.netxml')
if os.path.exists('test-01.kismet.csv'):
    os.remove('test-01.kismet.csv')

def scan(interface):
    # airmon-ng check kill
    exec_sync(["airmon-ng", "check", "kill"],
              "Executing `airmon-ng check kill`... ",
              "Error: failed to kill conflicting processes.",
              "Done.")
    
    exec_sync(['airmon-ng', 'start', interface],
              "Switching {0} to monitor mode... ".format(interface),
              "Error: could not switch {0} to monitor mode using `airmon-ng start {0}`".format(interface),
              "Done.")

    #run airodump
    print("Scanning for nearby access points... ", end="", flush=True)
    test = subprocess.Popen(['airodump-ng',interface + "mon",'-w','test'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    exec_sync(['airmon-ng', 'stop', interface + "mon"],
              "Stopping {0} monitor mode... ".format(interface + "mon"),
              "Error: could not stop {0} monitor mode using `airmon-ng stop {0}`".format(interface + "mon"),
              "Done.")

#print(scanned_networks)
#airodump.kill()
