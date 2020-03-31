# HTTP status code

## An overview of 301, 302 and 307

https://stackoverflow.com/questions/42136829/whats-the-difference-between-http-301-and-308-status-codes
https://airbrake.io/blog/http-errors/308-permanent-redirect

Th status code 307 is similar to 301 (Moved Permanently), except that it does not allow changing the request method from POST to GET.
  - 301 Moved Permanently: The resource has been permanently moved and request method conversion from POST to GET is allowed.
  - 307 Temporary Redirect: The resource has been temporarily moved and request method conversion from POST to GET is forbidden.
  - 302 Found: The resource has been temporarily moved and request method conversion from POST to GET is allowed.
As you can see, this set of three HTTP status codes is missing a code that indicates a permanent redirect that forbids POST to GET conversion.
This is the exact role that the 308 Permanent Redirect status code fulfills.

