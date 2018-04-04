import subprocess
import sys
from subprocess import Popen, call, PIPE

# local imports
from utils import exec_sync, print_stdout
import interface
import monitor
import ap

MIN_ARGS = 1
ARGUMENTS = sys.argv[1:]

# check arguments
if len(ARGUMENTS) < MIN_ARGS:
    print("Usage: python3 main.py interface")
    sys.exit(1)

INTERFACE = ARGUMENTS[0]

# Ensure the interface exists and is wireless
interface.verify_interface(INTERFACE)

# Scan for nearby access points
monitor.scan(INTERFACE)

# Select an access point, then create a hostapd configuration
target_ssid = ap.choose_access_point()
ap.make_hostapd_conf(target_ssid, INTERFACE)

# Set up local gateway and DNS
interface.establish_gateway(INTERFACE)
interface.establish_dns(INTERFACE)

# print_stdout(iwconfig)
print("You did it!")


