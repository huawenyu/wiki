# Env

Suggest install MobaXterm as our windows terminal, and enter the local bashshell for our system admin

## Check network info

$ netstat -nr
0.0.0.0          0.0.0.0      192.168.0.1    192.168.0.175     25


## Route

Syntax route [-f] [-p] [Command[Destination] [mask Network] [Gateway] [metric Metric]] [if Interface]]

Example: [ad#ad-post-1]

To display the entire contents of the IP routing table, type:

route print

To display the routes in the IP routing table that begin with 10., type:

route print 10.*

To add a default route with the default gateway address of 192.168.12.1, type:

route add 0.0.0.0 mask 0.0.0.0 192.168.12.1

To add a route to the destination 10.41.0.0 with the subnet mask of 255.255.0.0 and the next hop address of 10.27.0.1, type:

route add 10.41.0.0 mask 255.255.0.0 10.27.0.1

To add a persistent route to the destination 10.41.0.0 with the subnet mask of 255.255.0.0 and the next hop address of 10.27.0.1, type:

route -p add 10.41.0.0 mask 255.255.0.0 10.27.0.1

To add a route to the destination 10.41.0.0 with the subnet mask of 255.255.0.0, the next hop address of 10.27.0.1, and the cost metric of 7, type:

route add 10.41.0.0 mask 255.255.0.0 10.27.0.1 metric 7

To add a route to the destination 10.41.0.0 with the subnet mask of 255.255.0.0, the next hop address of 10.27.0.1, and using the interface index 0x3, type:

route add 10.41.0.0 mask 255.255.0.0 10.27.0.1 if 0x3

To delete the route to the destination 10.41.0.0 with the subnet mask of 255.255.0.0, type:

route delete 10.41.0.0 mask 255.255.0.0

To delete all routes in the IP routing table that begin with 10., type:

route delete 10.*

To change the next hop address of the route with the destination of 10.41.0.0 and the subnet mask of 255.255.0.0 from 10.27.0.1 to 10.27.0.25, type:

route change 10.41.0.0 mask 255.255.0.0 10.27.0.25





ROUTE ADD 0.0.0.0  MASK 0.0.0.0  192.168.1.3  METRIC 25
according to

C:\>route /?

Manipulates network routing tables.

ROUTE [-f] [-p] [-4|-6] command [destination]
                  [MASK netmask]  [gateway] [METRIC metric]  [IF interface]

  …
  command      One of these:
                 [PRINT](PRINT)     Prints  a route
                 ADD       Adds    a route
                 DELETE    Deletes a route
                 CHANGE    Modifies an existing route
  destination  Specifies the host.
  MASK         Specifies that the next parameter is the 'netmask' value.
  netmask      Specifies a subnet mask value for this route entry.
               If not specified, it defaults to 255.255.255.255.
  gateway      Specifies gateway.
  interface    the interface number for the specified route.
  METRIC       specifies the metric, ie. cost for the destination.

## DNS
  
  nslookup
  dig @8.8.8.8 www.tired.com
  tracert   www.tired.com
