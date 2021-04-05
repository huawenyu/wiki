# Build on ubuntu

https://dev.to/tmidi/getting-started-with-haproxy-install-from-code-source-5c4g

    $ sudo apt install make gcc perl pcre-devel zlib-devel
    $ git clone https://github.com/haproxy/haproxy.git
    $ cd haproxy      +=== check INSTALL
    $ make clean
    $ sudo apt-get install -y liblua5.3-dev
    $ make -j $(nproc) TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_LUA=1 USE_PCRE=1

## Run from command line

https://www.techietown.info/2017/03/startrun-haproxy-in-foreground/

The command line flag “-D” will launch HAproxy in background or as a daemon. When you start
HAproxy using command line options make sure you don’t use the option “D”

In the haproxy configuration file, you will see an option “daemon”, if you keep it commented
HAproxy will not go to daemon mode and start on foreground

Sample config snippet as below

    #/etc/haproxy/haproxy.cfg
    global
    # to have these messages end up in /var/log/haproxy.log you will
    # need to:
    #
    # 1) configure syslog to accept network log events. This is done
    # by adding the ‘-r’ option to the SYSLOGD_OPTIONS in
    # /etc/sysconfig/syslog
    #
    # 2) configure local2 events to go to the /var/log/haproxy.log
    # file. A line like the following can be added to
    # /etc/sysconfig/syslog
    #
    # local2.* /var/log/haproxy.log
    #
    log 127.0.0.1 local2

    chroot /var/lib/haproxy
    pidfile /var/run/haproxy.pid
    maxconn 4000
    user haproxy
    group haproxy
    # daemon


    [root@test.test.com ~]# haproxy -f /etc/haproxy/haproxy.cfg
        [WARNING] 071/085241 (29884) : Server static/static is DOWN, reason: Layer4 connection problem, info: “Connection refused”, check duration: 0ms. 0 active and 0 backup servers left. 0 sessions active, 0 requeued, 0 remaining in queue.
        [ALERT] 071/085241 (29884) : backend ‘static’ has no server available!
        [WARNING] 071/085242 (29884) : Server app/app4 is DOWN, reason: Layer4 connection problem, info: “Connection refused”, check duration: 0ms. 3 active and 0 backup servers left. 0 sessions active, 0 requeued, 0 remaining in queue.

You can see that HAproxy started on foreground and printing debug logs to console.

### Enable log

    $ cd ~/proj/haproxy
    $ cat fwdtestmy.cfg

        global
            daemon
            maxconn 256
            #user        haproxy
            #group       haproxy
            user        hyu
            group       hyu
            #chroot      /var/lib/haproxy
            #local2.*    /var/log/haproxy.log

            # change level to debug, and dump log to rsyslog
            log 127.0.0.1:514 local0 debug
            #log 127.0.0.1:514 local1 warning
            #log stdout  format raw  local0  info
            #daemon

        defaults
            mode http
            log global
            # enable verbose log
            option httplog
            option  tcplog
            option  dontlognull
            timeout connect 5000ms
            timeout client 50000ms
            timeout server 50000ms

        frontend http
            bind *:1080
            http-request capture req.hdr(Host) len 5
            http-request capture req.hdr(User-Agent) len 5
            default_backend servers

        frontend https
            bind *:1443
            http-request capture req.hdr(Host) len 5
            http-request capture req.hdr(User-Agent) len 5
            default_backend servers

        backend servers
            balance roundrobin
            mode http
            option forwardfor
            option httpchk GET /
            server server1  172.16.80.129:80
            #server server2  google.com check
            #server server2 123.123.123.123 check
            #server server3 public.com check

    $ cat /etc/rsyslog.d/haproxy.conf
        $ModLoad imudp
        $UDPServerAddress 127.0.0.1
        $UDPServerRun 514
        $FileCreateMode 0644
        $FileOwner hyu
        # if change the file to /var/log/haproxy.log, it won't works, not check why
        local0.*     /tmp/haproxy.log
        local1.*     /tmp/haproxy_warn.log

### run from command line

    $ cd ~/proj/haproxy
    $ ./haproxy -dV -f ./fwdtestmy.conf

