# options
    -k, https
    -v, verbose
    -o, output to file
    --limit-rate,  Example: curl -k -o /dev/null --limit-rate 8b www.tired.com
    --speed-limit, Example: --speed-limit 100 and it will exit if less than 100 bytes per second are downloaded over a 30 second period.
    -#, --progress-bar, show percentage
    -I, ACTION=HEAD, told server only response headers

# sample

    ### Last long time to get a large file to /dev/null
    curl -o /dev/null -x 10.1.1.123:8080 -U guest:guest --limit-rate 8b http://172.18.2.169/upload/linoxu/debug_out
    curl -I https://www.wellsfargo.com          <<< only reponse the headers
    curl --header "X-MyHeader: 123" www.google.com      <<< add header
    curl http://example.com/first http://example.com/second     <<< pipeline

## statistics

### data + speed

    $ curl -kv -o ~/tmp/log.1 --limit-rate 8b www.tired.com
    100   184  100   184    0     0      8      0  0:00:23  0:00:22  0:00:01     7


    ### headers: total,download,upload,speed,time
    % Total    % Received % Xferd  Average Speed          Time             Curr.
                                   Dload  Upload Total    Current  Left    Speed
    0  151M    0 38608    0     0   9406      0  4:41:43  0:00:04  4:41:39  9287

### % percentage

    -#, --progress-bar
    $ curl -kv -# -o ~/tmp/log.1 --limit-rate 8b www.tired.com
    [##########################                                                37.0%]

## press OK

    $ curl --form upload=@localfilename --form press=OK [URL]

# nice-little-curl-commands

https://isamert.net/2018/03/24/nice-little-curl-commands.html

    $ curl -F'file=@FILENAME' http://0x0.st             <=== share file by filehost-webserver (<512M)
    $ curl -F'url=http://example.com/image.jpg' https://0x0.st

    $ curl ipinfo.io                                    <=== check current pc's public ip & info
