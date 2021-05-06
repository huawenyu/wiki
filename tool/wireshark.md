# Install

## ubuntu build-in wireshark (lower version)

	sudo add-apt-repository universe
	sudo apt install wireshark

## the newest version

	sudo add-apt-repository ppa:wireshark-dev/stable
	sudo apt update
	sudo apt install wireshark

## Running Wireshark without sudo

	sudo dpkg-reconfigure wireshark-common
	sudo chmod +x /usr/bin/dumpcap
	### sudo usermod -aG wireshark $(whoami)    +=== I can list interface without this

# Filter

	tls.handshake.type==2		+=== ClientHello
	tls.record.version			+=== The client reports its minimum version through the tls.record.version field and the server agrees to it in the Server Hello.
		Then inspect the Server Hello version field:
			tls.handshake.version
		or for TLS 1.3:
			tls.handshake.extensions.supported_version

# tshark/termshark/ssldump: command line capture

https://www.ethicalhacker.net/columns/chappell/tshark-7-tips-on-wiresharks-command-line-packet-capture-tool/
https://github.com/gcla/termshark

	sudo apt install -y  tshark
	## get the release executable termshark directly from release of https://github.com/gcla/termshark		+=== Depend on tshark

## usage of tshark

	tshark -h
	tshark -D		+=== list interface
	tshark -i etho
	tshark -i etho -w 'file1.pcap'
	tshark -i2		+=== the # come from `tshark -D`

	tshark -i ens4 -f 'host 10.1.1.1'		+=== filter:
		host 10.1.1.1				all to/from IP address 10.1.1.1
		not host www.google.com		all to/from www.google.com*
		net 10.1.0.0/16				all to/from IP subnet 10.1
		port 53						all to/from port 53 (UDP/TCP)
		tcp portrange 1-25			TCP traffic on ports 1-25
		not broadcast				all except broadcast traffic
		icmp						all ping traffic
		!arp						all except ARP traffic
		tcp and not port 80			all TCP traffic except traffic to/from port 80

## usage of termshark

https://github.com/gcla/termshark/blob/master/docs/UserGuide.md

	?		+=== get help from GUI-like

	termshark -r test.pcap		+=== Inspect a pcap file
	termshark -i eth0 icmp		+=== Capture ping packets on interface eth0
	termshark -i eth0 tcp		+=== Capture ping packets on interface eth0

	ls ~/.cache/termshark/pcaps/
		ens4--2021-05-04--11-19-25.pcap  ens4--2021-05-04--11-47-00.pcap
	rm  ~/.cache/termshark/pcaps/*

## ssldump

https://github.com/adulau/ssldump
We should build it from source.

