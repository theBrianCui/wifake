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
    print("Usage: python3 main.py INTERFACE [--forward=FW_INTERFACE]")
    sys.exit(1)
    
INTERFACE = ARGUMENTS[0]
FW_INTERFACE = None
if len(ARGUMENTS) > 1:
    FW_INTERFACE = ARGUMENTS[1].split("--forward=")[-1]

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

    # Scan for nearby access points
    monitor.scan(INTERFACE)

    # Select an access point, then create a hostapd configuration
    target_id = ap.choose_access_point()
    ap.make_hostapd_conf(target_id, INTERFACE)

    # Set up local gateway and DNS
    interface.establish_gateway(INTERFACE)
    interface.establish_dns(INTERFACE)

    # Set up forwarding
    if FW_INTERFACE != None:
        interface.establish_forward(FW_INTERFACE)

    # Start hosting the access point
    #ap.clone_mac(target_id, INTERFACE)
    ap.execute_hostapd()

    # Deauth clients on target network
    # Disabled for now, may interfere with hostapd
    # ap.deauth(target_id, INTERFACE)

    # print_stdout(iwconfig)
    print("You did it!")

# Clean up after requesting exit (Ctrl+C)
except KeyboardInterrupt:
    print("")
    print("")
    print("! KeyboardInterrupt detected. Exiting...")
    interface.stop_dns()
    if FW_INTERFACE != None:
        interface.stop_forward(FW_INTERFACE)
    monitor.exit_monitor_mode(INTERFACE)
    interface.down_interface(INTERFACE)
    #ap.reset_mac(INTERFACE)
