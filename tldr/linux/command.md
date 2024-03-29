# terminal application

## [great-terminal-replacements-for-gui-applications][5]

# Howtos

## file order-by-size

If you want to find all files in the current directory and its sub directories and list them according to their size (without considering their path), and assuming none of the file names contain newline characters, with GNU `find`, you can do this:

    find . -type f -printf "%s\t%p\n" | sort -n


From `man find` on a GNU system:

       -printf format
              Unlike  -print, -printf  does  not add a newline at the end of
              the string.  The escapes and directives are:

              %p     File's name.
              %s     File's size in bytes.

From `man sort`:

       -n, --numeric-sort
              compare according to string numerical value


## how to disable annoying F1 help

1. Go to System - Preferences - Keyboard Shortcuts
2. Create a new shortcut. Name it 'do nothing', and write 'false' (without quotes) in the "command" field. Push ok.
3. Scroll to the bottom of the list and find your new command. Click on the "Disabled", on the right, and push F1.

Now F1 is linked to /bin/false, a command whose "man false" says: "Do nothing, successfully."

Now no Gnome application (like nautilus) will open the help window ever again when accidentally pushing F1.

## hostname change

    $ sudo hostname new-server-name-here
    $ sudo vi /etc/hostname
    $ sudo vi /etc/hosts
        From:
            127.0.1.1 old-host-name
        To:
            127.0.1.1 new-server-name-here

## sudo & su

The major difference between `sudo and su` is:
  - `sudo` lets you run commands in your own user account with root privileges.
  - `su` lets you switch as another user so that you're actually logged in as root.

sudo   Runs a single command with root privileges. The system prompts you for your current user account's password before running command as the root user.
       By default, Ubuntu remembers the password for fifteen minutes and won't ask for a password again until the fifteen minutes are up.

The major difference between sudo -i and sudo -s is:
  - sudo -i     gives you the root environment, i.e. your ~/.bashrc is ignored.
                Just acquires the root environment, not your env.
  - sudo -s     gives you the user's environment, so your ~/.bashrc is respected.
                Runs a new shell with root privileges, and also with all current user's environment, specially useful when we install and setup a new env.
  - sudo -u Bob whoami   execute a command 'whoami' as another user.

  - su                      switches to the super user – or root user – when you execute it with no additional options. You'll have to enter the root account’s password.
    + su -c 'command'       Run a single command as the root user
    + su - Bob              Start a new shell, and change to another user's environment to check the shell or env setup ok or not.
    + su Bob                You'll be prompted to enter Bob's password and the reuse current shell and also switch to Bob's user account with old env.

### sudo change timeout

    $ sudo visudo

        Defaults env_reset

    ### Change it like this, here as 10 minutes:
        Defaults env_reset, timestamp_timeout=10

    ### After that, press Ctrl+X and followed by Y to save the changes

### sudo with vim

:w !sudo tee %

In above command:

  * Colon (:) indicates we are in Vim’s ex mode
  * w write current file's all lines to the command follow
  * Exclamation (!) mark indicates that we are running shell command
  * sudo and tee are the shell commands, `tee [option] [FILE]`: Copy standard input to each FILE, and also to standard output.
  * Percentage (%) sign indicates current filename

### revoke sudo as soon

Q1: Long story short, how does one run one command in a script with sudo, while then removing the elevated privileges for the rest of the script

You can 'revoke' the sudo permission (actually: close the sudo time window early) by doing:

    sudo -k

Also, you can configure sudo to only allow elevated permissions on certain commands, or even to impersonate non-root for specific commands. See `man sudoers`. The **examples section** makes it exceedingly clear that there is virtually no limit to the configurability of sudo (roles, hosts, commands, allow escaping, allow sudo target users, exceptions to allowed things, password less authorization etc etc).

Hopefully an interesting example in your context:

> The user fred can run commands as any user in the DB Runas_Alias (oracle or sybase) without giving a password.
>
>        fred           ALL = (DB) NOPASSWD: ALL

----

If you can't / don't really want to meddle with /etc/sudoers (visudo!) then I suggest using something like


    {
         trap "sudo -k" EXIT INT QUIT TERM
         sudo ls # whatever
    }

### sudo-command-tips

Overview

sudo stands for superuser do. It allows authorized users to execute command as an another user. Another user can be regular user or superuser. However, most of the time we use it to
execute command with elevated privileges.

sudo command works in conjunction with security policies, default security policy is sudoers and it is configurable via /etc/sudoers file. Its security policies are highly extendable.
One can develop and distribute their own policies as plugins.

#### How it’s different than su

In GNU/Linux there are two ways to run command with elevated privileges:

  * Using su command
  * Using sudo command

su stands for switch user. Using su, we can switch to root user and execute command. But there are few drawbacks with this approach.

  * We need to share root password with another user.
  * We cannot give controlled access as root user is superuser
  * We cannot audit what user is doing.

sudo addresses these problems in unique way.

 1. First of all, we don’t need to compromise root user password. Regular user uses its own password to execute command with elevated privileges.
 2. We can control access of sudo user meaning we can restrict user to execute only certain commands.
 3. In addition to this all activities of sudo user are logged hence we can always audit what actions were done. On Debian based GNU/Linux all activities are logged in /var/log/auth.log
    file.

Later sections of this tutorial sheds light on these points.

#### Hands on with sudo

##### Allow sudo access

Let us add regular user as a sudo user. In my case user’s name is linuxtechi

    1) Edit /etc/sudoers file as follows:

        $ sudo visudo

    2) Add below line to allow sudo access to user linuxtechi:

        <your-user-name> ALL=(ALL) ALL

        In above command:

          * linuxtechi indicates user name
          * First ALL instructs to permit sudo access from any terminal/machine
          * Second (ALL) instructs sudo command to be allowed to execute as any user
          * Third ALL indicates all command can be executed as root


    $ sudo cat /etc/passwd

    When you execute this command, it will ask linuxtechi’s password and not root user password.

##### Execute command as an another user

In addition to this we can use sudo to execute command as another user. For instance, in below command, user linuxtechi executes command as a devesh user:

    $ sudo -u devesh whoami
    [sudo] password for linuxtechi:
    devesh

    $ sudo bash

    After executing this command – you will observe that prompt sign changes to pound (#) character.

##### Execute multiple commands using sudo

So far we have executed only single command with sudo but we can execute multiple commands with it. Just separate commands using semicolon (;) as follows:

$ sudo -- bash -c 'pwd; hostname; whoami'

In above command:

  * Double hyphen (&#8211;) stops processing of command line switches
  * bash indicates shell name to be used for execution
  * Commands to be executed are followed by –c option

##### Run sudo command without password

When sudo command is executed first time then it will prompt for password and by default password will be cached for next 15 minutes. However, we can override this behavior and disable
password authentication using NOPASSWD keyword as follows:

    linuxtechi ALL=(ALL) NOPASSWD: ALL

##### Restrict user to execute certain commands

To provide controlled access we can restrict sudo user to execute only certain commands. For instance, below line allows execution of echo and ls commands only

    linuxtechi ALL=(ALL) NOPASSWD: /bin/echo /bin/ls

Insights about sudo

Let us dig more about sudo command to get insights about it.

$ ls -l /usr/bin/sudo
-rwsr-xr-x 1 root root 145040 Jun 13  2017 /usr/bin/sudo

If you observe file permissions carefully, setuid bit is enabled on sudo. When any user runs this binary it will run with the privileges of the user that owns the file. In this case it
is root user.

To demonstrate this, we can use id command with it as follows:

$ id
uid=1002(linuxtechi) gid=1002(linuxtechi) groups=1002(linuxtechi)

When we execute id command without sudo then id of user linuxtechi will be displayed.

$ sudo id
uid=0(root) gid=0(root) groups=0(root)

But if we execute id command with sudo then id of root user will be displayed.

## file & dir's space & size

### free disk space

1. check core dump

    $ find / -xdev -name core -ls -o  -path "/lib*" -prune

2. find which file|dir take the space

    $ sudo du -hsx /home/* | sort -rh | head -n 10
    $ sudo du -hsx --max-depth=1 /home/* | sort -rh | head -n 10

### current dir size
    du -hsc .

## User management

```sh
    # create a user
    USERNAME=foo
    $ useradd $USERNAME

    # reset password
    USERNAME=foo
    $ passwd $USERNAME

    # add an existing user to a group
    USERNAME=foo
    GROUP=www
    $ usermod -a -G $GROUP $USERNAME
    $ cat /user/group

    # remove user
    USERNAME=foo
    $ userdel $USERNAME

    # add a user to a group
    USERNAME=foo
    GROUP=www-data
    $ usermod -a -G $GROUP $USERNAME
```

## clean logfile

Clean logfile which come from `plink -telnet 127.0.0.1 | tee log.file`

    # Removing non printable characters
    $ tr -dc '[:print:]\n' < log.file
       -c, -C, --complement
              use the complement of SET1

       -d, --delete
              delete characters in SET1, do not translate

    # also remove escape sequences as well
    $ sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"

## Test Internet speed
### Download speed

    lftp -e `pget http://example.com/file.iso; exit;`

### Upload speed

    lftp -u userName ftp.example.com -e `put largecd1.avi; bye`

### Get network throughput rate:

    iperf -s -B serverIP
    iperf -c serverIP -d -t 60 -i 10

## ssh with password

    $ sudo apt-get install sshpass
    $ sshpass -p your_password ssh user@hostname

## SSH Escape Character and Disconnect Sequence

Short answer: Type `exit`

If that doesn't work, however...

Most SSH implementations implement an escape character for interactive sessions, similar to telnet's `Ctrl-]` combination.
The default SSH escape character is `~.`, entered at the beginning of a line.

If you want to terminate an interactive OpenSSH session **which is stuck and cannot be exited by entering `exit`
or <kbd>Ctrl</kbd><kbd>D</kbd> into a shell on the remote side**,
   you can enter `~` followed by a dot `.`. To be sure to enter the escape character at the beginning of an input line,
   you should press Enter first.
So the following sequence will in most cases terminate an SSH session:

    *Enter ~ .*

Other Escape Sequences
-----

OpenSSH, for example, offers other escape sequences besides `~.`. Entering `~?` during a session should give you a list. Some examples:

- `~` followed `Ctrl-Z` suspends the session,
- `~&` puts it directly into background,
- `~#` gives a list of forwarded connections in this session.
- If you want to simply enter a tilde at the beginning of a line, you have to double it: `~~`.

The escape character can be changed using the command line option `-e`. If you set the special value `-e none`, escaping is disabled and the session is fully transparent.

## command history

[Command History][7]

```
    history n               <<< This will only list the last n commands.

    CTRL + R                <<< Search history, hit ctrl-r again to scroll backward through the matched history
    CTRL + S                <<< scroll forward through the matched history
    CTRL + G, or left,right <<< Escape from search mode
    !abc                    <<< Echo last command in history beginning with abc
    !abc:p                  <<< Echo last command in history beginning with abc
    !?abc                   <<< Echo the last command that contains abc
    !?abc?                  <<< Echo the most recent command that contains string.

    !!                      <<< Echo last whole command
    !* <OR> !^ <OR> !$  <OR> !:2    <<< Echo last command’s parameters <ALL>,  <first>,  <last>, <2nd>
    Alt+.  <OR>  Alt+_      <<< Echo last command’s parameters: Press esc-. or alt+., tt cycles through the previous arguments you used.

    ls -l !cp:2             <<< !cp:2 echo command starts with cp and takes the second argument

    $ ls | sed ... | source /dev/stdin   <<< execute the output of a command within the current shell?
    $ eval $( ls | sed... )
```


## tricks

```
    $ gnome-session-quit	<<< shell’s logout command
    $ reset		<<< shell reset
    $ setxkbmap	<<< reset the keyboard map
    $ bash -xv filesize.sh   <<<< Execute Shell script with debug option
```

# Command howto:

## check git which dir commit most frequent

    $ git log0 --name-only --oneline > log.list
    $ cat log.list | grep '^*' -v | cut -d'/' -f1-2 | sort | uniq -c | sort -nr | head -10
       7123 | tests/data
       2443 | docs/libcurl
       1903 | CHANGES
       1659 | RELEASE-NOTES
       1590 | tests/libtest
       1208 | lib/url.c
       1165 | docs/examples
        864 | include/curl
        725 | tests/server
        692 | lib/ftp.c

# Commands:

## top

so either use shift or caps lock.

    P %CPU
    M %MEM
    N PID
    T TIME+

By default, they will be sorted in DESC order. Use R to toggle ASC/DESC.
To set the sorting from the command line option, use top -o %MEM. You can specify any column.

## tool: mutt - email client

    echo "" | mutt -s 'patch of HTTP-CONNECT-USER' hyu@fortinet.com -a patch.diff

## tool: trans - dictionary client

[Page][https://github.com/soimort/translate-shell]

    $ wget git.io/trans
    $ chmod +x ./trans

    $ trans :zh word
    $ trans en:zh "word processor"

    ### Translate a word into Chinese and Japanese
    $ trans :zh+ja word

    $ trans zh: 手紙

## watch

-t   silent the header
-c   support color
-n   secdons

### sample

```sh
    $ watch -c du -sch ./*

    # every 5-seconds execute the command
    $ watch    -n 5 free -m
    $ watch -t -n 5 free -m               <=== -t silent the header
    $ watch -d=cumulative 'ls -l | fgrep janis'
```

### shell-script likes

You can emulate the basic functionality with the shell loop:

    while :; do clear; your_command; sleep 2; done

That will loop forever, clear the screen, run your command, and wait two seconds - the basic `watch your_command` implementation.

You can take this a step further and create a `watch.sh` script that can accept `your_command` and `sleep_duration` as parameters:

```sh
    #!/bin/bash
    # usage: watch.sh <your_command> <sleep_duration>

    while :;
      do
      clear
      date
      $1
      sleep $2
    done
```

## du

    du -shc <dir>
      -s, --summarize
      -h, --human-readable
      -c, --total

    $ df .                    # find out what partition the current directory is on

    $ du -sch --exclude=.git
        544M    .
        544M    total

    ### the cumulative disk usage of all non-hidden directories, files etc
    $ du -sch -- * | tail
        4.0K    sit
        1.9M    snmp
        1.9M    tests
        544M    total

    ### Only list the dirs
    $ du -h --max-depth=1 | sort -hr
        13G     ./.git
        13G     .
        20M     ./router
        19M     ./dev-dir

    ### Or using `./*`
    $ du -sch ./* | sort -h
        148K    ./mk
        352K    ./include
        1.9M    ./tests
        13M     ./tools
        544M    total

    $ watch du -sch ./*

## dd

    $ dd if=mylinux.iso of=/dev/sdb bs=20M	# Creating a bootable USB disk
    $ dd if=/dev/dvd of=myfile.iso bs=2048	# Ripping a CD or DVD for local storage
    $ dd if=/dev/sdc of=sdc.img bs=100M conv=sync,noerror	# Image a disk

## netcat: a better `telnet`

https://www.g-loaded.eu/2006/11/06/netcat-a-couple-of-useful-examples/

    $ sudo apt-get install netcat pv


### telnet with a batch of commands

```sh
    telnet 192.168.1.199 <<<"print_debug"
```

Out of sudden, netcat comes to my mind, and It works!

```sh
    nc 192.168.1.199 23 <<<"print_debug"
    nc 192.168.1.199 23 <<<"print_debug" > result.txt
```

A more better solution:

    1. First, Create a normal text file and list all the commands line by line. At the end of the line put ‘exit’, Assume my file is call commands.txt. Examples:

```sh
    print_debug
    proplist
    ...
    exit
```

    2. Secondly, I can reconstruct my netcat command line into this

```sh
    nc 192.168.1.199 23 < commands.txt >results.txt
```

### transfer file between two PCs

    pc-A: $ sudo tar -zcf - CentOS-7-x86_64-DVD-1503.iso | pv | nc -l -p 5555 -q 5

    pc-B: $ sudo nc 192.168.1.4 5555 | pv | tar -zxf -

## socat

socat can setup a pipeline just like the UNIX command line pipe "|" except that with socat you setup a two way pipe.
That is the beauty of socat.

The official examples: https://github.com/craSH/socat/blob/master/EXAMPLES

https://www.cybrary.it/0p3n/socat-polymorphic-networking-tool
http://lukeluo.blogspot.com/2014/06/linux-virtual-console5-socat-bridging.html


### Using Socat to Simulate Networking Traffic to Test and Debug

https://www.vividcortex.com/blog/2013/04/15/using-socat-to-simulate-networking-traffic-to-test-and-debug/

We need a way to test/debug that the interface we programmed to enable our system communicate with the other end, can satisfy all the use
cases. For brevity’s sake, we will have only one such case, and invent a very simple protocol as a proof of concept.

The Solution

What we need is an ad-hoc pseudo-chat client that lets us send arbitrary payloads over a persistent tcp connection, while being as verbose
as possible.

Uhmmm… What?

A simulator!

We want a program that:

  * Can connect to our system via tcp socket.
  * Can persist that connection. (the protocol can have “handshaking” logic for each connection)
  * Lets us send arbitrary payloads
  * Accept arbitrary payloads and print them.
  * Print those also in hexa in case the payload is not printable.

Why?

Well… if we have everything above done for us, human insteraction can do the rest!

How?

Wait for it… With socat of course! Here is an example:

Let’s say our system is an ATM, and we are going to be able to send transactions to a new banking institution. For that, we have to
implement their Bacon&Eggs protocol. They don’t provide a simulator for their end, but they at least give us some example payloads.

Here is a bacon payload (request) with id 666:

```sh
__      _.._
       .-'__`-._.'.--.'.__.,
      /--'  '-._.'    '-._./    id=666
     /__.--._.--._.'``-.__/
     '._.-'-._.-._.-''-..'

```

And here is an eggs payload (response, referencing the request with id 666):

```sh
$ cat eggs.payload

,-""""-.     ,'"`.
   /        `.  /     \
  |           );       :    responded=666
   \        ,' :       ;
    `-....-'    `.___,'

```

Ok, we upgrade our ATM software to support protocol Bacon&Eggs. How can we test and debug as we go?

Setup

 1. Create a pipe to receive the payloads. mkfifo /tmp/receive
 2. Create a pipe to send the response payloads. mkfifo /tmp/send
 3. Create a file to stream the responses to the sending pipe (more on this later). touch /tmp/stream
 4. Set a console to read (and keep reading) from /tmp/receive. tail -f /tmp/receive
 5. Set a console to write (and keep writing) to /tmp/send. tail -f /tmp/stream >> /tmp/send
 6. Set socat to listen and accept connections on some port and:
 7. whatever it receives from the socket, it forwards it to the receiving pipe.
 8. whatever it receives from the sending pipe, it forwards it to the socket.
 9. print the payload in text and in hexa

Like this:
```sh
    $ socat -x -v -d -d tcp4-listen:8032,fork,reuseaddr pipe:/tmp/send\!\!/tmp/receive
    # -x HEX print
    # -d dump data
    # pipe:/tmp/send!!/tmp/receive
    #   /tmp/send as the PIPE's input
    #   /tmp/receive as the PIPE's output


```
Now we can make our ATM connect to port 8032 at localhost as if it were a true Bacon&Eggs system. Now, whenever our ATM software sends a
bacon request with id=667, we just open our egg payload response example in a text or hex editor, replace 666 with 667 to make it a correct
response and send it back.

```sh
cat eggs.payload >> /tmp/stream
```

Our ATM software receives a correct egg response for its bacon request and thus the transaction is approved. The connection is still open,
so we can keep sending requests and responses and try different scenarios and use cases.

It’s like chatting with your software over a socket. Here is a screenshot of my human operated Bacon&Eggs protocol server processing a
transaction.


### simple telnet server by using socat

On server side:

```sh
    $ ./socat exec:'bash -li',pty,stderr,setsid  tcp-listen:8999,reuseaddr
```

On client side:

```sh
    $ ./socat tcp-connect:127.0.0.1:8999 file:`tty`,raw,echo=0
```

### A UDP example: name server lookup

Just to give you an example that is not also based on TCP, let's look at name server lookups. They are (usually) based on UDP. As we will see, this is a binary protocol. This time we have to use socat to set up a UDP relay:

```sh
    socat -x udp-listen:1234,reuseaddr udp:000.000.000.000:53
```
Note the -x option to output a hex dump. Replace 000.000.000.000 by the numerical IP address of your name server from /etc/resolv.conf. In order to perform the lookup, one can use the dig program. (The host program does not allow to specify a port to contact.) The following command line makes it connect to the relay we have set up:

```sh
    dig @127.0.0.1 -p 1234 volkerschatz.com
```

The IP after the @ is the name server to contact, and the number after -p is the port; in this case they refer to the local port of the socat relay. The hex dump of the communication is:

> 2013/03/17 20:23:19.001936  length=45 from=0 to=44
 49 66 01 20 00 01 00 00 00 00 00 01 0c 76 6f 6c 6b 65 72 73 63 68 61 74 7a 03 63 6f 6d 00 00 01 00 01 00 00 29 10 00 00 00 00 00 00 00
< 2013/03/17 20:23:19.046846  length=61 from=0 to=60
 49 66 81 80 00 01 00 01 00 00 00 01 0c 76 6f 6c 6b 65 72 73 63 68 61 74 7a 03 63 6f 6d 00 00 01 00 01 c0 0c 00 01 00 01 00 00 1c 10 00 04 51 a9 91 46 00 00 29 0f a0 00 00 00 00 00 00
Pretty much the only obvious thing one can discern is the host name volkerschatz.com starting with 76 6f 6c 6b ... (use man ascii to display the ASCII code manual page). Interestingly, the com top-level domain is separated by a byte with value 03, not a dot.


## ln

Check the original file of a softlink.
Or find the original file have some softlink already point-to itself.

```sh
    $ ln -s $(pwd)/orig.file $(pwd)/dirA/
    $ ln -s $(pwd)/orig.file $(pwd)/dirB/lorig.file
```

At this point, I can use readlink to see what is the 'original' (well, I guess the usual term here is either 'target' or 'source', but those in my mind can be opposite concepts as well, so I'll just call it 'original') file of the symlinks, i.e.

```sh
    $ readlink -f dirA/orig.file
    /tmp/orig.file
    $ readlink -f dirB/lorig.file
    /tmp/orig.file
```

... However, what I'd like to know is - is there a command I could run on the 'original' file, and find all the symlinks that point to it? In other words, something like (pseudo):

```sh
    $ find -L /dir/to/start -samefile /tmp/orig.file
```

## ls

    $ ls -d forti*
      forticov  fortipkg  fortitest  fortiweb

    $ ls forti*
      forticov:
      coretypes.h  defaults.h  filenames.h  gcov-io.c  gcov-io.h  gcov-iov.h  libgcov.c  Makefile  obj  Rules.mk  script  tm.h  tsystem.h

      fortipkg:
      fetch  include  lib  packages

      fortitest:
      appl  asic  common  include  init  linux  Makefile  netbt  obj  osdep  platform  Rules.mk  testcase  tools

      fortiweb:
      client  extutil  genoem.sh  genpy.py  include  java  Makefile  Makefile.gui  modules  obj  packages  python  Rules.mk  server  tools  ujson

With `zsh` you can easily express it directly, e.g:

    echo *(.)

will either only return the list of regular files or an error depending on your configuration.

For the non-directories:

    echo *(^/)

(will include symlinks (including to directories), named pipes, devices, sockets, doors...)

    echo *(-.)

for regular files and symlinks to regular files.

    echo *(-^/)

for non-directories and no symlinks to directories either.

Also, see the `D` globbing qualifier if you want to include <strong>D</strong>ot files (hidden files), like `*(D-.)`.

## grep; ag,ack

    $ grep -Inr "60D"
    $ ag --nogroup "kernel" cooked

    # cut long lines and keep color
    $ ag --nogroup --color "kernel" cooked | cut -c1-200

## rm

    $ rm "-1mpFile.out"
    $ rm -- -1mpFile.out
    $ rm !(*.c|*.py)        	 delete all the files except .c and .py files.

## diff

There have another tools like: lsdiff, filterdiff, diffstat, patch.

    $ diff -x '*.gz' -x '.git' -x '.svn' -w -u -r -N WorkingCopy1 WorkingCopy2
        -w to ignore all Whitespace
        -u to use the unified diff format (like subversion)
        -r for recursive
        -N to let new files appear in the patch

    $ diff -bur folder1/ folder2/

    This will output a recursive diff that ignore spaces, with a unified context:

        -b flag means ignoring whitespace
        -u flag means a unified context (3 lines before and after)
        -r flag means recursive
        -q quiet or brief, only list files name, not include patch content

## touch

    $ touch -d "9am" temp1  	 create dir according assigned time
    $ stat temp1            	 check the 'touch' result
    $ touch -t 200701310846.26 index.html    	 [[cc]yy]MMDDhhmm[.ss]
    $ touch -d '2007-01-31 8:46:26' index.html
    $ touch -d 'Jan 31 2007 8:46:26' index.html    	 you can copy the timestamp use ls -l
    $ touch -d "13 may 2001 17:54:19" date_marker

## cut

mode:
 - character-mode
 - field-mode

option: cut -d: -f 1,3
  -d, --delimiter
  -f, --show-field
  -c, --show-character

```shell
    $ cut -d: -f 1 names.txt		 show 1st field with a colon delimited
    $ cut -d: -f 1,3 names.txt 		 show 1st and 3rd field from a colon delimited file
    $ cut -c 1-8 names.txt			 show 1~8 characters of every line in a file
    $ cut -c 5-  log.txt			 remove first 4 characters, show the reserved
    $ free | tr -s ' ' | sed '/^Mem/!d' | cut -d" " -f2    	 Displays the total memory available on the system.
```

## split

    # You can use the split command with the -b option:
    $ split -b 1024m file.tar.gz

    # Creates files: file.tar.gz.part-aa, file.tar.gz.part-ab, file.tar.gz.part-ac, ...
    $ split -b 1024m file.tar.gz "file.tar.gz.part-"

### reassembled

    <windows>
    $ copy /b file1 + file2 + file3 + file4 filetogether

    <linux>
    $ cat file.tar.gz.part-* > file.tar.gz

### with tar

    # create archives
    $ tar cz my_large_file_1 my_large_file_2 | split -b 1024MiB - myfiles_split.tgz_

    # uncompress
    This solution avoids the need to use an intermediate large file when (de)compressing. Use the tar -C option to use a different directory for the resulting files. btw if the archive consists from only a single file, tar could be avoided and only gzip used:
    $ cat myfiles_split.tgz_* | tar xz

### with gzip

    # create archives
    $ gzip -c my_large_file | split -b 1024MiB - myfile_split.gz_

    # uncompress
    $ cat myfile_split.gz_* | gunzip -c > my_large_file
    For windows you can download ported versions of the same commands or use cygwin.

## awk

```shell
    awk -F ":" '/wilson/{ print $1 | "sort" }' /etc/passwd

    awk '/regex/'				 Print only lines which match regular expression (emulates "grep")
    awk '!/regex/'				 Print only lines which do NOT match regex (emulates "grep -v")
    awk 'NR==1; END{print}'		 print the first and last line

    awk '/AAA.*BBB.*CCC/'			 AND, contain "AAA" and "BBB", and "CCC" in this order.

    awk '/AAA|BBB|CCC/'			 OR, match any of "AAA" or "BBB", or "CCC".
    awk '/AAA/; /BBB/; /CCC/'		 AND, Grep for AAA and BBB and CCC (in any order)

    awk 'NR==8,NR==12'			 Region, Print section of file based on line numbers (lines 8-12, inclusive, emulates sed -n ‘8,12p’)
    awk '/Iowa/,/Montana/'		 Print section of file between two regular expressions (inclusive), (emulates sed -n ‘/Iowa/,/Montanna/p’)

    awk 'END{print}'				 Print the last line of a file (emulates "tail -1")
    awk 'NR < 11'				 Print first 10 lines of file (emulates behavior of "head")

    awk '!a[$0]++'				 Remove duplicate, consecutive lines (emulates "uniq")
    awk 'a !~ $0; {a=$0}'

    awk -F ":" '{ print $1 | "sort" }' /etc/passwd		 Print and sort the login names of all users
    awk '{gsub(/scarlet|ruby|puce/, "red"); print}'		 Change "scarlet" or "ruby" or "puce" to "red"
    awk '{sub(/^/, "     ");print}'					 Insert 5 blank spaces at beginning of each line (make page offset)
    awk '/regex/{getline;print}'					 Print the line immediately after a regex, but not the line containing the regex
    awk '{total = total + $1}END{print total}'
```

## sed

```shell
    $ sed 's/ruby/bird/g'		# replace like vim
    $ sed '$d' file				# delete last line
    $ sed -n '1,$p' file		# display all
    $ sed -n '/ruby/p' file		# grep keyword
    $ sed '1,3a drink tea' file	# append "drink tea" to the 1~3 line
```

## sort

option:
  -t    delimiter
  -k    index key fields
  -n    take key fields as number, default is string
  -r    output descending order

```shell
    sort -t: -u -k 3n

    $ sort -r names.txt			Sort a text file in descending order
    $ sort -t: -k 2 names.txt		Sort a colon delimited text file on 2nd field (employee_id)
    $ sort -t: -u -k 3 names.txt	Sort a tab delimited text file on 3rd field (department_name) and suppress duplicates
    $ sort -t: -k 3n /etc/passwd | more	 Sort the passwd file by the 3rd field (numeric userid)
    $ sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n /etc/hosts		Sort /etc/hosts file by ip-address

    ps -ef | sort				Sort the output of process list
    ls -al | sort +4n			List the files in the ascending order of the file-size. i.e sorted by 5th filed and displaying smallest files first.
    ls -al | sort +4nr			List the files in the descending order of the file-size. i.e sorted by 5th filed and displaying largest files first.
```
## tr

option
  -s    squeeze repetition of characters: `tr -s [:space:] ' '`
  -w    Delete specified characters: `tr -d 'x'`, `tr -d [:digit:]`
  -c    Complement behavior, like `grep -v`: echo 'unix' | tr -c 'u' 'a'      output=uaaa

Uppercase:
    $ tr a-z A-Z
    $ tr '[a-z]' '[A-Z]'
    $ tr [:lower:] [:upper:]

Tabs to white-space:
    $ tr [:space:] '\t'

Set replace one-by-one, using '*' to pad:
    $ tr '{}' '()'
    $ tr -c '[:alnum:]' '[\n*]'

Remove all non-printable character:
    $ tr -cd [:print:] < file.txt

Join lines into a single line:
    $ tr -s '\n' ' ' < file.txt

## uniq

`uniq` does not detect repeated lines unless they are adjacent.
You may want to sort the input first, or use 'sort -u' without 'uniq'.

The weird is have no option to assign delimiter, the field split by space.
so maybe we can use `tr` to convert the delimiter.

  -c    show repeated count
  -f    number-of-fields-to-skip, delimiter is ' ',
  -s    number-of-char-to-skip,
  -w    number-of-char-to-compare,
  -i    case-insensitive,
  -z    force ouput NUL-terminated, like find's -print0

```shell
    uniq <file>         Delete repeated lines
    uniq -c <file>      Display number of repeated for each line
    uniq -D <file>      Display only duplicated lines
    uniq -u <file>      Display only non-duplicated lines
    uniq -uf 1
    uniq -f 1		skip the first field
    uniq -s 8		skip the first 8 char
    uniq -uf 1

    # statitics app crash times
    ag --nogroup " application " Mar_16.txt.txt | awk '{print $6}' | sort | uniq -c
```

## join

like excel’s vlookup

## bc

```shell
    echo $(sed 's/$/+/' /tmp/file.txt) 0 | bc
    echo will remove newline, default have -n option which donnot show the newline.
    Also we can use paste -s to remove a file’s newline
    paste -sd+ - | bc
    http://www.theunixschool.com/2012/07/10-examples-of-paste-command-usage-in.html
```

## paste

merge two files by column

```shell
    $ paste file1	# like cat
    Linux
    Unix

    $ paste file1 file2
    Linux   Suse
    Unix    Fedora

    $ paste -d':' - - < file1
    Linux:Unix
    Solaris:HPUX
```

## tree

    $ tree -f -I "bin|unitTest" -P "*.[ch]|*.[ch]pp." your_dir/
        -f prints the full path for each file,
        -I excludes the files in the pattern here separated by a vertical bar.
        -P switch inlcudes only the files listed in the pattern matching a certain extension.

## mkdir

    -m: setup file mode
    -p: create the whole path


## tar

    tar cvjf Phpfiles-org.tar.bz2 /home/php
    tar cvzf MyImages-14-09-12.tar.gz /home/MyImages

    tar zxvf mysql.tar.gz -C /home/aaa		# uncompress to the assigned dir
    tar -xjf linux-2.6.38.tar.bz2 --transform 's/linux-2.6.38/linux-2.6.38.1/'

    tar -tvf foo.tar | grep 'etc/resolv.conf'	# list file
    tar --delete -f foo.tar etc/resolv.conf	# remove one file from tar

        c/x/t only exist one-of-them
        -c, compress/create
        -x, uncompress
        -C, uncompress to this dir
        -t, list files

        -z gzip
        -j bzip2
        -v verbose
        -f filename

## rar

    rar file
    tar xzf rarlinux-x64-5.0.b7.tar.gz
    sudo cp rar unrar /usr/local/bin/
    unrar x ~/Downloads/wps_symbol_fonts.rar

## cp & rsync


## dns & reverse-dns

    $ dig +noall +answer www.gnu.org
    www.gnu.org.            67      IN      CNAME   gnu.org.
    gnu.org.                67      IN      A       199.232.41.10

    The IP address is displayed in the A record, and is 199.232.41.10.
    The +noall, +answer combination basically tells dig to only report the answer of the DNS query and skip the rest of the output.

    ### -x option to do a reverse DNS lookup
    $ dig +noall +answer -x 199.232.41.10
    10.41.232.199.in-addr.arpa. 36000 IN    CNAME   rev-c41-10.gnu.org.
    rev-c41-10.gnu.org.       300     IN      PTR     www.gnu.org.

## locate

    The locate command is lightning fast because there is a background process that runs on your system that continuously finds new files and stores them in a database.
    When you use the locate command, it then searches that database for the filename instead of searching your filesystem while you wait (which is what the find command does).

## find

### -exec '\;'

If you run find with exec,
  - '{}' expands to the filename of each file or directory found with find.
  - ';'  the semicolon ends the command executed by exec. It needs to be escaped with \ so that the shell you run find inside does not treat it as its own special character, but rather passes it to find.

### -exec '+'

Also, find provides some optimization with exec cmd {} +
  - find appends found files to the end of the command rather than invoking it once per file (so that the command is run only once, if possible).

The difference in behavior (if not in efficiency) is easily noticeable if run with ls, e.g.

    find ~ -iname '*.jpg' -exec ls {} \;
    # vs
    find ~ -iname '*.jpg' -exec ls {} +

Assuming you have some jpg files (with short enough paths), the result is one line per file in first case and standard ls behavior of displaying files in columns for the latter.

### samples

    -a*,-c*,-m*: access, attr, modify
        [a] access (read the file's contents) - atime
        [c] change the status (modify the file or its attributes) - ctime
        [m] modify (change the file's contents) - mtime

    -mmin, -mtime: mins, days
        -mmin n   	  n minutes ago.
        -mtime n   	 days,  n*24 hours ago.
        -mtime -6,6,+6: > , ==, < ago
        -mtime +60 	 means you are looking for a file modified 60 days ago.
        -mtime -60  	 means less than 60 days.
        -mtime 60 If you skip + or - it means exactly 60 days.

        $ find . -daystart -atime 1 -maxdepth
        $ find . -newer date_marker
        $ find . \! -cnewer date_marker

    # find empty file
    $ find . -size 0c
    $ find . -empty -maxdepth 1 -exec rm {} \;

    $ find . -size 1000c	# find files with exactly 1000 characters
    $ find . -size +599c -and -size -701c	# find files containing between 600 to 700 characters, inclusive.
    $ find /usr/bin -size 48k
        c = bytes
        w = 2 byte words
        k = kilobytes
        b = 512-byte blocks

    find . -maxdepth 1
    find /path -name '*.[ch]'			# or
    find /path -name  '*.c' -o -name '*.h'	# or
    find /path -iname '*python*'		# case-insensitive.
    find /path -regex '.*python.*|.*\.py'	# Regex match
    find /home -user joe			# owned by `joe`
    find /tmp -name core -type f -print0 | xargs -0 /bin/rm -f
    find . -type f -exec file '{}' \;

    find . -maxdepth 3 -name rb_genco -exec grep -H "123268" {} \;
    find -H . -maxdepth 3 -name rb_genco | xargs -I{} grep -lsn "123268" {}

    $ find dir1 dir2 dir3 | wc -l		# Count files
    $ find . -newer ../temp1 ! -newer ../temp2 -exec cp '{}' ./bkup/ ';'	# copy newer than 'temp1' and not newer than temp2
    $ find . -newer marker -not -path "*/\.*"	# find newer compare with marker but exclude the hidden-dir

### batch rename

batch rename all wad*.c files to extension *.cpp files
    $ find . -name '*-GHBAG-*' -exec bash -c 'mv $0 ${0/GHBAG/stream-agg}' {} \;
    $ rename -v 's/([a-z]*)\.c/file_$1.cpp/' wad*.c

### find -exec vs xargs

    find ... -exec rm {} \;		# runs cmd 'rm' once for each match
    find ... -exec rm {} +		# new version like 'xargs'
    find ... -print0 | xargs -0 rm -rf	# more efficient, runs cmd 'rm' as few times as possible

### Using semicolon (;) vs plus (+) with exec in find

    This might be best illustrated with an example. Let's say that find turns up these files:
    file1
    file2
    file3

    Using -exec with a semicolon (find . -exec ls '{}' \;), will execute

    ls file1
    ls file2
    ls file3

    But if you use a plus sign instead (find . -exec ls '{}' \+), all filenames will be passed as arguments to a single command:
    ls file1 file2 file3

## fastmod

  https://github.com/facebookincubator/fastmod
  Fastmod is a fast partial replacement for codemod. Like codemod, it is a tool to assist you with large-scale codebase refactors.

  Let's say you're deprecating your use of the <font> tag. From the command line, you might make progress by running:

    $ fastmod -m -d /home/jrosenstein/www --extensions php,html \
        '<font *color="?(.*?)"?>(.*?)</font>' \
        '<span style="color: ${1};">${2}</span>'

    $ fastmod -m ~/workref/compile_commands.json-v6.0.6 \
        '/ssd/work/top3-ssl-offload/br_6-0_eps_proxy' \
        '/ssd/work/bug-socks-log/6.0-kvm'

    """ quiet and quicker
    $ fastmod --accept-all -F '/ssd/work/top3-ssl-offload/br_6-0_eps_proxy' '/ssd/work/bug-socks-log/6.0-kvm' ./compile_commands.json

## wget

    --no-check-certificate, skip certificate

## curl

    -k, skip certificate

[Doc](https://ec.haxx.se/http-cookies.html)
@SeeAlso [[../tool/tools#curl]]

### Install new verion (ubuntu)

1. Append to /etc/apt/sources.list like this:

deb http://security.ubuntu.com/ubuntu zesty-security main
deb http://cz.archive.ubuntu.com/ubuntu zesty main

2. Install

$ sudo apt-get update
$ sudo apt-get install libcurl3  ### if needed, maybe remove them first
$ sudo apt-get install curl

# Samples

    $ stat -f /      	 Display the status of the filesystem using option –f
    $ tr a-z A-Z < employee.txt   	  Convert a file to all upper-case
    $ ac -p  	 Display total connect time of users
    $ wc -l **/*.c  	 count all file recursive
    $ pwd | tr -d ‘\n’ | xsel		 to clipboard
    $ grep -rl -w 'bar' /path/to/folder | xargs sed -i sed "s/\<bar\>/no bar/g"   	 search and replace in grep result
    $ diff -r -u a/dir/file1 b/dir/file1    	 generate the diff of two files

    # change all filename into lowercase
    $ ls | while read upName; do loName=`echo "${upName}" | tr '[:upper:]' '[:lower:]'`; mv "$upName" "$loName"; done

# command lists:

[Linux Tricks and Useful Commands][1][2][4]

```shell
    $ wget -c <url>			# resume interrupted downloads
    $ curl -C <url>			# resume interrupted downloads
    $ wget -rpk <url>			# mirror an entire website
    $ curl dict://dict.org/d:<word>
    $ host <url>			# public IP
    $ cat /dev/urandom > /dev/null	# put a CPU to 100% usage
    $ xset dpms force off		# Turning of the monitor to save power
    $ <command> | xsel --clipboard	# put output into the X system clipboard
    $ echo "command you want to run" | at 01:00		# Running a command at a specified time

    $ sudo cat /etc/issue		# os info
    $ sudo cat /proc/cpuinfo
    $ sudo getconf LONG_BIT		# 32bit or 64bit OS
    $ uname -a | grep Linux
    $ sudo fuser -k <file_name>		# Killing a process that has locked a particular file

    $ sudo fdisk -l			# Partitioning and formatting a USB key
    $ cat image.png compressed.zip > secret.png		# Hiding a file or directory within an image, view with $ unzip secret.png


    $ grep -l "printf" *.c     	 search all the files in a directory containing a particular string "printf"
    $ grep -B2 Subj: maildrop.log | grep -v ^From: | grep -v ^– | xargs -d$’\n’ -n 2        # Join the Date and Subj line together in procmail log.
    $ grep -ril inactive /etc # Show matching files(-l) with the string “inactive” regardless of case(-i) in all subdirs of /etc (-r)
    $ > ./logfile           	 empty a file

    $ man -k login          	 search man pages for a particular string "login"
    $ tail -f logfile logfile1   	 follow multiple log files on the go
    $ <space>cmd                  	 insert space to not appear in `history` command

    # typing simulate using pv
    $ echo "You can simulate on-screen typing just like in the movies" | pv -qL 10

    $ pushd                 	 put or pop dir into stack
    $ popd

    $ pwd -P                  # Print path to the dir you are in, converting any symlinks in the path into their real/(P)hysical directory name.
    $ ascii || man ascii      # Quick access to the ASCII character table either through the ascii program or the man page
    $ ionice -c 3 cp vm1.img vm1-clone.img # Copy a file using “ionice -c 3″ to give it idle IO priority to reduce load on the system.
    $ foremost                # file recovery program
    $ ls -d */                # View only the directory
    $ gzip -l largefile.gz    # A fast way to get the size of the uncompressed gzip file

    $ sleep 30m ; killall tcpdump      # Use a ; in a statement if you want to run a command after another, but don’t care about the exit status of 1st
    $ ssh-keygen -R servername      # Remove the host key for ‘servername’ from your known_hosts file
    $ ssh-copy-id ‘user@remotehost’    # Automatically installs your public key to the remote host (this actually is included in the openssh package)

    $ xargs -n1 -0 < /proc/$(pidof firefox| cut -d’ ‘ -f1)/environ       # Print the environment of a running process (ie. firefox)
    $ last |awk ‘BEGIN {f=0;u=”YOURUSER”;} {if ($1==u && f==0){f=1; print $0;}else if(f==1 && $1!=u) {print $0;exit;}}’       # Display prev. user b4 u
    $ find . -type f | egrep -o “[^\.]+$” | tr A-Z a-z | sort | uniq -c  # Show a count of all the file extensions in use below current directory.
    $ awk ‘{a[$1] += $10} END {for (h in a) print h ” ” a[h]}’ access_log | sort -k 2 -nr | head -10          # Display top bandwidth hogs on website.
    $ awk ‘{if (a[$1]) { print; } else { a[$1]=1 }}’ md5sums.txt         # And here is a way to print only duplicates using just awk. sort md5sums.txt | uniq -d -w 32 # Print only duplicate md5sums by looking only at first 32 chars for uniqueness. head -5 file1 |cat – file2 >combofile # One way of putting the first 5 lines of file1 before the contents of file2 and writing to combofile
    $ ps aux | awk ‘/firefox/ {sum += $6} END { printf “%dMB\n”, sum/1024 }’         # Show the total memory used by Firefox processes (Probably a lot)

    $ df -TP | grep -E ” ext[34] ” | awk {‘print $NF’} | sed ‘s/.*/disk & 5%/’ # Print out the partition table and format it for snmpd.conf
    $ df -TP | awk ‘$2=/ext[34]/ {print “disk ” $NF ” 5%”}’ # snmpd disk entries, same thing but let awk do most of the processing work.
    $ df -P -t ext3 -t ext4 | grep / | awk ‘{print “disk ” $NF ” 5%”}’ # snmpd disk entries, Let df select the filesystems directly.
    $ df -TP | grep -E ” ext[34] ” | rev | cut -d’ ‘ -f1 | rev | while read -r fs ; do echo “disk $fs 5%” ; done # Disk entries. The Crazy Way!

    $ ethtool -p eth0           # Blink eth0′s LED so you can find it in the rat’s next of server cables. Ctrl-C to stop. Thanks

## Howtos extra

### How to Disable Invalid SSL in Firefox

Secure Socket Layer, or SSL, protects private data by encrypting it during transmission.
To enable SSL encryption, websites use an SSL certificate issued by a certificate authority.
When you enter an "https://" address to browse a site, Firefox checks the SSL certificate data to determine whether it is valid.
When Firefox encounters an expired or invalid SSL certificate, it blocks the page or displays a warning.
However, you might want to disable the warnings or blocking of unencrypted sites for site testing or other reasons.
A change to advanced Firefox preferences allows you to prevent the warnings.

- about:config
- browser.ssl_override_behavior" in the "Filter" box. Double-click the "browser.ssl_override_behavior" value in the "Preference Name" list.
- Change the value in the "Enter integer value" dialog box from "2" to "1" and click the "OK" button.

```

  [1]: http://linuxtrove.com/wp/?p=314
  [2]: http://57un.wordpress.com/2013/04/29/15-interesting-and-extremely-helpful-linux-cli-tricks/
  [3]: http://www.cyberciti.biz/faq/linux-unix-test-internet-connection-download-upload-speed/
  [4]: http://varunbpatil.github.io/2012/09/19/linux-tricks/#.UhuM2BJDss0
  [5]: http://www.tuxarena.com/2014/03/20-great-terminal-replacements-for-gui-applications/
  [6]: http://www.thegeekstuff.com/2008/08/15-examples-to-master-linux-command-line-history/
  [7]: http://www.tldp.org/LDP/GNU-Linux-Tools-Summary/html/x1712.htm

