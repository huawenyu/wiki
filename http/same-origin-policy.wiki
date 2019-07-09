# Doc
[whitepaper](https://www.netsparker.com/whitepaper-same-origin-policy/)
[wiki](https://en.wikipedia.org/wiki/Same-origin_policy)
[Just client-side policy](https://softwareengineering.stackexchange.com/questions/216605/how-do-web-servers-enforce-the-same-origin-policy)

    The same origin policy is a wholly client-based restriction, and is primarily engineered to protect *users*, not *services*. All or most browsers include a command-line switch or configuration option to to turn it off. The SOP is like seat belts in a car: they protect the rider in the car, but anyone can freely choose not to use them. *Certainly* don't expect a person's seat belt to stop them from getting out of their car and attacking you (or accessing your Web service).

    Suppose I write a program that accesses your Web service. It's just a program that sends TCP messages that include HTTP requests. You're asking for a server-side mechanism to distinguish between requests made by my program (which can send anything) and requests made by a browser that has a page loaded from a permitted origin. It simply can't be done; my program can always send a request identical to one formed by a Web page.

    The same-origin policy was invented because it prevents code from one website from accessing *credential-restricted content* on another site. Ajax requests are by default sent with
    any auth cookies granted by the target site. For example, suppose I accidentally load `http://evil.com/`, which sends a request for `http://mail.google.com/`. If the SOP were not
    in place, and I was signed into Gmail, the script at `evil.com` could see my inbox. If the site at `evil.com` wants to load `mail.google.com` without my cookies, it can just use a
    proxy server; the public contents of `mail.google.com` are not a secret (but the contents of `mail.google.com` when accessed with my cookies *are* a secret).

## cross-origin requests

[cross-origin requests](https://www.w3.org/TR/access-control/#user-agent-security)
This document defines a mechanism to enable client-side cross-origin requests.
Specifications that enable an API to make cross-origin requests to resources can use the algorithms defined by this specification.
If such an API is used on http://example.org resources,
a resource on http://hello-world.example can opt in using the mechanism described by this specification
(e.g., specifying Access-Control-Allow-Origin: http://example.org as response header),
which would allow that resource to be fetched cross-origin from http://example.org.

## Why we need it

https://security.stackexchange.com/questions/8264/why-is-the-same-origin-policy-so-important
https://stackoverflow.com/questions/3076414/ways-to-circumvent-the-same-origin-policy

# config

## firefox

about:config -> security.fileuri.strict_origin_policy -> false
