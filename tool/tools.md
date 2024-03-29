[#](#) terminal application

## [great-terminal-replacements-for-gui-applications][1]

# Tools

## Encrypt/Decrypt and Password Protect Files in Linux

1. GnuPG
GnuPG stands for GNU Privacy Guard and is often called as GPG which is a collection of cryptographic software. Written by GNU Project in C programming Language.
In most of the today’s Linux distributions, the gnupg package comes by default, if in-case it’s not installed you may apt or yum it from repository.

	$ sudo apt-get install gnupg
	# yum install gnupg
    $ gpg --version

    ### Encrypt a file
    $ cat ~/Desktop/Tecmint/tecmint.txt
    $ gpg -c ~/Desktop/Tecmint/tecmint.txt
    $ ls -l ~/Desktop/Tecmint
         ~/Desktop/Tecmint/tecmint.txt
         ~/Desktop/Tecmint/tecmint.txt.gpg
    ### and remove the orginal file
    $ rm ~/Desktop/Tecmint/tecmint.txt

    ### Decrypt a file
    $ gpg ~/Desktop/Tecmint/tecmint.txt.gpg

## meld (GUI diff)

    # Ubuntu (Linux Mint 14.04.1-Ubuntu)
    1. Download from https://github.com/GNOME/meld
    2. The doc say:
        $ python3 setup.py install --prefix=/usr
    3. But that not work for me. If use the doc's build cmd, it works except it require GTK 3.14, current only GTK 3.10:
        $ python3 setup.py --no-compile-schemas install
    4. If meld requre GTK 3.14, so far it's hard to upgrade GTK 3.14 from 3.10, we should use old meld:
        Download a old release version from github/meld, install this old one.

## Mosh (Mobile Shell): SSH without the connectivity issues

    ### Server & Client side
    $ sudo apt update
    $ sudo apt install mosh

    ### Server
    $ sudo ufw allow 60000:61000/udp

    ### Working from Client
    $ mosh seeni@LinuxHandBook.com

    ### specify a different ssh port
    $ mosh seeni@LinuxHandBook.com --ssh="ssh -p 2222"

    ### But it's terrible using vi: local buffer for avoiding latency
    $ mosh --predict=experimental user@server.com

### re-attach to a detached mosh session (You can't)

    Once the client is dead, you can't re-attach to the server session.

    https://github.com/keithw/mosh/issues/394

    For security reasons, you can only resume a connection to a mosh-server from the corresponding mosh-client.
    If the client is dead (e.g. the user quit the client while it was off the network),
    the only option is to kill the server with that PID (e.g. kill 12726).

## tmux

### copy history

    prefix + alt + shift + p

### rename-window <name>

    For example, if the top-line show like this:
      > 1:zsh  2:ssl-log- 3:urlfilter  4:block

### swap-window -s(src) 4 -t(dst) 2
    tmux-command: move-window/swap-window -s 4 -t 2         <=== move/swap s(src) to t(dest)

### swap-pane -s(src) 4 -t(dst) 2

    Prefix+q: show pane number

## vifm: cli file manager

```sh
    sudo apt-get install vifm
```

## todo.txt-cli: but taskwarrior is better

### install
    $ git clone https://github.com/huawenyu/todo.txt-cli-ex
    Create softlink existed 'todo' into this dir.

    # todo.txt-cli
    mkdir -p ~/tools
    cd ~/tools
    git clone https://github.com/todotxt/todo.txt-cli.git
    git clone https://github.com/huawenyu/todo.txt-cli-ex.git

    # should link the existed dir "todo" into the dir 'todo.txt-cli-ex':
    cd todo.txt-cli-ex
    # copy sh from 'todo.txt-cli' into our dir 'todo.txt-cli-ex':
    make -B


    ### append the follow lines into .zshrc:

        # todo.txt-cli
        export TODOTXT_DEFAULT_ACTION=ls
        #alias t='$HOME/tools/todo.txt-cli-ex/todo.sh -d $HOME/tools/todo.txt-cli-ex/todo.cfg'
        alias t='$HOME/tools/todo.txt-cli-ex/todo.sh'

### usage

```sh
    $ t -h
    $ t add "setup new linode server"
    $ t add "discuss fosswork.com site with Ravi"
    $ t
    $ t pri 1 A
    $ t append 2 "ready at 3PM"
    $ t do 1
    $ t del 1
    $ t listall

    ### create another task file
    $ t move 10 maybelater.txt
    $ t listfile maybelater.txt
    $ t addto ideas.txt "My bright idea"
    $ t lf ideas.txt apple
```

# qutebrowser - vim-like browser

https://qutebrowser.org/doc/quickstart.html

# minicom

    1. set env var value
      MINICOM="-w"
      export MINICOM

    2. sudo also using current shell's env: sudo -E
      $ sudo -E minicom -b 115200 | tee ~/tmp/log.minicom

# thunderbird

## Dark theme: use default dark theme, then just add user.js to our profile dir:

      https://github.com/overdodactyl/ShadowBird
      ## https://www.reddit.com/r/Thunderbird/comments/bxkymy/thunderbird_dark_theme_background_and_text_color/

## Create virtual dir base on search
      https://superuser.com/questions/41599/is-there-any-way-to-search-for-tags-in-mozilla-thunderbird

## Export message filter

    The msgFilterrules.dat is just plain text file. Edit it as you needed—usually just the directory paths for duplicating an account's filter to another account.
    Remember to close Thunderbird before manually change these msgfilterRules.dat files. Otherwise, Thunderbird will overwrite your changes.
    To quickly find all your filter setting files on Linux, run

    $ find ~/.thunderbird/ -name msgFilterRules.dat | xargs ls -l {} \+

## Addons FireTray: System Tray with unread message notify

    ### For TB 60.
    git clone https://github.com/firetray-updates/FireTray
    cd FireTray/src
    make build
    ls ../build-*/*.xpi # <-- your xpi, ready to be installed

    I don't use git, so just visited the page https://github.com/firetray-updates/FireTray
    Downloaded the zip file, right-click extracted it
    Used the Terminal command: cd ExtractedDirectory/FireTray/src
    followed by command: make build
    then navigate UP one directory to find "build-" directory which contains the file firetray-0.6.1.xpi
    click and drag it to Addons page in Thunderbird, click ok and restart

## Addons ThreadVis: Visualize the group threaded mail

    But conflict with addons, so please disable them before use: Thunderbird-conversation, Compact-header

## Addons:

- Edit email Subject
- Lightning
- NestedQuote Remover
- XNote++
- Cardbook
- AutoResize image

# nomachine

## remote control over ssh

```
Error Message:

    Running NoMachine sessions over a SSH connection is disabled on this server.

The suggested workaround is:
  $ sudo vi /usr/NX/etc/server.cfg
      ClientConnectionMethods NX,HTTP,SSH

  $ sudo /usr/NX/bin/nxserver --restart
```

# auto-expect

https://github.com/qsmx/auto-expect

# window's best terminal: Mobaxterm

We have two methods to add more tool into our Mobaxterm: download plugins, or `apt-get install bind-utils`

## Shortcuts

Ctrl+Tab    toggle tab
F11         toggle fullscreen

## HOME: MobaXterm keep its home directory?

```sh
  $ open /home/mobaxterm
  $ open `pwd`
```

## Config file

https://blog.mobatek.net/post/mobaxterm-configuration-settings/

How to locate my MobaXterm configuration file?
Well, it depends… Your MobaXterm.ini configuration file should be located:

in the same folder as MobaXterm executable if you are using MobaXterm Portable Edition
in %MyDocuments%\MobaXterm folder if you are using MobaXterm Installer Edition
in %MyDocuments%\MobaXterm folder if you are using MobaXterm Portable Edition and if you only have read access to the folder where the executable is
Moreover, you can use the -i commandline setting in order to determine the configuration file path for MobaXterm. For instance, you can specify the configuration file path manually at MobaXterm startup using the following command:
C:\Some\place\MobaXterm.exe -i “D:\Data\MobaXterm.ini”

or you can use a network shared folder:
C:\Some\place\MobaXterm.exe -i “\MySharedFolder\MobaXterm.ini”

or you can even use a web (HTTP) address in order to retrieve the configuration file:
C:\Some\place\MobaXterm.exe -i https://MyIntranetServer/MobaXterm.ini
In this case, the configuration file will be read from your intranet and any modification made by the user will be saved in a new MobaXterm.ini file created under %MyDocuments%\MobaXterm folder.




Which settings can be put in this INI file?
There are many settings which could be put in this MobaXterm.ini configuration file. We will just list the settings which cannot be set using the graphical interface. All these settings should be put under the [Misc] section of the configuration file. These options should be used by advanced users only:

Setting	Default value	Comment
MobaTempDir	%TEMP%	Path to MobaXterm temp folder
XWinSwitches	-hostintitle +bs	Additional X11 commandline parameters
Scrollbar	1	Toggle scrollbar visibility in terminal
SeparationLine	1	Toggle separation line visibility in terminal
BoldAsFont	no	Render bold text using bold font
BoldAsColour	yes	Render bold text using different colour
BellSound	no	Play a "beep" sound when terminal bell is triggered
BellFlash	no	Flash terminal when terminal bell is triggered
AllowBlinking	no	Allow font blinking in terminal
CtrlAltIsAltGr	no	Use Ctrl+Alt keys to simulate AltGr key press
NbPenguins	4	Number of penguins for the "consolesaver"
TimerConst	600	Time (in seconds) before starting the "consolesaver"
TimerInt	100	Time (in ms) between each penguin move in the "consolesaver"
PgUpDnScroll	0	Use PageUp/PageDown without "Shift" modifier for terminal scrolling
ScrollMod	shift	Change scroll modifier to ctrl/alt/shift
ScrollbackLines	360000	Specify scrollback buffer size

## Howto install [plugins](plugins)

1. Download plugin from Plugins list: https://mobaxterm.mobatek.net/plugins.html
2. Then put the plugin file into:
    - go into the C:\Program Files (x86)\Mobatek\MobaXterm Personal Edition or whichever edition you have and place the plugin there.
    - Restart MobaXterm and it should work.

## make apt-get packages also permanent

Q: If using install-version, no such issue at all, so don't need resolve.

I am using MobaXterm 10.8 portable.

Whenever I install any package with

$ apt-get install nano
$ apt-get install vim
$ apt-get install tmux
$ apt-get install bind-utils

I can use the package for the whole MobaXterm session. But these packages vanish when closing MobaXterm.

On the other hand, plugins are persistent.

Is there any way to make apt-get packages also permanent?

A:

The solution is setting a specific Settings -> General -> Persistent root (/) directory, instead of the default <Temp>:

## howto access windows native path
    $ cd /cygdrive/c            <=== if from cygwin env
    $ cd /drives/D/Downloads/   <=== if from Mobaxterm local shell env

## Install vim 8.0 + vim-plugins

    $ apt-get install vim

## Local shell: Bash profile

    $ ln -s ~/dotfiles/.bash_windows ~/.bash_profile

    $ cat .bash_profile
        parse_git_branch() {
             git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
        }
        export PS1="\[\033[32m\]\W\[\033[31m\]\$(parse_git_branch)\[\033[00m\] $ "

## tmux: should listen local socket to solve the permission issues

  $ apt-get install tmux
  $ tmux -S ~/.tmsock new work
  $ tmux -S ~/.tmsock list-keys

# Static code analyzers/checker for C

## cppchecker

### install
    $ git clone https://github.com/danmar/cppcheck.git
    $ cd cppcheck
    $ make SRCDIR=build CFGDIR=/usr/local/bin/ HAVE_RULES=yes CXXFLAGS="-O2 -DNDEBUG -Wall -Wno-sign-compare -Wno-unused-function"

    ### 'make install' also build and requires the CFGDIR option to be passed.
    $ sudo make install CFGDIR=/usr/local/bin/ HAVE_RULES=yes CXXFLAGS="-O2 -DNDEBUG -Wall -Wno-sign-compare -Wno-unused-function"

### usage

    $ cppcheck --enable=all wad_http_cache.c

## cpplint

This is automated checker to make sure a C++ file follows Google's C++ style
guide (https://google.github.io/styleguide/cppguide.html).

    https://github.com/google/styleguide/tree/gh-pages/cpplint

# Howtos

## Screen recorder

Screen present recorder video was generated with screenkey -g $(slop -n -f '%g') and simplescreenrecorder.

## Upgrade GTK 3.14

The GTK 3.10 is default version of Ubuntu (Linux Mint 14.04.1-Ubuntu).

### list current GTK version

    $ dpkg -l libgtk2.0-0 libgtk-3-0

  [1]: http://www.tuxarena.com/2014/03/20-great-terminal-replacements-for-gui-applications/
