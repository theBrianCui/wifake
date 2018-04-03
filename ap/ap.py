import sys
import subprocess
from utils import exec_sync, print_stdout

MIN_ARGS = 1
ARGUMENTS = sys.argv[1:]

# check arguments
if len(ARGUMENTS) < MIN_ARGS:
    print("Usage: python3 ap.py interface")
    sys.exit(1)

INTERFACE = ARGUMENTS[0]

# ensure the network interface exists, and is wireless
exec_sync(["iwconfig", INTERFACE],
          "Checking interface {0}... ".format(INTERFACE),
          "Error: network interface \"{0}\" does not exist or is not wireless.".format(INTERFACE),
          "Done.")

# airmon-ng check kill
exec_sync(["airmon-ng", "check", "kill"],
          "Executing `airmon-ng check kill`... ",
          "Error: failed to kill conflicting processes.",
          "Done.")

# establish local gateway at 10.0.0.1/24
exec_sync(["ifconfig", INTERFACE, "10.0.0.1/24", "up"],
          "Establishing local gateway for {0} at 10.0.0.1/24... ".format(INTERFACE),
          "Error: failed to assign local gateway.",
          "Done.")

# print_stdout(iwconfig)
print("You did it!")

