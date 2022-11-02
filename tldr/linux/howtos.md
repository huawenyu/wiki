# Chrome browser ignore certificate

## Chrome asks for password to unlock keyring on startup
  - add --password-store=basic to skip the anoy-ask-passwd on startup
  - add --ignore-certificate-errors to skip the certificate-error page when test
    Reference from [https://www.technipages.com/google-chrome-bypass-your-connection-is-not-private-message]

From the manpage:
> --password-store=&lt;basic|gnome|kwallet&gt;  
> Set the password store to use. The default is to automatically detect based on the desktop environment. `basic` selects the built in, unencrypted password store. `gnome` selects Gnome keyring. `kwallet` selects (KDE) KWallet. (Note that KWallet may not work reliably outside KDE.)

The easiest way to fix that in the launcher is to copy the `.desktop` file to your home folder and edit it (google chrome users should copy the appropriate file):

Then edit the new file such that the `Exec` line reads like this:

`Exec=chromium --password-store=basic %U`

`cp /usr/share/applications/google-chrome.desktop ~/.local/share/applications`

```shell
    $ cat .local/share/applications/google-chrome.desktop | grep Exec

        Exec=/usr/bin/google-chrome-stable --password-store=basic --ignore-certificate-errors %U
        Exec=/usr/bin/google-chrome-stable
        Exec=/usr/bin/google-chrome-stable --incognito
```

If you have any other Chromium app installed, their `.desktop` files should also be in `~/.local/share/applications`, edit them accordingly.


# Add a new user 'newname' but reuse existed user 'oldname' env

If there have radius authentication, unplug the wire, login to your old local user.

## create a temp user

    $ sudo useradd -G sudo temp        //create a temp user in sudo group
    $ sudo passwd temp                           //create password for temp user

    ### logout any user, or just reboot.
    ### press Ctrl+alt+F2 to switch to tty2, login with user 'temp'.

## replace the user 'newname' env with user 'oldname'

    $ sudo userdel -fr newname          # delete the user with newname first
    $ sudo usermod -l newname oldname   # Change username from old to new
    $ sudo groupmod -n newname oldname  # Change the default groupname
    $ sudo usermod -md /home/newname newname    # this step may take a while, you can stop it by Ctrl+C, as far as I know, it will still work
    $ [optional] sudo usermod -c "New_real_name" newname        # Just to change Display Name

# Peek the output of a running process

## Using strace

    $ sudo strace -p<pid> -s9999 -e write
      (-s9999 avoids having strings truncated to 32 characters, and write the system call that produces output.)
    $ strace -p1234 -e trace= -e write=3        <<<===(a particular file descriptor)
    $ strace -o trace.log                       <<<=== If the output is scrolling by too fast

## Using `tail`

    $ cd /proc/1199

    Then look for the `fd` directory underneath which hold the file-descriptors (0: stdin, 1: stdout, 2: stderr):
    $ cd fd
    $ tail -f 1

