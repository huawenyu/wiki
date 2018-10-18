
## IPAddress int to string, also backward

Python 3 has ipaddress module which features very simple conversion:
```python
import ipaddress

int(ipaddress.IPv4Address("192.168.0.1"))
str(ipaddress.IPv4Address(3232235521))
```

