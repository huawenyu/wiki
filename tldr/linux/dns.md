# Quick Start:

[Howto Setup DNS-server on Ubuntu][1]

# Ubuntu DNS server

## nameserver: 127.0.0.53

Check /etc/resolv.conf reset to be nameserver: 127.0.0.53

If I change that to 8.8.8.8 or 208.67.222.222 then everything works. Until I reboot.

Upon reboot or resume, the nameserver is reset to 127.0.0.53.
```sh
    $ cat /etc/resolv.conf
    $ nslookup www.google.com
        Server:     10.0.0.1     <--This is the DNS server address.
        Address:    10.0.0.1#53

        Non-authoritative answer:
        Name:   www.google.com
        Address: 216.58.217.36

    $ dig @172.16.100.100  voip.fortinet.com        <-- force using inner nameserver
```

## DNS by dnsmasq (better)

Easy to setup, please follow the instruction:
https://serverfault.com/questions/429839/assign-multiple-ips-to-1-entry-in-hosts-file

1. install dnsmasq
2. edit /etc/resolv.conf and set "nameserver 127.0.0.1" as a first DNS
3. add normal DNS as alternative (google one for example) "nameserver 8.8.8.8" as a second line
4. make sure two required records are in your /etc/hosts file
5. now check with a command `host abc.efg.datastore.com`

That should respond two records with RR-DNS so if one node from the list is down - your application will be connected to another one

## DNS by resolvconf

    $ sudo apt install resolvconf

Then you can then create or modify files:

    `/etc/resolvconf/resolv.conf.d/head`
    `/etc/resolvconf/resolv.conf.d/tail`

    options rotate
    options timeout:2
    nameserver 8.8.8.8
    nameserver 172.16.100.100
    nameserver 172.16.100.80
    nameserver 127.0.0.53

    $ sudo resolvconf -u        <=== update immediately

# Enforce Safe-Search

https://support.opendns.com/hc/en-us/articles/227986807-How-to-Enforcing-Google-SafeSearch-YouTube-and-Bing<Paste>

# DNS cache

https://www.keycdn.com/support/dns-cache

DNS cache is a very efficient way to avoid having to complete an entire DNS lookup each time you visit a site.
Instead, this process will only need to occur the first time you visit the site and upon subsequent requests,
    your machine will use the OS's and browser's cached DNS information until it expires or is flushed.

## OS-level

- Linux have no OS-level DNS caching
- Windows have OS-level DSN cache: ipconfig /displaydns
- Mac have cache

## Browser level

- Chrome:
    Input "chrome://net-internals/#dns" into your address bar,
    The browser will list current list of cached DNS records.


## check TTL of host
```sh
    $ dig a www.youtube.com

        ;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 17463
        ;; Flags: qr rd ra; QUERY: 1; ANSWER: 6; AUTHORITY: 4; ADDITIONAL: 8

        ;; QUESTION SECTION:
        ;; www.youtube.com.     0       IN      A

        ;; ANSWER SECTION:
        www.youtube.com.        19202   IN      CNAME   youtube-ui.l.google.com.    <=== Time To Live (TTL)
        youtube-ui.l.google.com.        25      IN      A       172.217.14.206
        youtube-ui.l.google.com.        25      IN      A       172.217.14.238



    $ host -a www.youtube.com

        Trying "www.youtube.com"
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46392
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 8

        ;; QUESTION SECTION:
        ;www.youtube.com.               IN      ANY

        ;; ANSWER SECTION:
        www.youtube.com.        18560   IN      CNAME   youtube-ui.l.google.com.

        ;; AUTHORITY SECTION:
        youtube.com.            18516   IN      NS      ns2.google.com.
        youtube.com.            18516   IN      NS      ns4.google.com.
```
## Flush

https://documentation.cpanel.net/display/CKB/How+To+Clear+Your+DNS+Cache

- Windows - command: ipconfig /flushdns
- Mac - sudo killall -HUP mDNSResponder
- clear the DNS cache in Chrome browsers, input "chrome://net-internals/#dns" and click the 'Clear Host Cache' button.

# Useful command:

  [1]: http://mixeduperic.com/ubuntu/seven-easy-steps-to-setting-up-an-interal-dns-server-on-ubuntu.html
