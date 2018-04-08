from utils import exec_sync, print_stdout

DNSMASQ_CONF = "dnsmasq.conf"

def verify_interface(interface, silent=True, err_silent=False):
    if silent:
        exec_sync(["iwconfig", interface], silent=silent, err_silent=err_silent)
    else:
        # ensure the network interface exists, and is wireless
        exec_sync(["iwconfig", interface],
                  "Checking interface {0}... ".format(interface),
                  "Error: network interface \"{0}\" does not exist or is not wireless.".format(interface),
                  "Done.", silent=silent, err_silent=err_silent)

def establish_gateway(interface):
    exec_sync(["ifconfig", interface, "10.0.0.1/24", "up"],
              "Establishing local gateway for {0} at 10.0.0.1/24... ".format(interface),
              "Error: failed to assign local gateway.",
              "Done.")

def establish_dns(interface):
    # setup dnsmasq
    # make sure dnsmasq is installed
    exec_sync(["which", "dnsmasq"],
              error="Error: dnsmasq is not installed. Install dnsmasq with `apt-get install dnsmasq`.")

    dnsmasq_conf = "\n".join((
        "interface={0}".format(interface),
        "dhcp-range=10.0.0.10,10.0.0.250,12h",
        "dhcp-option=3,10.0.0.1", # gateway
        "dhcp-option=6,10.0.0.1", # DNS server (this machine)
        "server=8.8.8.8", # upstream DNS server (Google DNS)
        "log-queries",
        "log-dhcp",
        ""))

    print("Creating {0} file for {1}... ".format(DNSMASQ_CONF, interface),
          end="", flush=True)
    with open(DNSMASQ_CONF, "w") as dnsmasq_conf_file:
        dnsmasq_conf_file.write(dnsmasq_conf)
    print("Done.")

    # start dnsmasq, then print its PID
    exec_sync(["dnsmasq", "-C", DNSMASQ_CONF],
              "Starting dnsmasq using configuration {0}... ".format(DNSMASQ_CONF),
              "Error: could not start dnsmasq with configuration {0}.\n".format(DNSMASQ_CONF) + "Check if dnsmasq is already running.",
              "Done.")

    pid = exec_sync(["pgrep", "dnsmasq"],
                    error="Warning: could not determine dnsmasq PID.",
                    die=False)
    if len(pid) > 0:
        print("dnsmasq PID: {0}".format(pid.decode("utf-8")[:-1]))
