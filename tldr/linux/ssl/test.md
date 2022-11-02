## HTTPS test server that checks client certificates

1. You can use the following URLs to test SSL client authentication:

https://server.cryptomix.com/secure/
https://prod.idrix.eu/secure/
They both use the same configuration: they accept any client certificate and upon success they display the content of various webserver variables like the certificate used and the ciphersuite selected. If the authentication fails, an error is displayed.

2. https://client.badssl.com (part of the badssl.com service) lets you test authentication using client SSL certificates. The client certificate can be downloaded from https://badssl.com/download/.

This server returns 200 OK if the correct client certificate is provided, and 400 Bad Request otherwise.

3. https://drjohnstechtalk.com/blog/2019/06/how-to-test-if-a-web-site-requires-a-client-certificate/
