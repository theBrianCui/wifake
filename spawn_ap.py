import os


# location of SSID in the string
ssid_index = 13

# metadata for hostapd.conf
interface = "wlan0"
driver = "nl80211"
channel = 1

# list of found access points
ssid_list = []


# creates a list of the found access points
def make_ssid_list():
    with open("test-01.csv", "r") as csv_file:
        for line in csv_file:
            if "ESSID" in line:
                continue
            separated_line = line.split(",")
            if len(separated_line) >= ssid_index:
                # skip blank lines
                if len(separated_line[ssid_index]) <= 1:
                    continue
                ssid_list.append(separated_line)


# gets user choice input
def get_input(prompt, count):
    choice = 100
    while True:
        try:
            choice = int(input(prompt))
            if choice > count or choice < 1:
                raise ValueError
            break
        except ValueError:
            print()
            print("That's not a valid choice. Please try again.")
    return choice


# choose an access_point from the list of found access points
def choose_access_point():
    print ("Here are the available access points")
    line_num = 1
    for line in ssid_list:
        print("{num}) {line}".format(num = line_num, line = line[ssid_index]))
        line_num += 1
    # -1 is for 1-based indexing...
    print()
    choice = get_input("Which one would you like to mimic?\n", line_num-1)
    ap_ssid = ssid_list[choice-1][ssid_index]
    print("Using access point: {ap}\n".format(ap = ap_ssid))
    return ap_ssid


# updates hostapd.conf with the new access point
def make_hostapd_conf(ap_ssid):
    print ("Creating hostapd_conf for access point {ap}".format(ap = ap_ssid))
    # removes existing hostapd.conf
    if os.path.exists("hostapd.conf"):
        os.remove("hostapd.conf")
    with open("hostapd.conf", "w") as hostapd_conf:
        hostapd_conf.write("interface={intf_name}\n".format(intf_name = interface))
        hostapd_conf.write("driver={drvr_name}\n".format(drvr_name = driver))
        hostapd_conf.write("ssid={ssid}\n".format(ssid = ap_ssid))
        hostapd_conf.write("channel={chan}\n".format(chan = channel))


# executes hostapd to spawn the access point
def execute_hostapd():
    ## TODO implement execution of hostapd
    pass


if __name__ == "__main__":
    make_ssid_list()
    ap_ssid = choose_access_point()
    make_hostapd_conf(ap_ssid)
    execute_hostapd()
