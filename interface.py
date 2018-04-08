from utils import exec_sync, print_stdout

DNSMASQ_CONF = "dnsmasq.conf"

def verify_interface(target_interface, wireless=True,
                     msg=True, silent=True, err_silent=False):
    command = "ifconfig"
    if wireless: command = "iwconfig"

    if not msg:
        exec_sync([command, target_interface], silent=silent, err_silent=err_silent)
    else:
        # ensure the network target_interface exists, and is wireless
        exec_sync([command, target_interface],
                  "Checking interface {0}... ".format(target_interface),
                  "Error: network interface \"{0}\" does not exist or is not wireless.".format(target_interface),
                  "Done.", silent=silent, err_silent=err_silent)

def down_interface(target_interface):
    exec_sync(["ifconfig", target_interface, "down"],
              "Stopping interface {0}... ".format(target_interface),
              "Error: could not down network interface {0}.".format(target_interface),
              "Done.", die=False)

def establish_gateway(target_interface):
    exec_sync(["ifconfig", target_interface, "10.0.0.1/24", "up"],
              "Establishing local gateway for {0} at 10.0.0.1/24... ".format(target_interface),
              "Error: failed to assign local gateway.",
              "Done.")

def establish_forward(forward_interface):
    # sysctl -w net.ipv4.ip_forward=1
    exec_sync(["sysctl", "-w", "net.ipv4.ip_forward=1"],
              "Enabling IPv4 network forwarding in `sysctl`... ",
              "Error: failed to enable network forwarding with `sysctl -w net.ipv4.ip_forward=1`.",
              "Done.")

    # iptables -P FORWARD ACCEPT
    exec_sync(["iptables", "-P", "FORWARD", "ACCEPT"],
              "Enabling network forwarding in `iptables`... ",
              "Error: failed to enable network forwarding with `iptables -P FORWARD ACCEPT`.",
              "Done.")

    # iptables --table nat -A POSTROUTING -o wlan0 -j MASQUERADE
    exec_sync(["iptables", "--table", "nat", "-A", "POSTROUTING", "-o", forward_interface, "-j", "MASQUERADE"],
              "Enabling routing to interface {0} in `iptables`... ".format(forward_interface),
              "Error: failed to enable routing for interface {0} with `iptables --table nat -A POSTROUTING -o {0} -j MASQUERADE`.".format(forward_interface),
              "Done.")

def stop_forward(forward_interface):
    exec_sync(["iptables", "--table", "nat", "-A", "POSTROUTING", "-o", forward_interface, "-j", "MASQUERADE"],
              "Disabling routing to interface {0} in `iptables`... ".format(forward_interface),
              "Error: failed to disable routing for interface {0} with `iptables --table nat -A POSTROUTING -o {0} -j MASQUERADE`.".format(forward_interface),
              "Done.", die=False)

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
    print("Done.")

    start_dns()
