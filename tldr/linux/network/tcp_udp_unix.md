## stream vs data-gram

- If message boundaries are important, then SOCK_DGRAM would be the best choice.
    Because recvfrom/recvmsg/select will return when a complete message is received.
- With SOCK_STREAM, message receiving is more tricky:
    One receiving call may return a partial message, or part of two messages, or several messages... etc.
- If message boundaries are not important, then SOCK_STREAM could be the best choice.
- SOCK_DGRAM of AF_INET is unreliable UDP.
    But, in most sytems, SOCK_DGRAM of AF_UNIX is reliable.
    For example: If queue of receiver is full, sender will be blocked until there is space.

### tcp vs udp:

TCP - stream-oriented, requires a connection, reliable, slow
UDP - message-oriented, connectionless, unreliable, fast

- connect
- data sequence
- delivery reliability (windows/re-transmission/acknowledge)
- error check:
  + udp: has basic error-check like checksum, The integrity is guaranteed only on the single datagram.
- boundaries,
- speed,
- broadcasting,
- sample:
  + udp:
    - It's generally used for real time communication,
    - the packet delay is more serious than packet loss.
    - like video/audio, dns,voip,
  + tcp: http,smtp,pop,ftp,ssh,telnet
