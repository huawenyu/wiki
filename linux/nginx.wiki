# Doc

# Quick Start

     nginx -V
        nginx version: nginx/1.14.0 (Ubuntu)
        built with OpenSSL 1.1.1  11 Sep 2018 (running with OpenSSL 1.1.0g  2 Nov 2017)
        TLS SNI support enabled
        configure arguments:
          --prefix=/usr/share/nginx
          --conf-path=/etc/nginx/nginx.conf             <=== config
          --http-log-path=/var/log/nginx/access.log
          --error-log-path=/var/log/nginx/error.log
          --lock-path=/var/lock/nginx.lock
          --pid-path=/run/nginx.pid

    service nginx -v    <=== check version
    service nginx -V

    service nginx -h    <=== help
    service nginx -?
    service nginx status         <=== check status

    nginx -t                    <=== run config test
    service nginx configtest

    service nginx start
    service nginx stop           <=== Gracefully close
    killall -9 nginx
    service nginx quit

    service nginx restart
    service nginx reload        <=== more Gracefully close the old worker, and use the new config to start a new worker

    nginx -s signal
    Where signal may be one of the following:
      - stop — fast shutdown
      - quit — graceful shutdown
      - reload — reloading the configuration file
      - reopen — reopening the log files


## Config

    [How to Configure NGINX](https://www.linode.com/docs/web-servers/nginx/how-to-configure-nginx/)
    [Beginner’s Guide](http://nginx.org/en/docs/beginners_guide.html)

```conf
    $ cat /etc/nginx/sites-enabled/default

    # Default server configuration
    #
    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            root /var/www/html;

            # Add index.php to the list if you are using PHP
            index index.html index.htm index.nginx-debian.html;

            server_name _;

            location / {
                    # First attempt to serve request as file, then
                    # as directory, then fall back to displaying a 404.
                    try_files $uri $uri/ =404;
            }
    }
```
## web host dir:
   $ uname -a
   Linux VAN-200912-PC6 4.15.0-20-generic #21-Ubuntu SMP Tue Apr 24 06:16:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

   [Linuxmint 19]: `/var/www/html`, also we can verify from the above config file.
   There have another dir: /usr/share/nginx/html, but it not the real dir.


## service vs systemctl

`service` is an "high-level" command used for starting and stopping services in different unixes and linuxes.
Depending on the "lower-level" service manager, service redirects on different binaries.  For example,
  - on CentOS 7 it redirects to systemctl,
  - while on CentOS 6 it directly calls the relative /etc/init.d script.
  - On the other hand, in older Ubuntu releases it redirects to upstart.

`service` is adequate for basic service management, while directly calling `systemctl` give greater control options.

The `service` command is a wrapper script that allows system administrators to start, stop, and check the status of services
  without worrying too much about the actual init system being used.

Prior to systemd's introduction, it was a `wrapper` for `/etc/init.d scripts` and `Upstart's initctl` command,
      and now it is a wrapper for these two and `systemctl` as well.

# Install

## method-1. apt install nginx

## method-2. Build our own `Formula` for brew

We can build from an existed tap.
For example, we can build our own Formula of nginx debug version.

1. build our own tap
    - Git clone https://github.com/denji/homebrew-nginx our own tap.
    - Install the tap into local brew.
        $ brew tap huawenyu/nginx
        Usually it path: /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/huawenyu/homebrew-nginx

2. Clone a basic nginx build from homebrew-core into our own tap
    - brew edit nginx       <--- homebrew-core's nginx
      Found it's path: /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/nginx.rb

    - brew edit huawenyu/nginx/nginx-full  <--- our own nginx version, but it's too full, we need basic version here.
      Found it's path: /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/huawenyu/homebrew-nginx/Formula/nginx-full.rb

    - copy to our own dir and push back to github:
      $ cp /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/{homebrew/homebrew-core,huawenyu/homebrew-nginx}/Formula/nginx.rb
      $ cd /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/huawenyu/homebrew-nginx
      $ git add Formula/nginx.rb

3. Check & Verify:
    $ brew search nginx
        huawenyu/nginx/nginx    <-- new added formula
    $ brew install huawenyu/nginx/nginx
        Docroot is: `/home/linuxbrew/.linuxbrew/var/www`

        The default port has been set in `/home/linuxbrew/.linuxbrew/etc/nginx/nginx.conf to 8080` so that
        nginx can run without sudo.

        nginx will load all files in `/home/linuxbrew/.linuxbrew/etc/nginx/servers/`.

        Warning: nginx provides a launchd plist which can only be used on macOS!
        You can manually execute the service instead with:
          nginx

    $ which nginx
        /home/linuxbrew/.linuxbrew/bin/nginx
    $ nginx     <-- run nginx
    $ ps -ef|grep nginx
        hyu      29431     1  0 10:12 ?        00:00:00 nginx: master process nginx
        hyu      29432 29431  0 10:12 ?        00:00:00 nginx: worker process

    $ curl http://localhost:8080/   <-- try to access it

        <p><em>Thank you for using nginx.</em></p>

## How to submit a new formula

* Fork this repository on GitHub.
* Clone to your Mac.
* Read and look at the other formule here.
* In your locally cloned `homebrew-nginx` repo, create a new branch: `git checkout --branch my_new_formula`
* Write/edit your formula (ruby file). Check [Homebrew's documentation](https://github.com/Homebrew/brew/blob/master/docs/README.md) for details.
* Test it locally! `brew install ./my-new-formula.rb`. Does it install? Note, `./<formula>.rb` will target the local file.
* `git push --set-upstream origin my-new-formula` to get it into your GitHub fork as a new branch.
* If you have to change something, add a commit and `git push`.
* On GitHub, select your new branch and then click the "Pull Request" button.

