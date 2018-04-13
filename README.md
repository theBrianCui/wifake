# Wifake

Wifake is a proof-of-concept tool for cloning and spawning "evil twins" of nearby Wifi access points. Wifake can replicate a nearby access point's SSID, BSSID, and password (if known), causing nearby (unwitting) users to connect to a spoofed access point rather than a real one. From there, Wifake can serve fake DNS requests for that redirect users from legitimate websites to hacker-controlled phishing pages.

For usage instructions, run

```python3 main.py```

Demo phishing static sites are available in the `web` directory which mimic their legitimate counterparts. These static pages are used expressly for **demonstration purposes only** to show how a hacker could possibly imitate a real webpage.
