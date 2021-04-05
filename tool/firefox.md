# Let browser ignore the invalid ssl-certificates

## [works] Opera

Change opera run-cmd from:
    opera %U
<to>
    opera --ignore-certificate-errors %U

## [Not work] Firefox ignore invalid ssl-certificates

https://stackoverflow.com/questions/20088/is-there-a-way-to-make-firefox-ignore-invalid-ssl-certificates

I ran into this issue when trying to get to one of my companies intranet sites. Here is the solution I used:

 - enter about:config into the firefox address bar and agree to continue.
 - search for the preference named security.ssl.enable_ocsp_stapling.
 - double-click this item to change its value to false.

This will lower your security as you will be able to view sites with invalid certs. Firefox
will still prompt you that the cert is invalid and you have the choice to proceed forward,
so it was worth the risk for me.

## [Stricter addons] Firefox privacy & addons

https://www.privacytools.io/browsers/#addons

# Disabne HSTS in firefox

https://security.stackexchange.com/questions/102279/can-hsts-be-disabled-in-firefox

Type about:support in firefox
Click Profile Folder | Open Folder which should open your profile folder.
Find file called SiteSecurityServiceState.txt and open it
Find the entry for your site url and remove it. Entry would looks something like - github.com:HSTS  120 17242   1521194647604,1,1
Make sure for above firefox is closed so that it does not overwrite it.
Firefox stores HSTS entries in this file with their expiration periods. Removing this entry should allow you to hit http url. TO further prevent it you can probably change permission of this file to read only.

More details - Understanding HTTP Strict Transport Security (HSTS)

NOTE : This will not work for well known sites like google as those lists are preloaded by browsers. Works fine for others. See above link for details.

# Start multiple firefox with different mode/account

1. private

Change firefox icon, edit it's command from "firefox %u" to "firefox -private %u"

2. open another firefix at normal mode as test client

Change the command from "firefox %u" to "firefox -P test"

# 

