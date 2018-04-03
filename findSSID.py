from subprocess import Popen, call, PIPE
import subprocess
import csv
import os


#remove any previous runs
os.remove('test-01.csv')


#drop wlan into monitor mode
call(['airmon-ng','start','wlan0'])

#run airodump
test = subprocess.Popen(['airodump-ng','wlan0mon','-w','test'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out,err = test.communicate(timeout=10)

#parse output
with open('test-01.csv') as csvFile:
    csvReader = csv.reader(csvFile)
    for row in csvReader:
        if(len(row)>12):
            print(row[13])

#print(scanned_networks)
#airodump.kill()
