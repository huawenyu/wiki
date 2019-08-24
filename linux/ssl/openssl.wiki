# docs

[openssl-cookbook](https://www.feistyduck.com/library/openssl-cookbook/online/ch-openssl.html)
    - https://www.feistyduck.com/library/openssl-cookbook/online/ch-openssl.html#
    - https://www.feistyduck.com/library/openssl-cookbook/online/ch-testing-with-openssl.html#testing-heartbleed

https://home.mpcdf.mpg.de/~jkennedy/2017/09/01/tools-for-testing-https-connections.html

# Install openssl 1.1.1a

According to the [OpenSSL website](https://www.openssl.org/source/):

> The latest stable version is the 1.1.1 series. This is also our Long Term Support (LTS) version, supported until 11th September 2023.

Since this is not in the current Ubuntu repositories, you will need to download, compile, and install the latest OpenSSL version manually.

Below are the instructions to follow:

1. Open a terminal (<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>t</kbd>).
2. Fetch the tarball: `wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz`
3. Unpack the tarball with `tar -zxf openssl-1.1.1a.tar.gz && cd openssl-1.1.1a`
4. Issue the command `./config`.
5. `sudo apt install build-essential && make`
6. Run `make test` to check for possible errors.
7. Backup current openssl binary: `sudo mv /usr/bin/openssl ~/tmp`
8. Issue the command `sudo make install`.
9. Create symbolic link from newly install binary to the default location:
    ```
    sudo ln -s /usr/local/bin/openssl /usr/bin/openssl
    ```
10. Run the command `sudo ldconfig` to update symlinks and rebuild the library cache.
11. Check version:
    $ openssl version
    OpenSSL 1.1.1a  20 Nov 2018

# curl with TLSv1.3

    $ brew install openssl@1.1
    ### and also openssl 1.0.2l with
    $ brew install openssl

    ### after install of curl with brew install curl it uses openssl 1.0.2l
    $ brew install curl

    ### How can one install curl with openssl@1.1 ?
    ###   Until we decide to use openssl@1.1 for curl, you can:
    $ brew install DomT4/crypto/curl-max

# TSL protocol

http://blog.fourthbit.com/2014/12/23/traffic-analysis-of-an-ssl-slash-tls-session
  http://www.ntu.edu.sg/home/ehchua/programming/webprogramming/http_ssl.html

The higher layer is stacked on top of the SSL Record Protocol, and comprises four subprotocols.
Each of these protocols has a very specific purpose, and are used at different stages of the communication:
- Handshake Protocol: It allows the peers to authenticate each other and to negotiate a cipher suite and other parameters of the connection. The SSL handshake protocol involves four sets of messages (sometimes called flights) that are exchanged between the client and server. Each set is typically transmitted in a separate TCP segment. The following diagram shows a summary of the process, which has several steps and offers optional ones. Please note that ChangeCipherSpec messages don’t belong to this protocol, as they are a protocol by themselves, as seen below.
```text
               TLS Handshake

               +-----+                              +-----+
               |     |                              |     |
               |     |        ClientHello           |     |
               |     o----------------------------> |     |
               |     |                              |     |
       CLIENT  |     |        ServerHello           |     |  SERVER
               |     |       [Certificate]          |     |
               |     |    [ServerKeyExchange]       |     |
               |     |    [CertificateRequest]      |     |
               |     |      ServerHelloDone         |     |
               |     | <----------------------------o     |
               |     |                              |     |
               |     |       [Certificate]          |     |
               |     |     ClientKeyExchange        |     |
               |     |    [CertificateVerify]       |     |
               |     |   ** ChangeCipherSpec **     |     |
               |     |         Finished             |     |
               |     o----------------------------> |     |
               |     |                              |     |
               |     |   ** ChangeCipherSpec **     |     |
               |     |         Finished             |     |
               |     | <----------------------------o     |
               |     |                              |     |
               +-----+                              +-----+



     Optional messages
     -----------------
      - Certificate (server)     needed with all key exchange algorithms, except for anonymous ones.
      - ServerKeyExchange        needed in some cases, like Diffie-Hellman key exchange algorithm.
      - CertificateRequest       needed if Client authentication is required.
      - Certificate (client)     needed in response to CertificateRequest by the server.
      - CertificateVerify        needed if client Certificate message was sent.
```

- ChangeCipherSpec Protocol: It makes the previously negotiated parameters effective, so communication becomes encrypted.
- Alert Protocol: Used for communicating exceptions and indicate potential problems that may compromise security.
- Application Data Protocol: It takes arbitrary data (application-layer data generally), and feeds it through the secure channel.

# apache conf

## ciphers suggests

https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/

The following configuration is (or used to be) the best configuration according to SSLLabs:

```
    SSLProtocol +TLSv1.2 +TLSv1.1 +TLSv1
    SSLCompression off
    SSLHonorCipherOrder on
    SSLCipherSuite "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA"
```

Add above to the config file:

`/etc/apache2/conf-available/default-ssl.conf`

# openssl tools

http://www.taddong.com/en/lab.html#TLSSLED

## list the SSL/TLS cipher suites of a website offers
https://superuser.com/questions/109213/how-do-i-list-the-ssl-tls-cipher-suites-a-particular-website-offers

### script/test_ciphers.sh

### Nmap with ssl-enum-ciphers

```
    ### Using buildin feature
    nmap --script ssl-cert,ssl-enum-ciphers -p 443 secure.m2osw.com


    ### Usging script
    $ cd wiki/linux/ssl

    ### List ciphers supported by an HTTP server
    $ nmap --script ssl-enum-ciphers -p 443 www.example.com

    ### List ciphers supported by an IMAP server
    $ nmap --script ssl-enum-ciphers -p 993 mail.example.com

    Here is a snippet of output from a Dovecot IMAP server:

    993/tcp open  imaps
    | ssl-enum-ciphers:
    |   SSLv3:
    |     ciphers:
    |       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA - strong
    |       TLS_DHE_RSA_WITH_AES_128_CBC_SHA - strong
    |       TLS_DHE_RSA_WITH_AES_256_CBC_SHA - strong
    |       TLS_RSA_WITH_IDEA_CBC_SHA - weak
    ...
    |   TLSv1.0:
    |     ciphers:
    |       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA - strong
    |       TLS_DHE_RSA_WITH_AES_128_CBC_SHA - strong
    |       TLS_DHE_RSA_WITH_AES_256_CBC_SHA - strong
    |       TLS_RSA_WITH_IDEA_CBC_SHA - weak
    ...
    |_  least strength: weak

    Nmap done: 1 IP address (1 host up) scanned in 1.03 seconds
```

### sslscan www.google.com

## commands

### General OpenSSL Commands
These commands allow you to generate CSRs, Certificates, Private Keys and do other miscellaneous tasks.

    === Generate a new private key and Certificate Signing Request
    $ openssl req -out CSR.csr -new -newkey rsa:2048 -nodes -keyout privateKey.key

    === Generate a self-signed certificate (see How to Create and Install an Apache Self Signed Certificate for more info)
    $ openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt

    === Generate a certificate signing request (CSR) for an existing private key
    $ openssl req -out CSR.csr -key privateKey.key -new

    === Generate a certificate signing request based on an existing certificate
    $ openssl x509 -x509toreq -in certificate.crt -out CSR.csr -signkey privateKey.key
    === Remove a passphrase from a private key
    $ openssl rsa -in privateKey.pem -out newPrivateKey.pem

### Checking Using OpenSSL
    If you need to check the information within a Certificate, CSR or Private Key, use these commands. You can also check CSRs and check certificates using our online tools.

    === Check a Certificate Signing Request (CSR)
    $ openssl req -text -noout -verify -in CSR.csr

    === Check a private key
    $ openssl rsa -in privateKey.key -check

    === Check a certificate
    $ openssl x509 -in certificate.crt -text -noout

    === Check a PKCS#12 file (.pfx or .p12)
    $ openssl pkcs12 -info -in keyStore.p12

### Debugging Using OpenSSL
    If you are receiving an error that the private doesn't match the certificate or that a certificate that you installed to a site is not trusted, try one of these commands. If you are trying to verify that an SSL certificate is installed correctly, be sure to check out the SSL Checker.

    === Check an MD5 hash of the public key to ensure that it matches with what is in a CSR or private key
    $ openssl x509 -noout -modulus -in certificate.crt | openssl md5
    $ openssl rsa -noout -modulus -in privateKey.key | openssl md5
    $ openssl req -noout -modulus -in CSR.csr | openssl md5

    === Check an SSL connection. All the certificates (including Intermediates) should be displayed
    $ openssl s_client -connect www.paypal.com:443

### Converting Using OpenSSL
    These commands allow you to convert certificates and keys to different formats to make them compatible with specific types of servers or software. For example, you can convert a normal PEM file that would work with Apache to a PFX (PKCS#12) file and use it with Tomcat or IIS. Use our SSL Converter to convert certificates without messing with OpenSSL.

    === Convert a DER file (.crt .cer .der) to PEM
    $ openssl x509 -inform der -in certificate.cer -out certificate.pem

    === Convert a PEM file to DER
    $ openssl x509 -outform der -in certificate.pem -out certificate.der

    === Convert a PKCS#12 file (.pfx .p12) containing a private key and certificates to PEM
    $ openssl pkcs12 -in keyStore.pfx -out keyStore.pem -nodes
    You can add -nocerts to only output the private key or add -nokeys to only output the certificates.

    === Convert a PEM certificate file and a private key to PKCS#12 (.pfx .p12)
    $ openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile CACert.crt

## curl

    $ curl --cert certificate_file.pem:password https://www.example.com/some_protected_page

## s_client

### Displaying a remote SSL certificate details

    $ echo | openssl s_client -showcerts -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -inform pem -noout -text

    $ openssl s_client -connect test.example.com:443 -servername example.com
    $ openssl s_client -connect test.example.com:443 -ssl3
    $ openssl s_client -connect test.example.com:443 -tls1
    $ openssl s_client -connect test.example.com:443 -tls1_1
    $ openssl s_client -connect test.example.com:443 -tls1_2

### Test different protocols

    $ openssl s_client -connect server.yourwebhoster.eu:21 -starttls ftp      <<< Test FTP certificate
    $ openssl s_client -connect server.yourwebhoster.eu:995                   <<< Test POP3 certificate
    $ openssl s_client -connect server.yourwebhoster.eu:993                   <<< Test IMAP certificate
    $ openssl s_client -connect server.yourwebhoster.eu:465                   <<< Test SMTP SSL certificate
    $ openssl s_client -connect server.yourwebhoster.eu:587 -starttls smtp    <<< Test SMTP TLS certificate
    $ openssl s_client -connect server.yourwebhoster.eu:443                   <<< Test HTTPS certificate
    $ openssl s_client -connect server.yourwebhoster.eu:2222                  <<< Test DirectAdmin certificate

### protocol: https
    $ openssl s_client -quiet -connect example.com:443
        < (...some certificate debugging will be displayed here...)
        < (...after that, use the normal commands you would use in a telnet connection to port 80...)
        user > GET / HTTP/1.1
        user > Host: example.com

### protocol: SSMTP / SMTPS
    $ openssl s_client -quiet -connect mail.yourserver.tld:485
        < (...some certificate debugging will be displayed here...)
        < (...after that, use the normal commands you would use in a telnet connection to port 25...)
        < 220 mail.yourserver.tld
        user > HELO your-name

        < 250 remote-server
        user > MAIL FROM:<me@example.com>

        < 250 2.1.0 Ok
        user > RCPT TO:<tch@example.com>

    Or, to test TLS on port 25:
    $ openssl s_client -quiet -starttls smtp -connect mail.yourserver.tld:25

### protocol: IMAP

Note the "-starttls imap" added to the command line - this one shows an expired certificate:

    $ openssl s_client -quiet -starttls imap -connect mail.yourserver.tld:143
        depth=2 O = Digital Signature Trust Co., CN = DST Root CA X3
        verify return:1
        depth=1 C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3
        verify return:1
        depth=0 CN = mail.yourserver.tld
        verify error:num=10:certificate has expired
        notAfter=Sep 21 09:07:00 2016 GMT
        verify return:1
        depth=0 CN = mail.yourserver.tld
        notAfter=Sep 21 09:07:00 2016 GMT
        verify return:1
        . OK Completed

## x509: validate the certs

    $ echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates
        notBefore=Feb 14 00:00:00 2017 GMT
        notAfter=Feb 14 23:59:59 2018 GMT

