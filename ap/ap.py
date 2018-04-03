import sys
import subprocess
from utils import print_stdout

MIN_ARGS = 1
ARGUMENTS = sys.argv[1:]

# check arguments
if len(ARGUMENTS) < MIN_ARGS:
    print("Usage: python3 ap.py interface")
    sys.exit(1)

INTERFACE = ARGUMENTS[0]

# ensure the network interface exists, and is wireless
print("Checking interface {0}... ".format(INTERFACE), end="", flush=True)
iwconfig = None
try:
    iwconfig = subprocess.run(["iwconfig", INTERFACE], stdout=subprocess.PIPE, check=True)
except:
    print("Error: network interface \"{0}\" does not exist or is not wireless.".format(INTERFACE))
    sys.exit(1)
print("Done.")

# airmon-ng check kill
print("Executing `airmon-ng check kill`... ", end="", flush=True)
try:
    subprocess.run(["airmon-ng", "check", "kill"], stdout=subprocess.PIPE, check=True)
except:
    print("Error: failed to kill conflicting processes.")
    sys.exit(1)
print("Done.")

# print_stdout(iwconfig)
print("You did it!")

