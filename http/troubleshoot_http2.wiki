# Chrome

## Install chrome-dev version (alongside the stable version)

https://developers.google.com/web/updates/2017/04/headless-chrome

    --proxy-server="https://206.246.75.178:3129"
        [<proxy-scheme>://]<proxy-host>[:<proxy-port>]
        <proxy-scheme> is the protocol of the proxy server:
            "http", "socks", "socks4", "socks5".

    --headless --disable-gpu
    --remote-debugging-port=9222
    --force-device-scale-factor=1
    --no-first-run
    --no-default-browser-check,
    --no-sandbox http://www.chromestatus.com

    --net-log-capture-mode=IncludeCookiesAndCredentials
    --net-log-capture-mode=IncludeSocketBytes

```sh
#!/bin/bash
# 1. Download deb package
#   - Download the deb package directly from: https://www.google.com/chrome/dev/
#   - Unpack it (ar xo /path/to/file.deb)
#   - Unpack the data.tar.xz (tar -xvf ...)
#   - Run opt/google/chrome/google-chrome
# 2. About flags:
#    http://www.chromium.org/developers/how-tos/run-chromium-with-flags
#     --remote-debugging-port=9222
~/Downloads/chrome/opt/google/chrome-unstable/google-chrome-unstable \
        --allow-insecure-localhost \
        --no-first-run \
        --no-default-browser-check \
        --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir')
```

## Network log

https://textslashplain.com/2020/01/17/capture-network-logs-from-edge-and-chrome/
https://textslashplain.com/2020/04/08/analyzing-network-traffic-logs-netlog-json/


Chrome-Address: chrome://net-internals/#hsts

### Capture Network Logs
https://www.chromium.org/for-testers/providing-network-details

    - Optional but helpful: Close all browser tabs but one.
    - Navigate the tab to chrome://net-export
    - In the UI that appears, press the Start Logging to Disk button.
    - Choose a filename to save the traffic to. Tip: Pick a location you can easily find later, like your Desktop.
    - Reproduce the networking problem in a new tab. If you close or navigate the //net-export tab, the logging will stop automatically.
    - After reproducing the problem, press the Stop Logging button.
    - Share the Net-Export-Log.json file with whomever will be looking at it. Optional: If the resulting file is very large, you can compress it to a ZIP file.

Or we can run command from command-line with flags:

https://www.chromium.org/for-testers/providing-network-details
https://www.chromium.org/developers/design-documents/network-stack/netlog
https://textslashplain.com/2020/03/25/debugging-proxy-configuration-scripts-in-the-new-edge/

    --net-log-capture-mode=IncludeCookiesAndCredentials
    --net-log-capture-mode=IncludeSocketBytes
    --log-net-log=FILENAME

### Viewer netlog

Upload our network log to here:
https://netlog-viewer.appspot.com/#import

# upgrade

## Http2: h2c

https://stackoverflow.com/questions/46788904/why-do-web-browsers-not-support-h2c-http-2-without-tls

Technically
There are several technical reasons why HTTP/2 is much better and easier to handle over HTTPS:

Doing HTTP/2 negotiation in TLS with ALPN is much easier and doesn't lose round-trips like Upgrade: in plain HTTP does. And it doesn't suffer from the upgrade problem on POST that you get with plain-text HTTP/2.
N% of the web doesn't support unsolicited Upgrade: h2cheaders in requests and instead respond with 400 errors.
Doing something else than HTTP/1.1 over TCP port 80 breaks in Y% of the cases since the world is full of middle-boxes that "help" out and replace/add things in-stream for such connections. If that then isn't HTTP/1.1, things break (this is also why brotli for example also requires HTTPS).
Ideologically
There's a push for more HTTPS on the web that is shared by and worked on in part by some of the larger web browser developer teams. That makes it considered a bonus if features are implemented HTTPS-only as they then work as yet another motivation for sites and services to move over to HTTPS. Thus, some teams never tried very hard (if at all) to make HTTP/2 work without TLS.

Practically
At least one browser vendor expressed its intention early on to implement and provide HTTP/2 for users done over plain-text HTTP (h2c). They ended up never doing this because of technical obstacles as mentioned above.

# Tools

## client:

    $ nghttp -va https://www.facebook.com

