# Deprecated Linux networking commands and their replacements

In my article detailing the command line utilities available for configuring and troubleshooting network properties on Windows and Linux, I mentioned some Linux tools that, while still
included and functional in many Linux distributions, are actually considered deprecated and therefore should be phased out in favor of more modern replacements.

Specifically, the deprecated Linux networking commands in question are: arp, ifconfig, iptunnel, iwconfig, nameif, netstat, and route. These programs (except iwconfig) are included in
the net-tools package that has been unmaintained for years. The functionality provided by several of these utilities has been reproduced and improved in the new iproute2 suite, primarily
by using its new ip command. The iproute2 software code is available from Kernel.org. Iproute2 documentation is available from the Linux Foundation and PolicyRouting.org.

+-------------------------------------------------------------------------------------------------------------------+
| Deprecated command |                                    Replacement command(s)                                    |
|--------------------+----------------------------------------------------------------------------------------------|
|arp                 |ip n (ip neighbor)                                                                            |
|--------------------+----------------------------------------------------------------------------------------------|
|ifconfig            |ip a (ip addr), ip link, ip -s (ip -stats)                                                    |
|--------------------+----------------------------------------------------------------------------------------------|
|iptunnel            |ip tunnel                                                                                     |
|--------------------+----------------------------------------------------------------------------------------------|
|iwconfig            |iw                                                                                            |
|--------------------+----------------------------------------------------------------------------------------------|
|nameif              |ip link, ifrename                                                                             |
|--------------------+----------------------------------------------------------------------------------------------|
|netstat             |ss, ip route (for netstat-r), ip -s link (for netstat -i), ip maddr (for netstat-g)           |
|--------------------+----------------------------------------------------------------------------------------------|
|route               |ip r (ip route)                                                                               |
+-------------------------------------------------------------------------------------------------------------------+

.
Now let's take a closer look at these deprecated commands and their replacements.

This article will not focus on iproute2 or the ip command in detail; instead it will simply give one-to-one mappings between the deprecated commands and their new counterparts. For
replacement commands that are listed as 'not apparent', please contact me if you know otherwise.

Jump to:

  * Arp
  * Ifconfig
  * Iptunnel
  * Iwconfig
  * Nameif
  * Netstat
  * Route
  * Discussion
  * Recommended reading

Please note that nslookup and dig are covered separately here.

## Arp

+-------------------------------------------------------------------------------------------------------------------+
|                               Deprecated arp commands                               |         Replacement         |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -a [host] or --all [host]                                                        |                             |
|.                                                                                    |ip n (or ip neighbor), or ip |
|Shows the entries of the specified hostname <-> IP address. If the [host] parameter  |n show                       |
|is not used, all entries will be displayed.                                          |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|                                                                                     |ip n del [ip_addr] (this     |
|arp -d [ip_addr] or --delete [ip_addr]                                               |"invalidates" neighbor       |
|.                                                                                    |entries)                     |
|Removes the ARP cache entry for the specified host.                                  |.                            |
|                                                                                     |ip n f [ip_addr] (or ip n    |
|                                                                                     |flush [ip_addr])             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -D or --use-device                                                               |                             |
|.                                                                                    |Not apparent                 |
|Uses the hardware address associated with the specified interface.                   |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -e                                                                               |                             |
|.                                                                                    |Not apparent                 |
|Shows the entries in default (Linux) style.                                          |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -f [filename] or --file [filename]                                               |                             |
|.                                                                                    |Not apparent                 |
|Similar to the -s option, only this time the address info is taken from the file that|                             |
|[filename] set up. If no [filename] is specified, /etc/ethers is used as default.    |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -H or --hw-type [type] or -t [type]                                              |                             |
|.                                                                                    |                             |
|When setting or reading the ARP cache, this optional parameter tells arp which class |Not apparent                 |
|of entries it should check for. The default value of this parameter is ether (i.e.   |                             |
|hardware code 0x01 for IEEE 802.3 10Mbps Ethernet).                                  |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -i [int] or --device [int]                                                       |                             |
|.                                                                                    |                             |
|Selects an interface. When dumping the ARP cache only entries matching the specified |ip n [add | chg | del | repl]|
|interface will be printed. For example, arp -i eth0 -s 10.21.31.41 A321.ABCF.321A    |dev [name]                   |
|creates a static ARP entry associating IP address 10.21.31.41 with MAC address       |                             |
|A321.ABCF.321A on eth0.                                                              |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -n or --numeric                                                                  |                             |
|.                                                                                    |Not apparent                 |
|Shows IP addresses instead of trying to determine domain names.                      |                             |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -s [ip_addr] [hw_addr] or --set [ip_addr]                                        |ip n add [ip_addr] lladdr    |
|.                                                                                    |[mac_address] dev [device]   |
|Manually creates a static ARP address mapping entry for host [ip_addr] with the      |nud [nud_state] (see example |
|hardware address set to [hw_addr].                                                   |below)                       |
|-------------------------------------------------------------------------------------+-----------------------------|
|arp -v                                                                               |                             |
|.                                                                                    |ip -s n (or ip -stats n)     |
|Uses verbose mode to provide more details.                                           |                             |
+-------------------------------------------------------------------------------------------------------------------+

.
Some ip neighbor examples are as follows:

    # ip n del 10.1.2.3 dev eth0

Invalidates the ARP cache entry for host 10.1.2.3 on device eth0.

    # ip neighbor show dev eth0

Shows the ARP cache for interface eth0.

    # ip n add 10.1.2.3 lladdr 1:2:3:4:5:6 dev eth0 nud perm

Adds a "permanent" ARP cache entry for host 10.1.2.3 device eth0. The Neighbor Unreachability Detection (nud) state can be one of the following:

  * noarp -- entry is valid. No attempts to validate this entry will be made but it can be removed when its lifetime expires.
  * permanent -- entry is valid forever and can be only be removed administratively.
  * reachable -- entry is valid until the reachability timeout expires.
  * stale -- entry is valid but suspicious.

## Ifconfig

+-------------------------------------------------------------------------------------------------------------------+
|                        Deprecated ifconfig commands                        |             Replacement              |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig                                                                    |                                      |
|.                                                                           |ip a (or ip addr)                     |
|Displays details on all network interfaces.                                 |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface]                                                        |                                      |
|.                                                                           |                                      |
|The name of the interface. This is usually a driver name followed by a unit |ip a show dev [interface]             |
|number; for example, eth0 for the first Ethernet interface. Eth0 will       |                                      |
|usually be a PC's primary network interface card (NIC).                     |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [address_family]                                                   |                                      |
|.                                                                           |ip -f [family] a                      |
|To enable the interpretation of differing naming schemes used by various    |.                                     |
|protocols, [address_family] is used for decoding and displaying all protocol|[family] can be inet (IPv4), inet6    |
|addresses. Currently supported address families include inet (TCP/IP,       |(IPv6), or link. Additionally, -4 = -f|
|default), inet6 (IPv6), ax25 (AMPR Packet Radio), ddp (Appletalk Phase 2),  |inet and -6 = -f inet6.               |
|ipx (Novell IPX) and netrom (AMPR Packet radio).                            |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] add [address/prefixlength                              |ip a add [ip_addr/mask] dev           |
|.                                                                           |[interface]                           |
|Adds an IPv6 address to the [interface].                                    |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] address [address]                                      |ip a add [ip_addr/mask] dev           |
|.                                                                           |[interface]                           |
|Assigns the specified IP [address] to the specified [interface].            |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] allmulti or -allmulti                                  |ip mr iif [name] or ip mroute iif     |
|.                                                                           |[name], where [name] is the interface |
|Enables or disables all-multicast mode. If selected, all multicast packets  |on which multicast packets are        |
|on the network will be received by the [interface] specified. This enables  |received.                             |
|or disables the sending of incoming frames to the kernel's network layer.   |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] arp or -arp                                            |                                      |
|.                                                                           |ip link set arp on or arp off         |
|Enables or disables the use of the ARP protocol on this [interface].        |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] broadcast [address]                                    |ip a add broadcast [ip_address]       |
|.                                                                           |.                                     |
|Specifies the address to use to use for broadcast transmissions. By default,|ip link set dev [interface] broadcast |
|the broadcast address for a subnet is the IP address with all ones in the   |[mac_address] (sets the link layer    |
|host portion of the subnet address (i.e., a.b.c.255 for a /24 subnet).      |broadcast address)                    |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] del [address/prefixlength]                             |ip a del [ipv6_addr or ipv4_addr] dev |
|.                                                                           |[interface]                           |
|Removes an IPv6 address from the [interface], such as eth0.                 |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] down                                                   |                                      |
|.                                                                           |ip link set dev [interface] down      |
|Disables the [interface], such as eth0.                                     |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] hw [class] [address]                                   |                                      |
|.                                                                           |                                      |
|Sets the hardware (MAC) address of this [interface], if the device driver   |ip link set dev [interface] address   |
|supports this operation. The keyword must be followed by the name of the    |[mac_addr]                            |
|hardware [class] and the printable ASCII equivalent of the hardware address.|                                      |
|Hardware classes currently supported include ether (Ethernet), ax25 (AMPR   |                                      |
|AX.25), ARCnet and netrom (AMPR NET/ROM).                                   |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] io_addr [address]                                      |                                      |
|.                                                                           |Not apparent; possibly ethtool.       |
|Sets the start [address] in I/O space for this device.                      |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] irq [address]                                          |                                      |
|.                                                                           |Not apparent; possibly ethtool.       |
|Sets the interrupt line used by the network interface.                      |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] mem_start [address]                                    |                                      |
|.                                                                           |Not apparent; possibly ethtool.       |
|Sets the start address for shared memory of the interface.                  |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] media [type]                                           |                                      |
|.                                                                           |                                      |
|Sets physical port or medium type. Examples of [type] are 10baseT, 10base2, |Not apparent; possibly ethtool.       |
|and AUI. A [type] value of auto will tell the interface driver to           |                                      |
|automatically determine the media type (driver support for this command     |                                      |
|varies).                                                                    |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] mtu [n]                                                |                                      |
|.                                                                           |ip link set dev [interface] mtu [n]   |
|Sets the Maximum Transfer Unit (MTU) of an interface to [n].                |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] multicast                                              |                                      |
|.                                                                           |ip link set dev [interface] multicast |
|Sets the multicast flag on the interface (should not normally be needed as  |on or off                             |
|the drivers set the flag correctly themselves).                             |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] netmask [mask_address]                                 |                                      |
|.                                                                           |                                      |
|Sets the subnet mask (not the IP address) for this [interface]. This value  |Not apparent                          |
|defaults to the standard Class A, B, or C subnet masks (based on the        |                                      |
|interface IP address) but can be changed with this command.                 |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|                                                                            |not apparent; possibly ipppd [device].|
|ifconfig [interface] pointopoint or -pointopoint                            |The command ip a add peer [address]   |
|.                                                                           |specifies the address of the remote   |
|Enables or disables point-to-point mode on this [interface].                |endpoint for point-to-point           |
|                                                                            |interfaces.                           |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] promisc or -promisc                                    |ip link set dev [interface] promisc on|
|.                                                                           |or off                                |
|Enables or disables promiscuous mode on the [interface].                    |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] txquelen [n]                                           |                                      |
|.                                                                           |ip link set dev [interface] txqueuelen|
|Sets the transmit queue length on the [interface]. Smaller values are       |[n] or txqlen [n]                     |
|recommended for connections with high latency (i.e., dial-up modems, ISDN,  |                                      |
|etc).                                                                       |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] tunnel [address]                                       |                                      |
|.                                                                           |ip tunnel mode sit (other possible    |
|Creates a Simple Internet Transition (IPv6-in-IPv4) device which tunnels to |modes are ipip and gre).              |
|the IPv4 [address] provided.                                                |                                      |
|----------------------------------------------------------------------------+--------------------------------------|
|ifconfig [interface] up                                                     |                                      |
|.                                                                           |ip link set [interface] up            |
|Activates (enables) the [interface] specified.                              |                                      |
+-------------------------------------------------------------------------------------------------------------------+

.
Some examples illustrating the ip command are as follows; using the table above you should be able to figure out what they do.

    # ip link show dev eth0
    # ip a add 10.11.12.13/8 dev eth0
    # ip link set dev eth0 up
    # ip link set dev eth0 mtu 1500
    # ip link set dev eth0 address 00:70:b7:d6:cd:ef

## Iptunnel

+-------------------------------------------------------------------------------------------------------------------+
|          Deprecated iptunnel commands          |                           Replacement                            |
|------------------------------------------------+------------------------------------------------------------------|
|                                                |ip tunnel a or add                                                |
|iptunnel [add | change | del | show]            |ip tunnel chg or change                                           |
|                                                |ip tunnel d or del                                                |
|                                                |ip tunnel ls or show                                              |
|------------------------------------------------+------------------------------------------------------------------|
|iptunnel add [name] [mode {ipip | gre | sit} ]  |ip tunnel add [name] [mode {ipip | gre | sit | isatap | ip6in6 |  |
|remote [remote_addr] local [local_addr]         |ipip6 | any }] remote [remote_addr] local [local_addr]            |
|------------------------------------------------+------------------------------------------------------------------|
|iptunnel -V or --version                        |not apparent                                                      |
+-------------------------------------------------------------------------------------------------------------------+

.
The syntax between iptunnel and ip tunnel is very similar as these examples show.

    # [iptunnel | ip tunnel] add ipip-tunl1 mode ipip remote 83.240.67.86 (ipip-tunl1 is the name of the tunnel, 83.240.67.86 is the IP address of the remote endpoint).
    # [iptunnel | ip tunnel] add ipi-tunl2 mode ipip remote 104.137.4.160 local 104.137.4.150 ttl 1
    # [iptunnel | ip tunnel] add gre-tunl1 mode gre remote 192.168.22.17 local 192.168.10.21 ttl 255

Iptunnel is covered in more depth here.

## Iwconfig

Iwconfig's successor, iw, is still in development. Official documentation for iw is available here and here.

+-------------------------------------------------------------------------------------------------------------------+
|                                  Deprecated iwconfig commands                                  |   Replacement    |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig                                                                                        |                  |
|.                                                                                               |                  |
|Displays basic details about wireless interfaces, such as supported protocols (802.11a/b/g/n),  |iw dev [interface]|
|Extended Service Set ID (ESSID), mode, and access point. To view these details about a          |link              |
|particular interface, use iwconfig [interface] where the interface is the device name, such as  |                  |
|wlan0.                                                                                          |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] ap [address]                                                               |                  |
|.                                                                                               |                  |
|Forces the wireless adapter to register with the access point given by the [address], if        |Not apparent      |
|possible. This address is the cell identity of the access point (as reported by wireless        |                  |
|scanning) which may be different from its MAC address.                                          |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig commit                                                                                 |                  |
|.                                                                                               |                  |
|Some wireless adapters may not apply changes immediately (they may wait to aggregate the        |Not apparent      |
|changes, or apply them only when the card is brought up via ifconfig). This command (when       |                  |
|available) forces the adapter to immediately apply all pending changes.                         |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] essid [name]                                                               |                  |
|.                                                                                               |iw [interface]    |
|Connects to the WLAN with the ESSID [name] provided. With some wireless adapters, you can       |connect [name]    |
|disable the ESSID checking (ESSID promiscuous) with off or any (and on to re-enable it).        |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] frag [num]                                                                 |                  |
|.                                                                                               |                  |
|Sets the maximum fragment size which is always lower than the maximum packet size. This         |Not apparent      |
|parameter may also control Frame Bursting available on some wireless adapters (the ability to   |                  |
|send multiple IP packets together). This mechanism would be enabled if the fragment size is     |                  |
|larger than the maximum packet size. Other valid frag parameters to auto, on, and off.          |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] [freq | channel]                                                           |iw dev [interface]|
|.                                                                                               |set freq [freq]   |
|Sets the operating frequency or channel on the wireless device. A value below 1000 indicates a  |[HT20|HT40+|HT40-]|
|channel number, a value greater than 1000 is a frequency in Hz. You can append the suffix k, M  |.                 |
|or G to the value (for example, "2.46G" for 2.46 GHz frequency). You may also use off or auto to|iw dev [interface]|
|let the adapter pick up the best channel (when supported).                                      |set channel [chan]|
|                                                                                                |[HT20|HT40+|HT40-]|
|------------------------------------------------------------------------------------------------+------------------|
|                                                                                                |iw [interface]    |
|iwconfig [interface] key [key] [mode] [on | off]                                                |connect [name]    |
|.                                                                                               |keys [key] (for   |
|To set the current encryption [key], just enter the key in hex digits as XXXX-XXXX-XXXX-XXXX or |WEP)              |
|XXXXXXXX. You can also enter the key as an ASCII string by using the s: prefix. On and off re=  |.                 |
|enable and disable encryption. The security mode may be open or restricted, and its meaning     |To connect to an  |
|depends on the card used. With most cards, in open mode no authentication is used and the card  |AP with WPA or    |
|may also accept non-encrypted sessions, whereas in restricted mode only encrypted sessions are  |WPA2 encryption,  |
|accepted and the card will use authentication if available.                                     |you must use      |
|                                                                                                |wpa_supplicant.   |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] mode [mode]                                                                |                  |
|.                                                                                               |                  |
|Sets the operating mode of the wireless device. The [mode] can be Ad-Hoc, Auto, Managed, Master,|                  |
|Monitor, Repeater, or Secondary.                                                                |                  |
|.                                                                                               |                  |
|Ad-Hoc: the network is composed of only one cell and without an access point.                   |Not apparent      |
|Managed: the wireless node connects to a network composed of many access points, with roaming.  |                  |
|Master: the wireless node is the synchronization master, or it acts as an access point.         |                  |
|Monitor: the wireless node is not associated with any cell and passively monitors all packets on|                  |
|the frequency.                                                                                  |                  |
|Repeater: the wireless node forwards packets between other wireless nodes.                      |                  |
|Secondary: the wireless node acts as a backup master/repeater.                                  |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] modu [modulation]                                                          |                  |
|.                                                                                               |                  |
|Forces the wireless adapter to use a specific set of modulations. Modern adapters support       |Not apparent      |
|various modulations, such as 802.11b or 802.11g. The list of available modulations depends on   |                  |
|the adapter/driver and can be displayed using iwlist modulation. Some options are 11g, CCK OFDMa|                  |
|, and auto.                                                                                     |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] nick [name]                                                                |                  |
|.                                                                                               |Not apparent      |
|Sets the nick name (or station name).                                                           |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] nwid [name]                                                                |                  |
|.                                                                                               |                  |
|Sets the Network ID for the WLAN. This parameter is only used for pre-802.11 hardware as the    |Not apparent      |
|802.11 protocol uses the ESSID and access point address for this function. With some wireless   |                  |
|adapters, you can disable the Network ID checking (NWID promiscuous) with off (and on to        |                  |
|re-enable it).                                                                                  |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] power [option]                                                             |                  |
|iwconfig [interface] power min | max [secondsu | secondsm]                                      |                  |
|iwconfig [interface] power mode [mode]                                                          |Not apparent; some|
|iwconfig [interface] power on | off                                                             |power commands    |
|.                                                                                               |are:              |
|Configures the power management scheme and mode. Valid [options] are: period [value] (sets the  |.                 |
|period between wake ups), timeout [value] (sets the timeout before going back to sleep), saving |iw dev [interface]|
|[value] (sets the generic level of power saving).                                               |set power_save on |
|The min and max modifiers are in seconds by default, but append the suffices m or u to specify  |.                 |
|values in milliseconds or microseconds.                                                         |iw dev [interface]|
|Valid [mode] options are: all (receive all packets), unicast (receive unicast packets only,     |get power_save    |
|discard multicast and broadcast) and multicast (receive multicast and broadcast only, discard   |                  |
|unicast packets).                                                                               |                  |
|On and off re-enable or disable power management.                                               |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] rate/bit [rate]                                                            |                  |
|.                                                                                               |                  |
|Sets the bit rate in bits per second for cards supporting multiple bit rates. The bit-rate is   |iw [interface] set|
|the speed at which bits are transmitted over the medium, the user speed of the link is lower due|bitrates          |
|to medium sharing and various overhead.Suffixes k, M or G can be added to the numeric [rate]    |legacy-2.4 12 18  |
|(decimal multiplier : 10^3, 10^6 and 10^9 b/s), or add '0' for enough. The [rate] can also be   |24                |
|auto to select automatic bit-rate mode (fallback to lower rate on noisy channels), or fixed to  |                  |
|revert back to fixed setting. If you specify a bit-rate numeric value and append auto, the      |                  |
|driver will use all bit-rates lower and equal than this value.                                  |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] retry [option] [value]                                                     |                  |
|.                                                                                               |                  |
|To set the maximum number of retries (MAC retransmissions), enter limit [value]. To set the     |Not apparent      |
|maximum length of time the MAC should retry, enter lifetime [value]. By default, this value is  |                  |
|in seconds; append the suffices m or u to specify values in milliseconds or microseconds. You   |                  |
|can also add the short, long, min and max modifiers.                                            |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] rts [threshold]                                                            |                  |
|.                                                                                               |                  |
|Sets the size of the smallest packet for which the node sends RTS; a value equal to the maximum |Not apparent      |
|packet size disables the mechanism. You may also set the threshold parameter to auto, fixed or  |                  |
|off.                                                                                            |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig [interface] sens [threshold]                                                           |                  |
|.                                                                                               |                  |
|Sets the sensitivity threshold (defines how sensitive the wireless adapter is to poor operating |Not apparent      |
|conditions such as low signal, signal interference, etc). Modern adapter designs seem to control|                  |
|these thresholds automatically.                                                                 |                  |
|------------------------------------------------------------------------------------------------+------------------|
|                                                                                                |iw dev [interface]|
|iwconfig [interface] txpower [value]                                                            |set txpower [auto |
|.                                                                                               || fixed | |limit] |
|For adapters supporting multiple transmit powers, this sets the transmit power in dBm. If W is  |[tx power in mBm] |
|the power in Watt, the power in dBm is P = 30 + 10.log(W). If the [value] is postfixed by mW, it|.                 |
|will be automatically converted to dBm. In addition, on and off enable and disable the radio,   |iw phy [phyname]  |
|and auto and fixed enable and disable power control (if those features are available).          |set txpower [auto |
|                                                                                                || fixed | limit]  |
|                                                                                                |[tx power in mBm] |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig --help                                                                                 |                  |
|.                                                                                               |iw help           |
|Displays the iwconfig help message.                                                             |                  |
|------------------------------------------------------------------------------------------------+------------------|
|iwconfig --version                                                                              |                  |
|.                                                                                               |iw --version      |
|Displays the version of iwconfig installed.                                                     |                  |
+-------------------------------------------------------------------------------------------------------------------+

.
Some examples of the iw command syntax are as follows.

    # iw dev wlan0 link
    # iw wlan0 connect CoffeeShopWLAN
    # iw wlan0 connect HomeWLAN keys 0:abcde d:1:0011223344 (for WEP)

## Nameif

+-------------------------------------------------------------------------------------------------------------------+
|                                  Deprecated nameif commands                                  |    Replacement     |
|----------------------------------------------------------------------------------------------+--------------------|
|                                                                                              |ip link set dev     |
|nameif [name] [mac_address]                                                                   |[interface] name    |
|.                                                                                             |[name]              |
|If no name and MAC address are provided, it attempts to read addresses from /etc/mactab. Each |.                   |
|line of mactab should contain an interface name and MAC address (or comments starting with #).|ifrename -i         |
|                                                                                              |[interface] -n      |
|                                                                                              |[newname]           |
|----------------------------------------------------------------------------------------------+--------------------|
|nameif -c [config_file]                                                                       |ifrename -c         |
|.                                                                                             |[config_file]       |
|Reads from [config_file] instead of /etc/mactab.                                              |                    |
|----------------------------------------------------------------------------------------------+--------------------|
|nameif -s                                                                                     |                    |
|.                                                                                             |Not apparent        |
|Error messages are sent to the syslog.                                                        |                    |
+-------------------------------------------------------------------------------------------------------------------+

## Netstat

+-------------------------------------------------------------------------------------------------------------------+
|                                   Deprecated netstat commands                                    |  Replacement   |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -a or --all                                                                               |                |
|.                                                                                                 |ss -a or --all  |
|Shows both listening and non-listening sockets.                                                   |                |
|--------------------------------------------------------------------------------------------------+----------------|
|                                                                                                  |ss -f [family]  |
|netstat -A [family] or --protocol=[family]                                                        |or --family=     |
|.                                                                                                 |[family]        |
|Specifies the address families for which connections are to be shown. [family] is a comma         |.               |
|separated list of address family keywords like inet, unix, ipx, ax25, netrom, and ddp. This has   |Families: unix, |
|the same effect as using the --inet, --unix (-x), --ipx, --ax25, --netrom, and --ddp options.     |inet, inet6,    |
|                                                                                                  |link, netlink.  |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -c or --continuous                                                                        |                |
|.                                                                                                 |Not apparent    |
|Configures netstat to refresh the displayed information every second until stopped.               |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -C                                                                                        |ip route list   |
|.                                                                                                 |cache           |
|Prints routing information from the route cache.                                                  |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -e or --extend                                                                            |ss -e or        |
|.                                                                                                 |--extended      |
|Displays an increased level of detail. Can be entered as twice (as --ee) for maximum details.     |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -F                                                                                        |                |
|.                                                                                                 |Not apparent    |
|Prints routing information from the forward information database (FIB).                           |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -g or --groups                                                                            |ip maddr, ip    |
|.                                                                                                 |maddr show      |
|Displays multicast group membership information for IPv4 and IPv6.                                |[interface]     |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -i or --interface=[name]                                                                  |                |
|.                                                                                                 |ip -s link      |
|Displays a table of all network interfaces, or the specified [name].                              |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -l or --listening                                                                         |ss -l or        |
|.                                                                                                 |--listening     |
|Shows only listening sockets (which are omitted by netstat be default).                           |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -M or --masquerade                                                                        |                |
|.                                                                                                 |Not apparent    |
|Displays a list of masqueraded connections (connections being altered by Network Address          |                |
|Translation).                                                                                     |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -n or --numeric                                                                           |                |
|.                                                                                                 |ss -n or        |
|Show numerical addresses instead of trying to determine symbolic host, port or user names (skips  |--numeric       |
|DNS translation).                                                                                 |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat --numeric-hosts                                                                           |                |
|.                                                                                                 |Not apparent    |
|Shows numerical host addresses but does not affect the resolution of port or user names.          |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat --numeric ports                                                                           |                |
|.                                                                                                 |Not apparent    |
|Shows numerical port numbers but does not affect the resolution of host or user names.            |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat --numeric-users                                                                           |                |
|.                                                                                                 |Not apparent    |
|Shows numerical user IDs but does not affect the resolution of host or port names.                |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -N or --symbolic                                                                          |                |
|.                                                                                                 |ss -r or        |
|Displays the symbolic host, port, or user names instead of numerical representations. Netstat does|--resolve       |
|this by default.                                                                                  |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -o or --timers                                                                            |ss -o or        |
|.                                                                                                 |--options       |
|Includes information related to networking timers.                                                |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -p or --program                                                                           |                |
|.                                                                                                 |ss -p           |
|Shows the process ID (PID) and name of the program to which each socket belongs.                  |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -r or --route                                                                             |ip route, ip    |
|.                                                                                                 |route show all  |
|Shows the kernel routing tables.                                                                  |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -s or --statistics                                                                        |                |
|.                                                                                                 |ss -s           |
|Displays summary statistics for each protocol.                                                    |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -t or --tcp                                                                               |                |
|.                                                                                                 |ss -t or --tcp  |
|Filters results to display TCP only.                                                              |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -T or --notrim                                                                            |                |
|.                                                                                                 |Not apparent    |
|Stops trimming long addresses.                                                                    |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -u or --udp                                                                               |                |
|.                                                                                                 |ss -u or --udp  |
|Filters results to display UDP only.                                                              |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -v or --verbose                                                                           |                |
|.                                                                                                 |Not apparent    |
|Produces verbose output.                                                                          |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -w or --raw                                                                               |                |
|.                                                                                                 |ss-w or --raw   |
|Filter results to display raw sockets only.                                                       |                |
|--------------------------------------------------------------------------------------------------+----------------|
|netstat -Z or --context                                                                           |                |
|.                                                                                                 |                |
|Prints the SELinux context if SELinux is enabled. On hosts running SELinux, all processes and     |Not apparent    |
|files are labeled in a way that represents security-relevant information. This information is     |                |
|called the SELinux context.                                                                       |                |
+-------------------------------------------------------------------------------------------------------------------+

## Route

+-------------------------------------------------------------------------------------------------------------------+
|                     Deprecated route commands                      |                 Replacement                  |
|--------------------------------------------------------------------+----------------------------------------------|
|route                                                               |                                              |
|.                                                                   |ip route                                      |
|Displays the host's routing tables.                                 |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -A [family] [add] or route --[family] [add]                   |ip -f [family] route                          |
|.                                                                   |.                                             |
|Uses the specified address family with add or del. Valid families   |[family] can be inet (IP), inet6 (IPv6), or   |
|are inet (DARPA Internet), inet6 (IPv6), ax25 (AMPR AX.25), netrom  |link. Additionally, -4 = -f inet and -6 = -f  |
|(AMPR NET/ROM), ipx (Novell IPX), ddp (Appletalk DDP), and x25      |inet6.                                        |
|(CCITT X.25).                                                       |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -C or --cache                                                 |                                              |
|.                                                                   |Not apparent; ip route show cache dumps the   |
|Operates on the kernel's routing cache instead of the forwarding    |routing cache.                                |
|information base (FIB) routing table.                               |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -e or -ee                                                     |                                              |
|.                                                                   |                                              |
|Uses the netstat-r format to display the routing table. -ee will    |ip route show                                 |
|generate a very long line with all parameters from the routing      |                                              |
|table.                                                              |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -F or --fib                                                   |                                              |
|.                                                                   |Not apparent                                  |
|Operates on the kernel's Forwarding Information Base (FIB) routing  |                                              |
|table (default behavior).                                           |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -h or --help                                                  |                                              |
|.                                                                   |ip route help                                 |
|Prints the help message.                                            |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -n                                                            |                                              |
|.                                                                   |Not apparent                                  |
|Shows numerical IP addresses and bypass host name resolution.       |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -v or --verbose                                               |                                              |
|.                                                                   |ip -s route                                   |
|Enables verbose command output.                                     |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route -V or --version                                               |                                              |
|.                                                                   |ip -V                                         |
|Dispays the version of net-tools and the route command.             |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route add or del                                                    |ip route [add | chg | repl | del] [ip_addr]   |
|.                                                                   |via [ip_addr]                                 |
|Adds or delete a route in the routing table.                        |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] dev [interface]                                  |                                              |
|.                                                                   |ip route [add | chg | repl | del] dev         |
|Associates a route with a specific device. If dev [interface] is the|[interface]                                   |
|last option on the command line, the word dev may be omitted.       |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] [default] gw [gw]                                |                                              |
|.                                                                   |ip route add default via [gw]                 |
|Routes packets through the specified gateway IP address.            |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] -host                                            |                                              |
|.                                                                   |Not apparent                                  |
|Specifies that the target is a host (not a network).                |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] -irtt [n]                                        |                                              |
|.                                                                   |Not apparent; ip route [add | chg | repl |    |
|Sets the initial round trip time (IRTT) for TCP connections over    |del] rtt [number] sets the RTT estimate;      |
|this route to [n] milliseconds (1-12000). This is typically only    |rttvar [number] sets the initial RTT variance |
|used on AX.25 networks. If omitted the RFC 1122 default of 300ms is |estimate.                                     |
|used.                                                               |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] -net                                             |                                              |
|.                                                                   |Not apparent                                  |
|Specifies that the target is a network (not a host).                |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] [-host or -net] netmask [mask]                   |                                              |
|.                                                                   |Not apparent                                  |
|Sets the subnet [mask].                                             |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] metric [n]                                       |                                              |
|.                                                                   |ip route [add | chg | repl | del] metric      |
|Sets the metric field in the routing table (used by routing daemons)|[number] or preference [number]               |
|to the value of [n].                                                |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] mod, dyn, or reinstate                           |                                              |
|.                                                                   |Not apparent                                  |
|Install a dynamic or modified route. These flags are for diagnostic |                                              |
|purposes, and are generally only set by routing daemons.            |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] mss [bytes]                                      |ip route [add | chg | repl | del] advmss      |
|.                                                                   |[number] (the MSS to advertise to these       |
|Sets the TCP Maximum Segment Size (MSS) for connections over this   |destinations when establishing TCP            |
|route to the number of [bytes] specified.                           |connections).                                 |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] reject                                           |                                              |
|.                                                                   |                                              |
|Installs a blocking route, which will force a route lookup to fail. |ip route add prohibit [network_addr]          |
|This is used to mask out networks before using the default route.   |                                              |
|This is not intended to provide firewall functionality.             |                                              |
|--------------------------------------------------------------------+----------------------------------------------|
|route [add or del] window [n]                                       |                                              |
|.                                                                   |                                              |
|Set the TCP window size for connections over this route to the value|ip route [add | chg | repl | del] window [W]  |
|of [n] bytes. This is typically only used on AX.25 networks and with|                                              |
|drivers unable to handle back-to-back frames.                       |                                              |
+-------------------------------------------------------------------------------------------------------------------+

Some examples of ip route command syntax are as follows.

    # ip route add 10.23.30.0/24 via 192.168.8.50
    # ip route del 10.28.0.0/16 via 192.168.10.50 dev eth0
    # ip route chg default via 192.168.25.110 dev eth1

    (shows the interface and gateway that would be used to reach a remote host. This command would be especially useful for troubleshooting routing issues on
    hosts with large routing tables and/or with multiple network interfaces).
    # ip route get [ip_address]
    # ip route show cache
    # ip route flush cache


# Quick Start

## ip tools

    # ip link show
    # ip link set dev eth0 up
    # ip addr show dev lan
    # ip addr flush dev lan                     #清空网卡的所有ip地址
    # ip addr add 192.168.2.77/24 dev lan       #添加ip
    # ip neigh show                             #显示ip与mac对应关系
    # ip neigh flush dev lan
    # ip route
    # ip route add 192.168.2.0/24 via 192.168.1.1 dev1234
    # ip route change default via 10.10.10.30 dev wan
    # traceroute www.google.com

## ss

    $ ss -t4 state established           <<<< To display all Ipv4 tcp sockets that are in "connected" state.

    ### Since sockets remain in such states syn-sent, syn-recv for a very short time.
    ###   It would be ideal to use the watch command to detect such socket states in real time.
    $ watch -n 1 "ss -t4 state syn-sent"

    $ ss -at '( dport = :ssh or sport = :ssh )'    <<< Display all socket connections with source or destination port of ssh.
    $ ss -nt '( dst :443 or dst :80 )'   <<< Option -n donnot resolve hostname|domain-name
    <OR> $ ss -nt dst :443 or dst :80    <<< Sockets with destination port 443 or 80
    $ ss -nt dst 74.125.236.178          <<< Filter by address
    $ ss -nt dst 74.125.236.178/16       <<< CIDR notation is also supported
    $ ss -nt dst 74.125.236.178:80       <<< Address and Port combined

## netstat

    # netstat -a        <List All Ports (both listening and non listening ports)>
    # netstat -l        <Active Internet connections>
    # netstat -s        <Show statistics for all ports>
    # netstat -pt       <Show the PID/Program Name>

# netstat

## command of `netstat`

### (-a) List ports by protocol

    # netstat -a | more <---List All Ports (both listening and non listening ports)
    # netstat -at       <---List all tcp ports
    # netstat -au       <---List all udp ports

### (-l) List by state=Listening

    # netstat -l
    # netstat -lt
    # netstat -lu       <Active Internet connections>
    # netstat -lx       <Active UNIX domain sockets>

### (-s) Show the statistics for each protocol

    # netstat -s        <Show statistics for all ports>
    # netstat -st       <Show statistics for TCP (or) UDP ports>
    # netstat -su

### (-p) Display PID and program names

    # netstat -pt       <Show the PID/Program Name>

### (-n) Disable resolve host

- This will display in numbers, instead of resolving the host name, port name, user name.
- Also speeds up the output, as netstat is not performing any look-up.

### (-c) Auto refresh list

### (--verbose) Find the non supportive Address families in your system

### (-r) Display the kernel routing information

### (-i, -ie) Show the list of network interfaces

## sample output

### netstat -a | more

      Active Internet connections (servers and established)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      tcp        0      0 localhost:30037         *:*                     LISTEN
      udp        0      0 *:bootpc                *:*

      Active UNIX domain sockets (servers and established)
      Proto RefCnt Flags       Type       State         I-Node   Path
      unix  2      [ ACC ]     STREAM     LISTENING     6135     /tmp/.X11-unix/X0
      unix  2      [ ACC ]     STREAM     LISTENING     5140     /var/run/acpid.socket


    # netstat -at

      Active Internet connections (servers and established)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      tcp        0      0 localhost:30037         *:*                     LISTEN
      tcp        0      0 localhost:ipp           *:*                     LISTEN
      tcp        0      0 *:smtp                  *:*                     LISTEN
      tcp6       0      0 localhost:ipp           [::]:*                  LISTEN


    # netstat -au

      Active Internet connections (servers and established)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      udp        0      0 *:bootpc                *:*
      udp        0      0 *:49119                 *:*
      udp        0      0 *:mdns                  *:*


### netstat -l

      Active Internet connections (only servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      tcp        0      0 localhost:ipp           *:*                     LISTEN
      tcp6       0      0 localhost:ipp           [::]:*                  LISTEN
      udp        0      0 *:49119                 *:*
      List only listening TCP Ports using netstat -lt

    # netstat -lt

      Active Internet connections (only servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      tcp        0      0 localhost:30037         *:*                     LISTEN
      tcp        0      0 *:smtp                  *:*                     LISTEN
      tcp6       0      0 localhost:ipp           [::]:*                  LISTEN
      List only listening UDP Ports using netstat -lu

    # netstat -lu

      Active Internet connections (only servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      udp        0      0 *:49119                 *:*
      udp        0      0 *:mdns                  *:*
      List only the listening UNIX Ports using netstat -lx

    # netstat -lx

      Active UNIX domain sockets (only servers)
      Proto RefCnt Flags       Type       State         I-Node   Path
      unix  2      [ ACC ]     STREAM     LISTENING     6294     private/maildrop
      unix  2      [ ACC ]     STREAM     LISTENING     6203     public/cleanup
      unix  2      [ ACC ]     STREAM     LISTENING     6302     private/ifmail
      unix  2      [ ACC ]     STREAM     LISTENING     6306     private/bsmtp

### netstat -s

      Ip:
          11150 total packets received
          1 with invalid addresses
          0 forwarded
          0 incoming packets discarded
          11149 incoming packets delivered
          11635 requests sent out
      Icmp:
          0 ICMP messages received
          0 input ICMP message failed.
      Tcp:
          582 active connections openings
          2 failed connection attempts
          25 connection resets received
      Udp:
          1183 packets received
          4 packets to unknown port received.
      .....


    ### netstat -p option can be combined with any other netstat option.
    ###   This will add the “PID/Program Name” to the netstat output. This is very useful while debugging to identify which program is running on a particular port.

### netstat -pt

      Active Internet connections (w/o servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
      tcp        1      0 ramesh-laptop.loc:47212 192.168.185.75:www        CLOSE_WAIT  2109/firefox
      tcp        0      0 ramesh-laptop.loc:52750 lax:www ESTABLISHED 2109/firefox


    # netstat -an

    ### If you don’t want only any one of those three items ( ports, or hosts, or users ) to be resolved, use following commands.
    # netsat -a --numeric-ports
    # netsat -a --numeric-hosts
    # netsat -a --numeric-users


    ### netstat will print information continuously every few seconds.

### netstat -c

      Active Internet connections (w/o servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State
      tcp        0      0 ramesh-laptop.loc:36130 101-101-181-225.ama:www ESTABLISHED
      tcp        1      1 ramesh-laptop.loc:52564 101.11.169.230:www      CLOSING
      tcp        0      0 ramesh-laptop.loc:43758 server-101-101-43-2:www ESTABLISHED
      tcp        1      1 ramesh-laptop.loc:42367 101.101.34.101:www      CLOSING
      ^C

    ### Find the non supportive Address families in your system

### netstat --verbose

    At the end, you will have something like this.

    netstat: no support for `AF IPX' on this system.
    netstat: no support for `AF AX25' on this system.
    netstat: no support for `AF X25' on this system.
    netstat: no support for `AF NETROM' on this system.

### netstat -r
Display the kernel routing information using netstat -r

      Kernel IP routing table
      Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
      192.168.1.0     *               255.255.255.0   U         0 0          0 eth2
      link-local      *               255.255.0.0     U         0 0          0 eth2
      default         192.168.1.1     0.0.0.0         UG        0 0          0 eth2
      Note: Use netstat -rn to display routes in numeric format without resolving for host-names.

### netstat -i
Show the list of network interfaces

      Kernel Interface table
      Iface   MTU Met   RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
      eth0       1500 0         0      0      0 0             0      0      0      0 BMU
      eth2       1500 0     26196      0      0 0         26883      6      0      0 BMRU
      lo        16436 0         4      0      0 0             4      0      0      0 LRU

    ### Display extended information on the interfaces (similar to ifconfig) using netstat -ie:
    # netstat -ie

      Kernel Interface table
      eth0      Link encap:Ethernet  HWaddr 00:10:40:11:11:11
                UP BROADCAST MULTICAST  MTU:1500  Metric:1
                RX packets:0 errors:0 dropped:0 overruns:0 frame:0
                TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                collisions:0 txqueuelen:1000
                RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
                Memory:f6ae0000-f6b00000

# ss: a substitution of netstat

    ss -t -a dumps all TCP sockets
    ss -u -a dumps all UDP sockets
    ss -w -a dumps all RAW sockets
    ss -x -a dumps all UNIX sockets

    Option -o shows TCP timers state.
    Option -e shows some extended information.

## filter by socket states

    $ ss (action: state|exclude) <state>

F.e. to dump all tcp sockets except SYN-RECV:

    $ ss exclude SYN-RECV

    - all - for all the states
    - bucket - for TCP minisockets (TIME-WAIT|SYN-RECV)
    - big - all except for minisockets
    - connected - not closed and not listening
    - synchronized - connected and not SYN-SENT

If neither state nor exclude directives are present, state filter defaults to all with option -a or to all, excluding:
listening, syn-recv, time-wait and closed sockets.

some state identifier. abbreviations:

  1. established
  2. syn-sent
  3. syn-recv
  4. fin-wait-1
  5. fin-wait-2
  6. time-wait
  7. closed
  8. close-wait
  9. last-ack
  10. closing
  11. all - All of the above states
  12. connected - All the states except for listen and closed
  13. synchronized - All the connected states except for syn-sent
  14. bucket - Show states, which are maintained as minisockets, i.e. time-wait and syn-recv.
  15. big - Opposite to bucket state.


### Samples

1) List all the tcp sockets in state FIN-WAIT-1 for our apache to network 193.233.7/24 and look at their timers:

    $ ss -o state fin-wait-1 \( sport = :http or sport = :https \) \
                          dst 193.233.7/24

Oops, forgot to say that missing logical operation is equivalent to and.

2) Well, now look at the rest...

    $ ss -o excl fin-wait-1
    $ ss state fin-wait-1 \( sport neq :http and sport neq :https \) \
                       or not dst 193.233.7/24

Note that we have to do `two` calls of ss to do this. State match is always anded to address/port match.
The reason for this is purely technical:
  - ss does fast skip of not matching states before parsing addresses
  - and I consider the ability to skip fastly gobs of time-wait and syn-recv sockets as more important than logical generality.

3) So, let's look at all our sockets using autobound ports:

    $ ss -a -A all autobound

4) And eventually find all the local processes connected to local X servers:

    $ ss -xp dst "/tmp/.X11-unix/*"

Pardon, this does not work with current kernel, patching is required. But we still can look at server side:

    $ ss -x src "/tmp/.X11-unix/*"

# iproute

    # rpm -qf $(which ip)

      iproute-2.6.18-9.el5

从某种意义上说，iproute工具集几乎可以替代掉net-tools工具集，具体的替代方案是这样的：
```
     用途        net-tool（被淘汰） iproute2
  -----------------------------------------------
  地址和链路配置 ifconfig           ip-addr,ip-link
  路由表         route              ip-route
  邻居           arp                ip-neigh
  VLAN           vconfig            ip-link
  隧道           iptunnel           ip-tunnel
  组播           ipmaddr            ip-maddr
  统计           netstat            ss
```

## IP tools

- ip link set--改变设备的属性
- ip link show--显示设备属性
- ip address add--添加一个新的协议地址
- ip address delete--删除一个协议地址.
- ip address show--显示协议地址
- ip address flush--清除协议地址
- ip neighbour show --neighbour/arp表管理命令
- ip neighbour add -- 添加一个新的邻接条目
- ip neighbour change--修改一个现有的条目
- ip neighbour replace--替换一个已有的条目
- ip route show --路由
- ip route add -- 添加新路由
- ip route change -- 修改路由
- ip route replace -- 替换已有的路由
- ip route flush -- 替换已有的路由
- ip maddress -- 多播地址管理,
- ip mroute -- 多播路由缓存管理
- ip tunnel -- 通道配置
- ip monitor和rtmon -- 状态监视

## options

ip [OPTIONS] OBJECT [COMMAND [ARGUMENTS]]

OPTIONS是修改ip行为或改变其输出的选项。所有的选项都是以-字符开头，分为长、短两种形式。

OBJECT是要管理者获取信息的对象：
-V,-Version 打印ip的版本并退出。
-s,-stats,-statistics 输出更为详尽的信息。如果这个选项出现两次或多次，则输出的信息将更为详尽。
-f,-family 这个选项后面接协议种类，包括inet、inet6或link，强调使用的协议种类。如果没有足够的信息告诉ip使用的协议种类，ip就会使用默认值inet或any。link比较特殊，它表示不涉及任何网络协议。
-4 是-family inet的简写。
-6 是-family inet6的简写。
-0 是-family link的简写。
-o,-oneline 对每行记录都使用单行输出，回行用字符代替。如果需要使用wc、grep等工具处理ip的输出，则会用到这个选项。
-r,-resolve 查询域名解析系统，用获得的主机名代替主机IP地址
COMMAND 设置针对指定对象执行的操作，它和对象的类型有关。

一般情况下，ip支持对象的增加(add)、删除(delete)和展示(show或list)。
对于所有的对象，用户可以使用help命令获得帮助。
如果没有指定对象的操作命令，ip会使用默认的命令list，或者help命令。
ARGUMENTS 是命令的一些参数，它们倚赖于对象和命令。
ip支持两种类型的参数：flag和parameter。
flag由一个关键词组成；
parameter由一个 关键词加一个数值组成。
为了方便，每个命令都有一个可以忽略的默认参数。例如，参数dev是ip link命令的默认参数，因此ip link ls eth0等于ip link ls dev eth0。


## ip link show [ DEVICE ]

    # ip link set wlan down
    # ip link set eth0 name wlan            # rename interface
    # ip link set wlan up

## ifconfig

### list detail

    # ifconfig -a   # list all interface

    KVM-125 # sys ifconfig vlan125

    vlan125 Link encap:Ethernet  HWaddr 52:54:00:BD:0C:1C
            inet addr:192.168.17.125  Bcast:192.168.17.255  Mask:255.255.255.0
            UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
            RX packets:176 errors:0 dropped:0 overruns:0 frame:0
            TX packets:131 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000
            RX bytes:13933 (13.6 KB)  TX bytes:15071 (14.7 KB)

    KVM-125 # dia netlink interface list | grep vlan125 -C6

      if=port_ha family=00 type=1 index=8 mtu=1496 link=0 master=0
      ref=11 state=off start present fw_flags=0 flags=up broadcast multicast

      if=vsys_fgfm family=00 type=772 index=9 mtu=16436 link=0 master=0
      ref=15 state=off start fw_flags=0 flags=up loopback run

      if=vlan125 family=00 type=1 index=11 mtu=1500 link=0 master=0
      ref=15 state=off start fw_flags=0 flags=up broadcast run multicast

### toggle a interface

    # ifconfig eth0 down
    # ifconfig eth0 up

### Assign ip-address

    # ifconfig eth0 192.168.2.2
    # ifconfig eth0 netmask 255.255.255.0
    # ifconfig eth0 broadcast 192.168.2.255
    # ifconfig eth0 mtu 1500

    # ifconfig eth0 192.168.2.2 netmask 255.255.255.0 broadcast 192.168.2.255

### promisc mode

By default when a network card receives a packet,
it checks whether the packet belongs to itself.
If not, the interface card normally drops the packet.
But in promiscuous mode, the card doesn’t drop the packet.
Instead, it will accept all the packets which flows through the network card.

Superuser privilege is required to set an interface in promiscuous mode. Most network monitor tools use the promiscuous mode to capture the packets and to analyze the network traffic.

    # ifconfig eth0 promisc     # put the interface in promiscuous mode
    # ifconfig eth0 -promisc    # put the interface in normal mode.

## ip addr

    # ip addr add 192.168.2.77/24 dev lan       #添加ip
    # ip addr show dev lan
    # ip addr flush dev lan                     #清空网卡的所有ip地址

### ip address add--添加一个新的协议地址. 缩写：add、a

　　示例1：为每个地址设置一个字符串作为标签。为了和Linux-2.0的网络别名兼容，这个字符串必须以设备名开头，接着一个冒号，
　　# ip addr add local 192.168.4.1/28 brd + label eth0:1 dev eth0

　　示例2: 在以太网接口eth0上增加一个地址192.168.20.0，掩码长度为24位(155.155.155.0)，标准广播地址，标签为eth0:Alias：
　　# ip addr add 192.168.4.2/24 brd + dev eth1 label eth1:1
　　这个命令等于传统的: ifconfig eth1:1 192.168.4.2

### ip address delete--删除一个协议地址. 缩写：delete、del、d
　　# ip addr del 192.168.4.1/24 brd + dev eth0 label eth0:Alias1

### ip address show--显示协议地址. 缩写：show、list、lst、sh、ls、l
　　# ip addr ls eth0

### ip address flush--清除协议地址. 缩写：flush、f
　　示例1 : 删除属于私网10.0.0.0/8的所有地址：
　　# ip -s -s a f to 10/8

　　示例2 : 取消以太网卡eth0的IPv4地址
　　# ip -4 addr flush label "eth0"

## ip neigh

    # ip neigh show	#显示ip与mac对应关系
    # ip neigh flush dev lan

# ip route

must enable ip_forward:

    # ip route	#相当于route -n
    # ip route add 192.168.2.0/24 via 192.168.1.1 dev lan	#添加一条路由：去往2.0网段，通过lan网卡，下一跳IP为192.168.1.1
    # ip route add 0.0.0.0/0 via 10.10.10.30 dev wan	#添加默认路由
    # ip route add default via 10.10.10.30 dev wan		#添加默认路由
    # ip route del 192.168.2.0/24
    # traceroute www.google.com	#路由追踪
    # tracepath www.google.com	#..
    # mtr www.google.com		#动态刷新追踪


## ECMP(Equal Cost Multipath等值多路径路由)

当路由上有多个链路接入时，并且同时使用，可以考虑ECMP技术
添加两个默认路由，使用rr调度算法根据会话轮询

    # ip route help		#查看帮助
    # ip route add default mpath rr nexthop via 192.168.96.254 dev vmnet1 nexthop via 192.168.203.254 dev vmnet8
    # ip route 		#这样就会有两条默认路由了

    设置权重
    # ip route add default mpath rr nexthop via 192.168.96.254 dev vmnet1 weight 100 nexthop via 192.168.203.254 dev vmnet8 weight 10	#权重最大256


    ### check ip rule
    # ip route list table local	#最先查的表
    # ip route list table main	#平时操作的表
    # ip route list table default


## 1. 策略路由: 基于源地址

根据源客户端的子网网段走向相应的路由路径
例如：销售部门和办公部门，让销售部门享受10M带宽线路，让办公部门享受1M带宽线路；

### Requirement

- 让公司192.168.0.0/24网段的客户走网通路由
- 192.168.1.0/24网段的走电信路由

### users
Client1：192.168.0.1
Client2：192.168.1.2
Client3：20.0.0.1

### Gateway (linux PC)

对内：
I1:192.168.0.254	eth0
I2:192.168.1.254	eth0

对外：
E1:202.106.0.21		eth1
E2:202.106.46.152	eth1

### 网通CNC网关
C1:202.106.0.20		eth0
C2:20.0.0.2		    	eth1

### 电信TEL网关
T1:202.106.46.151 	eth0
T2:20.0.0.3		         eth1

### Gateway配置：

#### 增加自定义的路由表

    # vi /etc/iproute2/rt_tables
    100 	tab1
    101 	tab2

#### 添加路由规则

    # ip route add default via 202.106.0.20 dev eth1 table tab1	#添加默认路由到表tab1
    # ip route add default via 202.106.46.151 dev eth1 table tab2	#添加默认路由到表tab2
    # ip rule add from 192.168.1.0/24 table tab1			#来自192.168.1.0/24网段的请求走tab1表
    # ip rule add from 192.168.0.0/24 table tab2
    # ip rule
    # ip route add 192.168.1.0/24 dev eth0 table tab1	#添加直连路由，若不添加则Client1 ping GW后，数据包不能返回，因为tab1表中只有一个default路由
    # ip route add 192.168.0.0/24 dev eth0 table tab2

### TEL配置：

    添加去往Client1/2的路由
    # ip route add 192.168.0.0/24  via 202.106.46.152 dev eth0
    # ip route add 192.168.1.0/24  via 202.106.46.152 dev eth0

### CNC配置：

    添加去往Client1/2的路由
    # ip route add 192.168.0.0/24  via 202.106.0.21 dev eth0
    # ip route add 192.168.1.0/24  via 202.106.0.21 dev eth0

### Client配置：

    Client1\2:
    # ip route add default via 192.168.0.254 dev eth0
    # ip route add default via 192.168.1.254 dev eth0

    Client3:
    # ip route add default via 20.0.0.3 dev eth0	#测试仅从TEL路径返回也可以双路返回
    # ip route add default mpath rr nexthop via 20.0.0.2 dev eth0 nexthop via 20.0.0.3 dev eth0

    Client1\2测试:
    # traceroute 20.0.0.1


## 2. 基于防火墙标记的路由(firemark)

- 将来自不同ip段的数据包打上不同的防火墙标记，
- 根据防火墙的标记路由到相应的地址

### GW配置：

    1-100的IP标记为1，101-253的IP标记为10
    # iptables -t mangle -A PREROUTING -m iprange --src-range 192.168.1.1-192.168.1.100 -j MARK --set-mark 1
    # iptables -t mangle -A PREROUTING -m iprange --src-range 192.168.1.101-192.168.1.253 -j MARK --set-mark 10

    先清空之前的rule
    # ip rule del from 192.168.1.0/24
    # ip rule del from 192.168.0.0/24

    # ip rule add fwmark 1 pref 1000 table tab1 	#将标记为1的包送至tab1，pref为优先级
    # ip rule add fwmark 10 pref 2000 table tab2
    # ip rule
    0:  	from all lookup 255
    1000:		....	tab1
    2000:		....	tab2
    32766:  from all lookup main
    32767:  from all lookup default
    剩余基本同上
    # ip route add default via 202.106.0.20 dev eth1 table tab1	#添加默认路由到表tab1
    # ip route add default via 202.106.46.151 dev eth1 table tab2
    # ip route add 192.168.1.0/24 dev eth0 table tab1		#添加直连路由
    # ip route add 192.168.0.0/24 dev eth0 table tab2
    ........


## 3. 基于目的地址策略路由

根据访问的目标地址返回，访问网通的IP段走CNC，访问电信的走TEL

### GW配置：

    删除规则
    # iptables -F -t mangle
    # ip rule del fwmark 1 pref 1000 table tab1
    # ip rule del fwmark 10 pref 2000 table tab2

    # ip rule add to 20.0.0.1 table tab2
    # ip rule add to 20.0.0.4 table tab1
    # ip rule

    其余配置同上

    Client1\2测试:
    # traceroute 20.0.0.1
    # traceroute 20.0.0.4

假如访问教育网或国外网络，可以在main表中添加一条默认的路由


# ip link

## ip link set--改变设备的属性. 缩写：set、s

　　示例1：up/down 起动／关闭设备。
　　# ip link set dev eth0 up
　　这个等于传统的 # ifconfig eth0 up(down)

　　示例2：改变设备传输队列的长度。
　　参数:txqueuelen NUMBER或者txqlen NUMBER
　　# ip link set dev eth0 txqueuelen 100

　　示例3：改变网络设备MTU(最大传输单元)的值。
　　# ip link set dev eth0 mtu 1500

　　示例4： 修改网络设备的MAC地址。
　　参数: address LLADDRESS
　　# ip link set dev eth0 address 00:01:4f:00:15:f1

## ip link show--显示设备属性. 缩写：show、list、lst、sh、ls、l
　　-s选项出现两次或者更多次，ip会输出更为详细的错误信息统计。

　　示例:
　　# ip -s -s link ls eth0
　　这个命令等于传统的 ifconfig eth0

6. ip neighbour--neighbour/arp表管理命令
　　缩写 neighbour、neighbor、neigh、n
　　命令 add、change、replace、delete、fulsh、show(或者list)
　　缩写：add、a；change、chg；replace、repl

　　ip neighbour add -- 添加一个新的邻接条目
　　ip neighbour change--修改一个现有的条目
　　ip neighbour replace--替换一个已有的条目

　　示例1: 在设备eth0上，为地址10.0.0.3添加一个permanent ARP条目：
　　# ip neigh add 10.0.0.3 lladdr 0:0:0:0:0:1 dev eth0 nud perm

　　示例2:把状态改为reachable
　　# ip neigh chg 10.0.0.3 dev eth0 nud reachable

　　示例1:删除设备eth0上的一个ARP条目10.0.0.3
　　# ip neigh del 10.0.0.3 dev eth0

   ip neighbour show--显示网络邻居的信息. 缩写：show、list、sh、ls
　　示例1: # ip -s n ls 193.233.7.254
　　     193.233.7.254. dev eth0 lladdr 00:00:0c:76:3f:85 ref 5 used 12/13/20 nud reachable

　　ip neighbour flush--清除邻接条目. 缩写：flush、f
　　示例1: (-s 可以显示详细信息)
　　# ip -s -s n f 193.233.7.254

7. 路由表管理, 缩写 route、ro、r

　　内核把路由归纳到许多路由表中，这些表都进行了编号，编号数字的范围是1到255。另外，为了方便，还可以在/etc/iproute2/rt_tables中为路由表命名。
　　默认情况下，所有的路由都会被插入到表main(编号254)中。在进行路由查询时，内核只使用路由表main。

　　ip route add -- 添加新路由
　　ip route change -- 修改路由
　　ip route replace -- 替换已有的路由
　　    缩写：add、a；change、chg；replace、repl

　　示例0: 添加缺省路由
　　# ip route add default via 192.168.1.254
　　# ip route change default via 192.168.99.113

　　示例1: 设置到网络10.0.0/24的路由经过网关193.233.7.65
　　# ip route add 10.0.0/24 via 193.233.7.65

　　示例2: 修改到网络10.0.0/24的直接路由，使其经过设备dummy
　　# ip route chg 10.0.0/24 dev dummy

　　示例3: 实现链路负载平衡.加入缺省多路径路由，让ppp0和ppp1分担负载(注意：scope值并非必需，它只不过是告诉内核，这个路由要经过网关而不是直连的。实际上，如果你知道远程端点的地址，使用via参数来设置就更好了)。
　　# ip route add default scope global nexthop dev ppp0 nexthop dev ppp1
　　# ip route replace default scope global nexthop dev ppp0 nexthop dev ppp1

　　示例4: 设置NAT路由。在转发来自192.203.80.144的数据包之前，先进行网络地址转换，把这个地址转换为193.233.7.83
　　# ip route add nat 192.203.80.142 via 193.233.7.83

　　示例5: 实现数据包级负载平衡,允许把数据包随机从多个路由发出。weight 可以设置权重.
   # ip route replace default equalize nexthop via 211.139.218.145 dev eth0 weight 1 nexthop via 211.139.218.145 dev eth1 weight 1

　　ip route delete-- 删除路由, 缩写：delete、del、d

　　示例1:删除上一节命令加入的多路径路由
　　# ip route del default scope global nexthop dev ppp0 nexthop dev ppp1

　　ip route show -- 列出路由, 缩写：show、list、sh、ls、l
　　示例1: 计算使用gated/bgp协议的路由个数
　　# ip route ls proto gated/bgp |wc

　　示例2: 计算路由缓存里面的条数，由于被缓存路由的属性可能大于一行，以此需要使用-o选项
　　# ip -o route ls cloned |wc

　　示例3: 列出路由表TABLEID里面的路由。缺省设置是table main。TABLEID或者是一个真正的路由表ID或者是/etc/iproute2/rt_tables文件定义的字符串，
　　或者是以下的特殊值：
	　　all -- 列出所有表的路由；
	　　cache -- 列出路由缓存的内容。
　　        ip ro ls 193.233.7.82 tab cache

　　示例4: 列出某个路由表的内容
　　# ip route ls table fddi153

　　示例5: 列出默认路由表的内容
　　# ip route ls
　　这个命令等于传统的: route

　　ip route flush -- 擦除路由表

　　示例1: 删除路由表main中的所有网关路由（示例：在路由监控程序挂掉之后）：
　　# ip -4 ro flush scope global type unicast

　　示例2:清除所有被克隆出来的IPv6路由：
　　# ip -6 -s -s ro flush cache

　　示例3: 在gated程序挂掉之后，清除所有的BGP路由：
　　# ip -s ro f proto gated/bgp

　　示例4: 清除所有ipv4路由cache
　　# ip route flush cache

　　ip route get -- 获得单个路由 .缩写：get、g
　　使用这个命令可以获得到达目的地址的一个路由以及它的确切内容。
　　ip route get命令和ip route show命令执行的操作是不同的。
　　ip route show命令只是显示现有的路由，而ip route get命令在必要时会派生出新的路由。

　　示例1: 搜索到193.233.7.82的路由
　　# ip route get 193.233.7.82
　　    193.233.7.82 dev eth0 src 193.233.7.65 realms inr.ac cache mtu 1500 rtt 300

　　示例2: 搜索目的地址是193.233.7.82，来自193.233.7.82，从eth0设备到达的路由（这条命令会产生一条非常有意思的路由，这是一条到193.233.7.82的回环路由）
　　# ip r g 193.233.7.82 from 193.233.7.82 iif eth0
　　    193.233.7.82 from 193.233.7.82 dev eth0 src 193.233.7.65 realms inr.ac/inr.ac
　　    cache <src-direct,redirect> mtu 1500 rtt 300 iif eth0

8. ip route -- 路由策略数据库管理命令

　　add、delete、show(或者list)
　　注意：策略路由(policy routing)不等于路由策略(rouing policy)。
　　在某些情况下，我们不只是需要通过数据包的目的地址决定路由，可能还需要通过其他一些域：源地址、IP协议、传输层端口甚至数据包的负载。
　　这就叫做：策略路由(policy routing)。

   ip rule add -- 插入新的规则
   ip rule delete -- 删除规则
　　缩写：add、a；delete、del、d

　　示例1: 通过路由表inr.ruhep路由来自源地址为192.203.80/24的数据包
　　ip ru add from 192.203.80/24 table inr.ruhep prio 220

　　示例2:把源地址为193.233.7.83的数据报的源地址转换为192.203.80.144，并通过表1进行路由
　　ip ru add from 193.233.7.83 nat 192.203.80.144 table 1 prio 320

　　示例3:删除无用的缺省规则
　　ip ru del prio 32767

　　ip rule show -- 列出路由规则, 缩写：show、list、sh、ls、l

　　示例1: # ip ru ls
	　　0: from all lookup local
	　　32762: from 192.168.4.89 lookup fddi153
	　　32764: from 192.168.4.88 lookup fddi153
	　　32766: from all lookup main
	　　32767: from all lookup 253

9. ip maddress -- 多播地址管理, 缩写：show、list、sh、ls、l

　　ip maddress show -- 列出多播地址
　　示例1: # ip maddr ls dummy

　　ip maddress add -- 加入多播地址
　　ip maddress delete -- 删除多播地址, 缩写：add、a；delete、del、d
　　使用这两个命令，我们可以添加／删除在网络接口上监听的链路层多播地址。这个命令只能管理链路层地址。

　　示例1: 增加 # ip maddr add 33:33:00:00:00:01 dev dummy
　　示例2: 查看 # ip -O maddr ls dummy
	　　2: dummy
	　　link 33:33:00:00:00:01 users 2 static
	　　link 01:00:5e:00:00:01

　　示例3: 删除
　　# ip maddr del 33:33:00:00:00:01 dev dummy
　　
10.ip mroute -- 多播路由缓存管理

　　ip mroute show -- 列出多播路由缓存条目, 缩写：show、list、sh、ls、l

　　示例1:查看 # ip mroute ls
	　　(193.232.127.6, 224.0.1.39) Iif: unresolved
	　　(193.232.244.34, 224.0.1.40) Iif: unresolved
	　　(193.233.7.65, 224.66.66.66) Iif: eth0 Oifs: pimreg

　　示例2:查看
　　# ip -s mr ls 224.66/16

11. ip tunnel -- 通道配置, 缩写tunnel、tunl

　　ip tunnel add -- 添加新的通道
　　ip tunnel change -- 修改现有的通道
　　ip tunnel delete -- 删除一个通道
　　缩写：add、a；change、chg；delete、del、d

　　示例1:建立一个点对点通道，最大TTL是32
　　# ip tunnel add Cisco mode sit remote 192.31.7.104 local 192.203.80.1 ttl 32
　　ip tunnel show -- 列出现有的通道, 缩写：show、list、sh、ls、l
　　示例1: # ip -s tunl ls Cisco

12. ip monitor和rtmon -- 状态监视
　　ip命令可以用于连续地监视设备、地址和路由的状态。这个命令选项的格式有点不同，命令选项的名字叫做monitor，接着是操作对象：

　　ip monitor [ file FILE ] [ all | OBJECT-LIST ]
　　示例1: # rtmon file /var/log/rtmon.log
　　示例2: # ip monitor file /var/log/rtmon.log r


# Howtos

## vlan

    $ sudo ip link add link eth0 name eth0.5 type vlan id 5
    $ sudo ip link
    $ sudo ip -d link show eth0.5

    $ sudo ip addr add 192.168.17.122/24 brd 192.168.17.255 dev eth0.5
    $ sudo ip link set dev eth0.5 up

    $ sudo ip route change default via 192.168.17.125
    $ ip route list
    $ ping 192.168.17.125
    $ ping 8.8.8.8

    $ sudo ip address flush dev eth0.5
    $ sudo ip link set dev eth0.5 down
    $ sudo ip link delete eth0.5

  [1]: http://www.cyberciti.biz/files/ss.html
  [2]: http://www.binarytides.com/linux-ss-command/
  [6]: https://networkengineering.stackexchange.com/questions/14965/icmp-redirect-static-routing