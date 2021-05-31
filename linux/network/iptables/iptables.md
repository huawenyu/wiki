---
layout: post
date:   2014-02-17 13:31:01 +0800
categories: network
tags: develop, network
title:  "Linux iptables"
---

* content
{:toc}


# Doc

[Iptables-tutorial 1.2.1](https://www.frozentux.net/iptables-tutorial/chunkyhtml/index.html)
[An In-Depth Guide to iptables, the Linux Firewall](https://www.booleanworld.com/depth-guide-iptables-linux-firewall/)
[Connection tracking](https://www.rigacci.org/wiki/lib/exe/fetch.php/doc/appunti/linux/sa/iptables/conntrack.html)

## iptables: tables

If you load the ipchains module, you can't use iptables anymore.
You can even load the ipfwadm module if you want ipfwadm support.
So it's `iptables`, or `ipchains`, or `ipfwadm`, but no combination is possible.


```
                       +-----------------------------------------------+
                       |                 上层协议栈                    |
                       +----------+----------------------+-------------+
                                  ^                      |
                                  |                      |
              +----------------------------------------------------------------+
              |                   | Netfilter Hook Point |                     |
              |                   |                      v                     |
              |                   |                   <ROUT>                   |
              |                   |                      +                     |
              |                +--+-------+    +---------v-+                   |
              |                | LOCAL_IN |    | LOCAL_OUT |                   |
              |                +---^------+    +---------+-+                   |
              |                    +                     |                     |
              |                  <ROUT>                  v                     |
              |                    ^                                           |
   数据包入口 |   +-------------+  |   +---------+      +--------------+       | 数据包出口
  ----------> |   | PRE_ROUTING +--+-> | FORWARD +----> | POST_ROUTING |-------|------------>
              |   +-------------+      +---------+      +--------------+       |
              |                                                                |
              +----------------------------------------------------------------+

```

## Kernel Packet Traveling Diagram

https://unix.stackexchange.com/questions/104609/no-internet-even-with-iptables-accept-all

```
                                Network
                        -----------+-----------
                                   |
                      +--------------------------+
              +-------+-------+        +---------+---------+
              |    IPCHAINS   |        |      IPTABLES     |
              |     INPUT     |        |     PREROUTING    |
              +-------+-------+        | +-------+-------+ |
                      |                | |   conntrack   | |
                      |                | +-------+-------+ |
                      |                | |   mangle/raw  | | <- MARK WRITE
                      |                | +-------+-------+ |
                      |                | |      IMQ      | |
                      |                | +-------+-------+ |
                      |                | |      nat      | | <- DEST REWRITE
                      |                | +-------+-------+ |     DNAT or REDIRECT or DE-MASQUERADE
                      |                +---------+---------+
                      +------------+-------------+
                                   |
                           +-------+-------+
                           |      QOS      |
                           |    INGRESS    |
                           +-------+-------+
                                   |
             packet is for   +-----+-----+   packet is for
              this machine  /    INPUT    \  another address
            +--------------+    ROUTING    +--------------+
            |               \   + PDBB    /               |
            |                +-----------+                |
    +-------+-------+        Route base-on dst-addr       |
    |   IPTABLES    |                                     |
    |     INPUT     |                                     |
    | +-----+-----+ |                                     |
    | |   mangle  | |                                     |
    | +-----+-----+ |                                     |
    | |   filter  | |                                     |
    | +-----+-----+ |                                     |
    +-------+-------+                                     |
            |                               +---------------------------+
    +-------+-------+                       |                           |
    |     Local     |               +-------+-------+           +-------+-------+
    |    Process    |               |    IPCHAINS   |           |    IPTABLES   |
    +-------+-------+               |    FORWARD    |           |    FORWARD    |
            |                       +-------+-------+           | +-----+-----+ |
      +-----+-----+                         |                   | |  mangle   | | <- MARK WRITE
     /   OUTPUT    \                        |                   | +-----+-----+ |
     \   ROUTING   /                        |                   | |  filter   | |
      +-----+-----+                         |                   | +-----+-----+ |
            |                               |                   +-------+-------+
    +-------+-------+                       |                           |
    |    IPTABLES   |                       +---------------------------+
    |     OUTPUT    |                                     |
    | +-----------+ |                                     |
    | | conntrack | |                                     |
    | +-----+-----+ |                                     |
    | |   mangle  | | <- MARK WRITE                       |
    | +-----+-----+ |                                     |
    | |    nat    | | <-DEST REWRITE                      |
    | +-----+-----+ |     DNAT or REDIRECT                |
    | |   filter  | |                                     |
    | +-----+-----+ |                                     |
    +-------+-------+                                     |
            |                                             |
            +----------------------+----------------------+
                                   |
                      +------------+------------+
                      |                         |
              +-------+-------+       +---------+---------+
              |    IPCHAINS   |       |      IPTABLES     |
              |     OUTPUT    |       |    POSTROUTING    |
              +-------+-------        | +-------+-------+ |
                      |               | |    mangle     | | <- MARK WRITE
                      |               | +-------+-------+ |
                      |               | |      nat      | | <- SOURCE REWRITE
                      |               | +-------+-------+ |      SNAT or MASQUERADE
                      |               | |      IMQ      | |
                      |               | +-------+-------+ |
                      |               +---------+---------+
                      +------------+------------+
                                   |
                            +------+------+
                            |     QOS     |
                            |    EGRESS   |
                            +------+------+
                                   |
                        -----------+-----------
                                Network
```

### My remarks on the diagram

  - Output routing : the local process selects a source address and a route.
     This route is attached to the packet and used later.
  - Postrouting : there is also rerouting possible if netfilter changes some parts of the packets like address, tos, ... .
  - RPDB : routing policy database, controlled by ip.
     That's also the place where the kernel does source validation and nexthop decision.
  - IMQ : Packets put in the imq device travel also thru the "EGRESS" part of the diagram
     so you can use htb/cbq to control the packets in the imq device.
  - ipchains : Yes, there is some ipchains code in kernel 2.4.
  - mangle : since kernel 2.4.18, you have a mangle table in all 5 netfilter hooks.
  - IMQ in input comes before nat so IMQ does not know the real ip address.
     Ingress comes after nat, so ingress knows the real ip address.

### Leonardo old notes

  - The input routing determines local/forward.
  - ip rule (routing policy database RPDB) is input routing, more correctly, part of the input routing.
  - The output routing is performed from "higher layer".
  - nexthop and output device are determined both from the input and the output routing.
  - The forwarding process is called at input routing by functions from specific places in the code.
      It executes after input routing and does not perform nexthop/outdev selection.
      It's the process of receiving and sending the same packet,
        but in the context of all these hooks the code that sends ICMP redirects (demanded from input routing),
        decrements the IP TTL, performs dumb NAT and calls the filter chain.
      This code is used only for forwarded packets.
  - Sometimes the word "Forwarding" with "big F", is used for referencing both, the routing and forwarding process.

# Basic concepts

## Clearing the Running Config

https://netfilter.org/documentation/HOWTO/NAT-HOWTO-5.html

If you want to clear the ipset and iptables config (sets, rules, entries)
and reset to a fresh open firewall state (useful at the top of a firewall script),
run the following commands:

    iptables -P INPUT ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -t filter -F
    iptables -t raw -F
    iptables -t nat -F
    iptables -t mangle -F
    ipset -F
    ipset -X

iptables takes a number of standard options as listed below.
All the double-dash options can be abbreviated, as long as iptables can still tell them apart from the other possible options.
If your kernel has iptables support as a module, you'll need to load the ip_tables.o module first: `insmod ip_tables'.

The most important option here is the table selection option, `-t'.
For all NAT operations, you will want to use `-t nat' for the NAT table.
The second most important option to use is `-A' to append a new rule at the end of the chain (e.g. `-A POSTROUTING'),
    or `-I' to insert one at the beginning (e.g. `-I PREROUTING').

You can specify the source (`-s' or `--source') and destination (`-d' or `--destination') of the packets you want to NAT.
These options can be followed by a single IP address (e.g. 192.168.1.1), a name (e.g. www.gnumonks.org), or a network address (e.g. 192.168.1.0/24 or 192.168.1.0/255.255.255.0).

You can specify the incoming (`-i' or `--in-interface') or outgoing (`-o' or `--out-interface') interface to match,
    but which you can specify depends on which chain you are putting the rule into: at PREROUTING you can only select incoming interface,
    and at POSTROUTING you can only select outgoing interface.
    If you use the wrong one, iptables will give an error.

## Simple Selection using iptables

- The iptables contains five tables: `raw`, `filter`, `nat`, `mangle`, and `security`;
- And the tables may consist of some of chains: `INPUT`, `PREROUTING`, `FORWARD`, `POSTROUTING`, and `OUTPUT`;
- And the chains contain any rules added by customer or us.

iptables is used to inspect, modify, forward, redirect, and/or drop IPv4 packets. The code
for filtering IPv4 packets is already built into the kernel and is organized into a
collection of tables, each with a specific purpose. The tables are made up of a set of
predefined chains, and the chains contain rules which are traversed in order. Each rule
consists of a predicate of potential matches and a corresponding action (called a target)
which is executed if the predicate is true; i.e. the conditions are matched. iptables is
the user utility which allows you to work with these chains/rules. Most new users find the
complexities of linux IP routing quite daunting, but, in practice, the most common use
cases (NAT and/or basic Internet firewall) are considerably less complex.

The key to understanding how iptables works is this chart. The lowercase word on top is
the table and the upper case word below is the chain. Every IP packet that comes in on any
network interface passes through this flow chart from top to bottom. A common source of
confusion is that packets entering from, say, an internal interface are handled
differently than packets from an Internet-facing interface. All interfaces are handled the
same way; it's up to you to define rules that treat them differently. Of course some
packets are intended for local processes, hence come in from the top of the chart and stop
at <Local Process>, while other packets are generated by local processes; hence start at
<Local Process> and proceed downward through the flowchart. A detailed explanation of how
this flow chart works can be found here.

In the vast majority of use cases you won't need to use the raw, mangle, or security
tables at all. Consequently, the following chart depicts a simplified network packet flow
through iptables:



```
                                   XXXXXXXXXXXXXXXXXX
                                 <<X     Network    X>>
                                   XXXXXXXXXXXXXXXXXX
                                           +
                                           |
                                           v
     +-------------+              +------------------+
     |table: filter| <---+        | table: nat       |
     |chain: INPUT |     |        | chain: PREROUTING|
     +-----+-------+     |        +--------+---------+
           |             |                 |
           v             |                 v
     [local process]     |           ****************          +--------------+
           |             +---------+ Routing decision +------> |table: filter |
           v                         ****************          |chain: FORWARD|
    ****************                                           +------+-------+
    Routing decision                                                  |
    ****************                                                  |
           |                                                          |
           v                        ****************                  |
    +-------------+       +------>  Routing decision  <---------------+
    |table: nat   |       |         ****************
    |chain: OUTPUT|       |               +
    +-----+-------+       |               |
          |               |               v
          v               |      +-------------------+
    +--------------+      |      | table: nat        |
    |table: filter | +----+      | chain: POSTROUTING|
    |chain: OUTPUT |             +--------+----------+
    +--------------+                      |
                                          v
                                   XXXXXXXXXXXXXXXXXX
                                 <<X    Network     X>>
                                   XXXXXXXXXXXXXXXXXX
```

## Tables

iptables contains five tables:

 1. `raw` is used only for configuring packets so that they are exempt from connection
    tracking.
 2. `filter` is the default table, and is where all the actions typically associated with a
    firewall take place.
 3. `nat` is used for network address translation (e.g. port forwarding).
 4. `mangle` is used for specialized packet alterations.
 5. `security` is used for Mandatory Access Control networking rules (e.g. SELinux -- see
    this article for more details).

In most common use cases you will only use two of these: filter and nat. The other tables
are aimed at complex configurations involving multiple routers and routing decisions and
are in any case beyond the scope of these introductory remarks.

## Chains

Tables consist of chains, which are lists of rules which are followed in order.
 - The default table `filter` contains three built-in chains: INPUT, OUTPUT and FORWARD
     which are activated at different points of the packet filtering process, as illustrated in the flow chart.
 - The `nat` table includes chains: PREROUTING, POSTROUTING, and OUTPUT chains.

See man 8 iptables for a description of built-in chains in other tables.

By default, none of the chains contain any rules. It is up to you to append rules to the
chains that you want to use. Chains do have a default policy, which is generally set to
ACCEPT, but can be reset to DROP, if you want to be sure that nothing slips through your
ruleset. The default policy always applies at the end of a chain only. Hence, the packet
has to pass through all existing rules in the chain before the default policy is applied.

User-defined chains can be added to make rulesets more efficient or more easily
modifiable. See Simple stateful firewall for an example of how user-defined chains are
used.

## Rules

Packet filtering is based on rules, which are specified by multiple matches (conditions
the packet must satisfy so that the rule can be applied), and one target (action taken
when the packet matches all conditions). The typical things a rule might match on are what
interface the packet came in on (e.g eth0 or eth1), what type of packet it is (ICMP, TCP,
or UDP), or the destination port of the packet.

Targets are specified using the -j or --jump option. Targets can be either user-defined
chains (i.e. if these conditions are matched, jump to the following user-defined chain and
continue processing there), one of the special built-in targets, or a target extension.
Built-in targets are ACCEPT, DROP, QUEUE and RETURN, target extensions are, for example,
REJECT and LOG. If the target is a built-in target, the fate of the packet is decided
immediately and processing of the packet in current table is stopped. If the target is a
user-defined chain and the fate of the packet is not decided by this second chain, it will
be filtered against the remaining rules of the original chain. Target extensions can be
either terminating (as built-in targets) or non-terminating (as user-defined chains), see
man 8 iptables-extensions for details.

    - ACCEPT: This causes iptables to accept the packet.
    - DROP: iptables drops the packet. To anyone trying to connect to your system, it would appear like the system didn’t even exist.
    - REJECT: iptables `rejects` the packet.
       + It sends a `connection reset` packet in case of TCP,
       + or a `destination host unreachable` packet in case of UDP or ICMP.

## Traversing Chains

A network packet received on any interface traverses the traffic control chains of tables
in the order shown in the flow chart.
 - The first routing decision involves deciding
   + if the final destination of the packet is the local machine (in which case the packet traverses through the INPUT chains)
   + or elsewhere (in which case the packet traverses through the FORWARD chains).
 - Subsequent routing decisions involve deciding what interface to assign to an outgoing packet.
 - At each chain in the path, every rule in that chain is evaluated in order and whenever a rule matches, the corresponding target/jump action is executed.

The 3 most commonly used targets are ACCEPT, DROP, and jump to a user-defined chain.
While built-in chains can have default policies, user-defined chains can not.
If every rule in a chain that you jumped fails to provide a complete match, the packet is dropped back into
the calling chain as illustrated here. If at any time a complete match is achieved for a
rule with a DROP target, the packet is dropped and no further processing is done. If a
packet is ACCEPTed within a chain, it will be ACCEPTed in all superset chains also and it
will not traverse any of the superset chains any further. However, be aware that the
packet will continue to traverse all other chains in other tables in the normal fashion.

## Modules

There are many modules which can be used to extend iptables such as `connlimit`, `conntrack`,
`limit` and `recent`. These modules add extra functionality to allow complex filtering rules.

# NAT

## Controlling What To NAT

You need to create NAT rules which tell the kernel what connections to change, and how to change them.
To do this, we use the very versatile iptables tool, and tell it to alter the NAT table by specifying the `-t nat` option.
The table of `NAT` contains three `chains`:
 - each rule is examined in order until one matches.
 - The two chains are called PREROUTING (for Destination NAT, as packets first come in),
     and POSTROUTING (for Source NAT, as packets leave).
 - The third (OUTPUT) will be ignored here.

The following diagram would illustrate it quite well if I had any artistic talent:

       _____                                     _____
     /     \                                   /     \
   PREROUTING -->[Routing ]----------------->POSTROUTING----->
     \D-NAT/     [Decision]                    \S-NAT/
                     |                            ^
                     |                            |
                     |                            |
                     +-----> [Local Process] -----+

At each of the points above, when a packet passes we look up what connection it is associated with.
If it's a new connection, we look up the corresponding chain in the NAT table to see what to do with it.
The answer it gives will apply to all future packets on that connection.

## Why does SNAT happen in POSTROUTING chain and DNAT in PREROUTING chain?

https://unix.stackexchange.com/questions/280114/why-does-snat-happen-in-postrouting-chain-and-dnat-in-prerouting-chain

As the chain names suggest, PREROUTING is done at first when a packet is received and is thus routed based on where it is going (destination).
After all other routing rules have been applied, the POSTROUTING chain will determine where it goes based on where it came from (source).

For example, on my server, incoming ports that are to be forwarded (NATed) are all defined in the PREROUTING chain as DNAT,
    and all packets that come from the NATed interfaces, go through the POSTROUTING chain as SNAT,
    and consequently (in this case), go through the filter FORWARD chain.


Usually the main criterion for SNAT is "traffic that's going out a given interface" (i.e. -o eth0).
What interface a packet will go out is determined by routing, so to apply that criterion you need to run it in a POSTROUTING context.

DNAT rewrites the destination address of a packet, meaning it can affect where a packet goes to — for example,
     a packet that looks like it's destined for the gateway could end up being rewritten to go to a machine on the network instead.
     Since you want the routing to be able to take that rewritten destination into account when it makes its decision,
     so that the packet actually goes where it needs to, DNAT should run in a PREROUTING context.

With packets whose source is the local machine never visit the PREROUTING table, so POSTROUTING is the only choice by SNAT.

## Difference between SNAT and Masquerade

`MASQUERADE` is an iptables target that can be used instead of `SNAT` target (source NAT)
    when external ip of the inet interface is not known at the moment of writing the rule (when server gets external ip dynamically).

    # iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    # iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source xx.xx.xx.xx

Basically `SNAT` and `MASQUERADE` do the same source NAT thing in the nat table within the POSTROUTING chain.

Differences

- `MASQUERADE` does not require `--to-source` as it was made to work with dynamically assigned IPs
- `SNAT` works only with static IPs, that's why it has `--to-source`
- `MASQUERADE` has extra overhead and is slower than `SNAT` because each time `MASQUERADE` target gets hit by a packet, it has to check for the IP address to use.

The SNAT target requires you to give it an IP address to apply to all the outgoing packets.
The MASQUERADE target lets you give it an interface,
    and whatever address is on that interface is the address that is applied to all the outgoing packets.
In addition, with SNAT, the kernel's connection tracking keeps track of all the connections when the interface is taken down and brought back up;
the same is not true for the MASQUERADE target.

**NOTE**: A typical use case for `MASQUERADE`:
  - AWS EC2 instance in a VPC, it has a private IP within the VPC CIDR (e.g. 10.10.1.0/24) - 10.10.1.100 for example,
    it also has a public IP so as to communicate with the Internet(assume it is in a public subnet) thru which the private IP 1:1 NAT.
    The public IP may change after instance reboot (if it is NOT an EIP), `MASQUERADE` is a better option in this use case.

Important: It is still possible to use `MASQUERADE` target with static IP, just be aware of the extra overhead.

References

- [iptables Tutorial](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#MASQUERADETARGET)
- [NAT Tutorial](http://www.karlrupp.net/en/computer/nat_tutorial)

# Connection tracking

https://www.rigacci.org/wiki/lib/exe/fetch.php/doc/appunti/linux/sa/iptables/conntrack.html


# ipset

https://wiki.archlinux.org/index.php/Ipset
[Advanced Firewall Configurations with ipset](https://www.linuxjournal.com/content/advanced-firewall-configurations-ipset)

## list

    ipset -L -n
    ipset -L -t

# Transparent Proxy

[Kernel Doc: Transparent proxy support](https://www.kernel.org/doc/Documentation/networking/tproxy.txt)

# Troubleshooting

https://backreference.org/2010/06/11/iptables-debugging/

# Configuration and usage

iptables is a systemd service and is started accordingly. However, the service won't start
unless it finds an /etc/iptables/iptables.rules file, which is not provided by the Arch
iptables package. So to start the service for the first time:

    # touch /etc/iptables/iptables.rules

or

    # cp /etc/iptables/empty.rules /etc/iptables/iptables.rules

Then start the iptables.service unit. As with other services, if you want iptables to be
loaded automatically on boot, you must enable it.

iptables rules for IPv6 are, by default, stored in /etc/iptables/ip6tables.rules, which is
read by ip6tables.service. You can start it the same way as above.

Note: Since iptables-1.6.0-1 the iptables.service and ip6tables.service refer to the
network-pre.target so that the firewall is started before any network is configured.
Respective manual configuration changes to achieve this for prior versions (FS#33478) can
be dropped.[1]

## Save & Restore

After adding rules via command-line as shown in the following sections, the configuration
file is not changed automatically &#8212; you have to save it manually:

    # iptables-save > /etc/iptables/iptables.rules

If you edit the configuration file manually, you have to reload iptables.

Or you can load it directly through iptables:

    # iptables-restore < /etc/iptables/iptables.rules

## From the command line

### Showing the current rules

The basic command to list current rules is --list-rules (-S), which is similar in output
format to the iptables-save utility. The main difference of the two is that the latter
outputs the rules of all tables per default, while all iptables commands default to the
filter table only.

When working with iptables on the command line, the --list (-L) command accepts more
modifiers and shows more information. For example, you can check the current ruleset and
the number of hits per rule by using the command:

    # iptables -nvL

        Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
         pkts bytes target     prot opt in     out     source               destination

        Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
         pkts bytes target     prot opt in     out     source               destination

        Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
         pkts bytes target     prot opt in     out     source               destination

If the output looks like the above, then there are no rules (i.e. nothing is blocked) in
the default filter table. An other table can be specified with the -t option.

To show the line numbers when listing rules, append --line-numbers to that input. The line
numbers are a useful shorthand when #Editing rules on the command line.

### Resetting rules

You can flush and reset iptables to default using these commands:

    # iptables -F
    # iptables -X
    # iptables -t nat -F
    # iptables -t nat -X
    # iptables -t mangle -F
    # iptables -t mangle -X
    # iptables -t raw -F
    # iptables -t raw -X
    # iptables -t security -F
    # iptables -t security -X
    # iptables -P INPUT ACCEPT
    # iptables -P FORWARD ACCEPT
    # iptables -P OUTPUT ACCEPT

The -F command with no arguments flushes all the chains in its current table. Similarly,
-X deletes all empty non-default chains in a table.

Individual chains may be flushed or deleted by following -F and -X with a [chain]
argument.

### Editing rules

Rules can be edited by appending -A a rule to a chain, inserting -I it at a specific
position on the chain, replacing -R an existing rule, or deleting -D it. The first three
commands are exemplified in the following.

First of all, our computer is not a router (unless, of course, it is a router). We want to
change the default policy on the FORWARD chain from ACCEPT to DROP.

    # iptables -P FORWARD DROP

Warning: The rest of this section is meant to teach the syntax and concepts behind
iptables rules. It is not intended as a means for securing servers. For improving the
security of your system, see Simple stateful firewall for a minimally secure iptables
configuration and Security for hardening Arch Linux in general.

The Dropbox LAN sync feature broadcasts packets every 30 seconds to all computers it can
see. If we happen to be on a LAN with Dropbox clients and do not use this feature, then we
might wish to reject those packets.

    # iptables -A INPUT -p tcp --dport 17500 -j REJECT --reject-with icmp-port-unreachable

    # iptables -nvL --line-numbers

          Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
          num   pkts bytes target     prot opt in     out     source               destination
          1        0     0 REJECT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:17500 reject-with icmp-port-unreachable

          Chain FORWARD (policy DROP 0 packets, 0 bytes)
          num   pkts bytes target     prot opt in     out     source               destination

          Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
          num   pkts bytes target     prot opt in     out     source               destination


Note: We use REJECT rather than DROP here, because RFC 1122 3.3.8 requires hosts return
ICMP errors whenever possible, instead of dropping packets. This page explains why it is
almost always better to REJECT rather than DROP packets.

Now, say we change our mind about Dropbox and decide to install it on our computer. We
also want to LAN sync, but only with one particular IP on our network. So we should use -R
to replace our old rule. Where 10.0.0.85 is our other IP:

    # iptables -R INPUT 1 -p tcp --dport 17500 ! -s 10.0.0.85 -j REJECT --reject-with icmp-port-unreachable

    # iptables -nvL --line-numbers

        Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination
        1        0     0 REJECT     tcp  --  *      *      !10.0.0.85            0.0.0.0/0            tcp dpt:17500 reject-with icmp-port-unreachable

        Chain FORWARD (policy DROP 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

        Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

We have now replaced our original rule with one that allows 10.0.0.85 to access port 17500
on our computer. But now we realize that this is not scalable. If our friendly Dropbox
user is attempting to access port 17500 on our device, we should allow him immediately,
not test him against any firewall rules that might come afterwards!

So we write a new rule to allow our trusted user immediately. Using -I to insert the new
rule before our old one:

    # iptables -I INPUT -p tcp --dport 17500 -s 10.0.0.85 -j ACCEPT -m comment --comment "Friendly Dropbox"

    # iptables -nvL --line-numbers

        Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination
        1        0     0 ACCEPT     tcp  --  *      *       10.0.0.85            0.0.0.0/0            tcp dpt:17500 /* Friendly Dropbox */
        2        0     0 REJECT     tcp  --  *      *      !10.0.0.85            0.0.0.0/0            tcp dpt:17500 reject-with icmp-port-unreachable

        Chain FORWARD (policy DROP 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

        Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

And replace our second rule with one that rejects everything on port 17500:

    # iptables -R INPUT 2 -p tcp --dport 17500 -j REJECT --reject-with icmp-port-unreachable

Our final rule list now looks like this:

    # iptables -nvL --line-numbers

        Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination
        1        0     0 ACCEPT     tcp  --  *      *       10.0.0.85            0.0.0.0/0            tcp dpt:17500 /* Friendly Dropbox */
        2        0     0 REJECT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:17500 reject-with icmp-port-unreachable

        Chain FORWARD (policy DROP 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

        Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
        num   pkts bytes target     prot opt in     out     source               destination

## Guides

  * Simple stateful firewall
  * Router

# Logging

The LOG target can be used to log packets that hit a rule. Unlike other targets like
ACCEPT or DROP, the packet will continue moving through the chain after hitting a LOG
target. This means that in order to enable logging for all dropped packets, you would have
to add a duplicate LOG rule before each DROP rule. Since this reduces efficiency and makes
things less simple, a logdrop chain can be created instead.

Create the chain with:

    # iptables -N logdrop

And add the following rules to the newly created chain:

    # iptables -A logdrop -m limit --limit 5/m --limit-burst 10 -j LOG
    # iptables -A logdrop -j DROP

Explanation for limit and limit-burst options is given below.

Now whenever we want to drop a packet and log this event, we just jump to the logdrop
chain, for example:

    # iptables -A INPUT -m conntrack --ctstate INVALID -j logdrop

## Limiting log rate

The above logdrop chain uses the limit module to prevent the iptables log from growing too
large or causing needless hard drive writes. Without limiting an erroneously configured
service trying to connect, or an attacker, could fill the drive (or at least the /var
partition) by causing writes to the iptables log.

The limit module is called with -m limit. You can then use --limit to set an average rate
and --limit-burst to set an initial burst rate. In the logdrop example above:

    # iptables -A logdrop -m limit --limit 5/m --limit-burst 10 -j LOG

appends a rule which will log all packets that pass through it. The first 10 consecutive
packets will be logged, and from then on only 5 packets per minute will be logged. The
"limit burst" count is reset every time the "limit rate" is not broken, i.e. logging
activity returns to normal automatically.

## Viewing logged packets

Logged packets are visible as kernel messages in the systemd journal.

To view all packets that were logged since the machine was last booted:

    # journalctl -k | grep "IN=.*OUT=.*" | less

## syslog-ng

Assuming you are using syslog-ng, you can control where iptables' log output goes this
way:

    filter f_everything { level(debug..emerg) and not facility(auth, authpriv); };

to

    filter f_everything { level(debug..emerg) and not facility(auth, authpriv) and not filter(f_iptables); };

This will stop logging iptables output to /var/log/everything.log.

If you also want iptables to log to a different file than /var/log/iptables.log, you can
simply change the file value of destination d_iptables here (still in syslog-ng.conf)

    destination d_iptables { file("/var/log/iptables.log"); };

## ulogd

ulogd is a specialized userspace packet logging daemon for netfilter that can replace the
default LOG target. The package ulogd is available in the [community] repository.

# Howto write a iptable rules

## Skipping rules in iptables

### Using `RETURN`

A custom chain can be used to organize things more easily.
There's a an other "terminal" target more useful once in a custom chain:
  - `RETURN` to immediately come back and execute the rule after the calling rule.
  - `RETURN` in the base chain just applies the default policy, so is not so much used.

The asked example becomes:

```iptable
    iptables -N whitelist-check
    iptables -A whitelist-check -m set --match-set whitelist src -j RETURN
    iptables -A whitelist-check -p tcp --dport 22 -j DROP
    iptables -A INPUT -j whitelist-check
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

### Using `inverting logic`

Sometimes inverting logic and grouping can work too. For this simple case an equivalent method would have simply been:

    iptables -A INPUT -p tcp -m set ! --match-set whitelist src --dport 22 -j DROP
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT


**For the updated scenario**: drop everything which is not whitelisted nor from DE (nor ...). For additional exceptions, just add more rules ending with `-j RETURN` before the `-j DROP`

**Update 2**: changed the logic with `DE` since OP changed it too... if, as per OP's change, traffic is dropped for Germany, here, traffic continues for non-Germany.

```iptable
    iptables -N filterchain
    iptables -A filterchain -m set --match-set whitelist src -j RETURN
    iptables -A filterchain -m geoip ! --src-cc DE -j RETURN
    ...
    iptables -A filterchain -j DROP

    iptables -A INPUT -j filterchain
    ... other rules ...
```

## A near perfect iptables firewall configuration

https://www.lammertbies.nl/comm/info/iptables.html

```
    #
    # Example fast and scalable firewall configuration with iptables
    # Please only implement if you fully understand the functionality
    # because is very easy to lockout yourself from your computer if
    # the script isn't adapted to your specific situation.
    #

    *filter
    :INPUT ACCEPT [0:0]     <=== set buildin chain 'INPUT' default jump target/verdict
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    :Always - [0:0]         <=== create user chain 'Always'
    :Allow - [0:0]
    :Bogus - [0:0]
    :Enemies - [0:0]
    :Friends - [0:0]

    ### We can take the chain as call function
    # Like call function, enter chain 'Bogus'
    -A INPUT -j Bogus       <=== Traffic criter in chain 'INPUT', jump to user-chain 'Bogus'
    # Like call function, enter chain 'Always'
    -A INPUT -j Always      <=== After traffic RETURN from chain 'Bogus', then enter user-chain 'Always'
    -A INPUT -j Enemies
    -A INPUT -j Allow

    -A FORWARD -j Bogus
    -A FORWARD -j Always
    -A FORWARD -j Enemies
    -A FORWARD -j Allow

    # User define chain 'Bogus':
        -A Bogus -p tcp -m tcp --tcp-flags SYN,FIN SYN,FIN -j DROP      <=== The whole criter ended by 'DROP'
        -A Bogus -p tcp -m tcp --tcp-flags SYN,RST SYN,RST -j DROP
        -A Bogus -s 169.254.0.0/16 -j DROP
        -A Bogus -s 172.16.0.0/12 -j DROP
        -A Bogus -s 192.0.2.0/24 -j DROP
        -A Bogus -s 192.168.0.0/16 -j DROP
        -A Bogus -s 10.0.0.0/8 -j DROP
        -A Bogus -s 127.0.0.0/8 -i ! lo -j DROP
        ### traffic not 'DROP' return from user-chain 'Bogus', backto caller

    # User define chain 'Always':
        -A Always -p udp --dport 123 -j ACCEPT
        -A Always -m state --state ESTABLISHED,RELATED -j ACCEPT        <=== The whole criter ended by 'ACCEPT'
        -A Always -i lo -j ACCEPT

    # User define chain 'Friends':
        -A Friends -s 123.123.123.123 -j ACCEPT
        -A Friends -s 111.111.111.0/24 -j ACCEPT
        -A Friends -j DROP

    # User define chain 'Enemies':
        -A Enemies  -m recent --name psc --update --seconds 60 -j DROP
        -A Enemies -i ! lo -m tcp -p tcp --dport 1433  -m recent --name psc --set -j DROP
        -A Enemies -i ! lo -m tcp -p tcp --dport 3306  -m recent --name psc --set -j DROP
        -A Enemies -i ! lo -m tcp -p tcp --dport 8086  -m recent --name psc --set -j DROP
        -A Enemies -i ! lo -m tcp -p tcp --dport 10000 -m recent --name psc --set -j DROP
        -A Enemies -s 99.99.99.99 -j DROP

    # User define chain 'Allow':
        -A Allow -p icmp --icmp-type echo-request -j Friends
        -A Allow -p icmp --icmp-type any -m limit --limit 1/second -j ACCEPT
        -A Allow -p icmp --icmp-type any -j DROP
        -A Allow -p tcp -m state --state NEW -m tcp --dport 22 -j Friends
        -A Allow -p tcp -m state --state NEW -m tcp --dport 25 -j ACCEPT
        -A Allow -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
        -A Allow -p tcp -m state --state NEW -m tcp --dport 443 -j ACCEPT
        -A Allow -j DROP

    COMMIT
```


  [1]: https://www.netfilter.org/documentation/HOWTO/netfilter-hacking-HOWTO.txt
  [2]: http://www.docum.org/docum.org/kptd/
  [3]: http://fishcried.com/2016-02-19/iptables/
  [4]: https://gigenchang.wordpress.com/2014/04/19/10%E5%88%86%E9%90%98%E5%AD%B8%E6%9C%83iptables/
  [5]: https://my.oschina.net/HankCN/blog/117796
  [6]: https://www.frozentux.net/iptables-tutorial/chunkyhtml/
