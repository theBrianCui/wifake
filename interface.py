from utils import exec_sync, print_stdout

DNSMASQ_CONF = "dnsmasq.conf"

def verify_interface(target_interface, msg=True, silent=True, err_silent=False):
    if not msg:
        exec_sync(["iwconfig", target_interface], silent=silent, err_silent=err_silent)
    else:
        # ensure the network target_interface exists, and is wireless
        exec_sync(["iwconfig", target_interface],
                  "Checking target_interface {0}... ".format(target_interface),
                  "Error: network target_interface \"{0}\" does not exist or is not wireless.".format(target_interface),
                  "Done.", silent=silent, err_silent=err_silent)

def establish_gateway(target_interface):
    exec_sync(["ifconfig", target_interface, "10.0.0.1/24", "up"],
              "Establishing local gateway for {0} at 10.0.0.1/24... ".format(target_interface),
              "Error: failed to assign local gateway.",
              "Done.")

def get_dnsmasq_pid():
    pid = exec_sync(["pgrep", "dnsmasq"],
                    error="Warning: could not determine dnsmasq PID.",
                    silent=True,
                    die=False)

    if len(pid) > 0:
        return int(pid.decode("utf-8")[:-1])

    return -1

def start_dns():
    # stop dnsmasq if already running
    stop_dns()

    # start dnsmasq, then print its PID
    exec_sync(["dnsmasq", "-C", DNSMASQ_CONF],
              "Starting dnsmasq using configuration {0}... ".format(DNSMASQ_CONF),
              "Error: could not start dnsmasq with configuration {0}.\n".format(DNSMASQ_CONF) + "Check if dnsmasq is already running.",
              "Done.")

def stop_dns():
    dnsmasq_exists_pid = get_dnsmasq_pid()

    if dnsmasq_exists_pid > -1:
        exec_sync(["kill", str(dnsmasq_exists_pid)],
                  "Stopping dnsmasq process... ",
                  "Error: could not kill dnsmasq process with PID {0}.".format(dnsmasq_exists_pid),
                  "Done.")

def establish_dns(target_interface):
    # setup dnsmasq
    # make sure dnsmasq is installed
    exec_sync(["which", "dnsmasq"],
              error="Error: dnsmasq is not installed. Install dnsmasq with `apt-get install dnsmasq`.")

    dnsmasq_conf = "\n".join((
        "interface={0}".format(target_interface),
        "dhcp-range=10.0.0.10,10.0.0.250,12h",
        "dhcp-option=3,10.0.0.1", # gateway
        "dhcp-option=6,10.0.0.1", # DNS server (this machine)
        "server=8.8.8.8", # upstream DNS server (Google DNS)
        "log-queries",
        "log-dhcp",
        ""))

    print("Creating {0} file for {1}... ".format(DNSMASQ_CONF, target_interface),
          end="", flush=True)
    with open(DNSMASQ_CONF, "w") as dnsmasq_conf_file:
        dnsmasq_conf_file.write(dnsmasq_conf)

    start_dns()
