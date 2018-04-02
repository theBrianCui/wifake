import sys
import subprocess
from utils import print_stdout
MIN_ARGS = 1
ARGUMENTS = sys.argv[1:]

# check arguments
if len(ARGUMENTS) < MIN_ARGS:
    print("Usage: python3 ap.py [interface]")
    sys.exit(1)

# ensure the network interface exists
iwconfig = None
try:
    iwconfig = subprocess.run(["iwconfig", ARGUMENTS[0]], stdout=subprocess.PIPE, check=True)
except:
    print("Error: network interface \"{0}\" does not exist or is not wireless.".format(ARGUMENTS[0]))
    sys.exit(1)

print_stdout(iwconfig)
print("You did it!")

