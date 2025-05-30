# Howto

## apt install fail: Certificate verification failed: The certificate is NOT trusted.

sudo apt update
sudo apt install --reinstall ca-certificates
sudo update-ca-certificates

## Enforce ubuntu apt by ipv4

    ### https://www.cyberciti.biz/faq/howto-use-apt-get-with-ipv6-or-ipv4-transport-on-ubuntu-debian/
    sudo apt-get -o Acquire::ForceIPv4=true install pkg
    sudo apt-get -o Acquire::ForceIPv4=true update
    sudo apt-get -o Acquire::ForceIPv4=true upgrade
    sudo apt-get -o Acquire::ForceIPv4=true dist-upgrade
    sudo apt-get -o Acquire::ForceIPv4=true install ksh

## Fix install fail or update fail

    $ sudo -i
    # apt-get clean
    # cd /var/lib/apt
    # mv lists lists.old
    # mkdir -p lists/partial
    # apt-get clean
    # apt-get update

This will rename your "list" folder to "list.old" for backup purposes and then rebuild.

## How to disable network-connectivity-check on linux mint?

    https://unix.stackexchange.com/questions/513043/how-to-disable-network-connectivity-check-on-linux-mint

    ### You can also remove the package network-manager-config-connectivity-ubuntu:
    $ sudo apt purge network-manager-config-connectivity-ubuntu

## Step 1 - Find the version you want**

**`apt policy` or `apt-cache policy`**  (or `apt-cache madison`)

e.g.

    $ sudo apt policy thunderbird
    thunderbird:
      Installed: 1:60.2.1+build1-0ubuntu0.18.04.2
      Candidate: 1:60.2.1+build1-0ubuntu0.18.04.2
      Version table:
     *** 1:60.2.1+build1-0ubuntu0.18.04.2 500
            500 http://au.archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages
            500 http://security.ubuntu.com/ubuntu bionic-security/main amd64 Packages
         1:52.7.0+build1-0ubuntu1 500
            500 http://au.archive.ubuntu.com/ubuntu bionic/main amd64 Packages

So now we know (at this time) we have two versions:

 - `1:60.2.1+build1-0ubuntu0.18.04.2` and
 - `1:52.7.0+build1-0ubuntu1`

The three stars `***` indicates that this is the version *currently installed* as per the "Installed:" line.

## Step 2 - Install another version**

This is easy, just use the syntax **[packagename]=[version]** with `apt install`.

e.g.
```sh
    $ sudo apt install thunderbird=1:52.7.0+build1-0ubuntu1
        Reading package lists... Done
        Building dependency tree
        Reading state information... Done
        Suggested packages:
        thunderbird-gnome-support ttf-lyx
        The following packages will be DOWNGRADED:
        thunderbird
        0 to upgrade, 0 to newly install, 1 to downgrade, 0 to remove and 12 not to upgrade.
        Need to get 46.5 MB of archives.
        After this operation, 38.4 MB disk space will be freed.
        Do you want to continue? [Y/n]
```

Note the **warning** that the package will be **DOWNGRADED**

## Bonus step - lock in that version**  (a.k.a. **apt-mark hold**)

If you want to stop `apt upgrade` from upgrading the package again, then you can tell apt to **hold** a package.

e.g.

    $ sudo apt-mark hold thunderbird
    thunderbird set on hold.

So now, when you `apt upgrade` you'll get a warning that packages have been **kept back**.  e.g.

    $ sudo apt upgrade
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    Calculating upgrade... Done
    The following packages have been kept back:
      thunderbird
    0 to upgrade, 0 to newly install, 0 to remove and 1 not to upgrade.

When you are comfortable upgrading again, then you can release the hold:

    $ sudo apt-mark unhold thunderbird
    Cancelled hold on thunderbird.

e voila, the latest release is now the default again:

    $ sudo apt upgrade
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    Calculating upgrade... Done
    The following packages will be upgraded:
      thunderbird
    1 to upgrade, 0 to newly install, 0 to remove and 0 not to upgrade.
    Need to get 41.1 MB of archives.
    After this operation, 38.4 MB of additional disk space will be used.
    Do you want to continue? [Y/n]

You could also have gone with **apt pinning** and the `/etc/apt/preferences` file but *hold*ing is much easier for this task!

