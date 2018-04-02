import sys
import subprocess
MIN_ARGS = 1
ARGUMENTS = sys.argv[1:]

# check arguments
if len(ARGUMENTS) < MIN_ARGS:
    print("Usage: python3 ap.py [interface]")
    sys.exit(1)

# ensure the network interface exists
ifconfig = None
try:
    ifconfig = subprocess.run(["ifconfig", ARGUMENTS[0]], stdout=subprocess.PIPE, check=True)
except:
    print("Error: network interface \"{0}\" does not exist.".format(ARGUMENTS[0]))
    sys.exit(1)

print(ifconfig.stdout)
print("You did it!")

