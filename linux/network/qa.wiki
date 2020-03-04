## Does STP use Multicast?

Yes it does. The technical reference is [IEEE 802.1d](http://standards.ieee.org/getieee802/download/802.1D-2004.pdf)
The MAC multicast address is:
  - `01:80:c2:00:00:00` for the native VLAN,
  - `01:00:0c:cc:cc:cd` for the other VLANs I think.

