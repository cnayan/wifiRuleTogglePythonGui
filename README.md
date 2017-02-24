# wifiRuleTogglePythonGui

This app interacts with your router running on OpenWRT firmware using JSON RPC.

More details about OpenWRT UCI can be found here: https://wiki.openwrt.org/doc/uci

This is a simple GUI app which I created using Python.

# What it does
This app toggles the state, on / off, of a rule that you configure on your router using the web interface.

# How to use
If you wish to use this app, then you must configure these 4 things in 'wifiRuleTogglePythonGui.py' file:
<ul>
	<li>RULE_INDEX_STRING: This is the index of the firewall (traffic) rule that you have already must have configured on your router. Example: "-2"</li>
	<li>IP_STRING: This points to the router's IP. Example: "192.168.0.1"</li>
	<li>USER_NAME = "<< Your User Name >>"</li>
	<li>USER_PASSWORD = "<< Password for that user >>"</li>
</ul>

For me, the rule was configured to "deny" any access to internet for a specified MAC address. The default state of the rule is configured to be "off". Thus this app behaves accordingly.

Hope this application helps you in understanding how to use JSON RPC to interact with UCI of OpenWRT.

# Dependencies
This script uses PyQt5, paramiko. Make sure you have installed those packages before you run the script.

# Note
I've compiled this script with Python version 3.5