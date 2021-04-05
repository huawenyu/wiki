# troubleshooting
https://unix.stackexchange.com/questions/124942/rsyslog-not-logging
https://www.rsyslog.com/doc/master/troubleshooting/troubleshoot.html

## version

	$ rsyslogd -version

## Debugging logger

	$ logger -s "hi"
	saml: hi

## validate your configuration file

	$ sudo rsyslogd -N6 | head -10

	To check a full rsyslog configuration, run rsyslog interactively as follows:
	$ rsyslogd -f /path/to/config-file -N1

## Turn up rsyslogd debugging

	$ sudo -i
	# export RSYSLOG_DEBUGLOG="/tmp/debuglog"
	# export RSYSLOG_DEBUG="Debug"

	# service rsyslog stop
	# rsyslogd -d | head -10

## run rsyslog in interactively mode:

    $ sudo /usr/sbin/rsyslogd -n

## Checking Connection Problems

With netcat, you can test UDP and TCP syslog connections, but not TLS.

### check network data

    sudo netstat -taupn | grep syslog
    sudo tcpdump -i lo -A udp and port 514

### check the rsyslog server

    $ systemctl disable rsyslog.service
    $ systemctl stop rsyslog.service

    $ nc -k -l <ip-of-server> 13515 # [FOR TCP]
    $ nc -u -l <ip-of-server> 13515 # [FOR UDP]

### check the syslog client

    $ echo "test message 1" | nc <ip-of-server> 13515 # [FOR TCP]
    $ echo "test message 1" | nc <ip-of-server> 13515 # [FOR UDP]

