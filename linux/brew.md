# Another pkg tool: snap

## Install

$ sudo apt update
$ sudo apt install snapd

### Add path
You have to verify if /snap/bin is included in this $PATH

$ snap find <search_text>
$ sudo snap install <package>
$ sudo snap install --channel=edge <package>

$ sudo snap refresh <package>
$ sudo snap remove <package>

# Intro

Linuxbrew Homepage: http://linuxbrew.sh/.
It's feature set includes:

- Allowing installation of packages to a home directory without root access.
- Supports installing of third-party software (not packaged on the native distributions).
- Supports installing of up-to-date versions of packages when the one provided in the distro repositories is old.
- In addition, brew allows you to manage packages on both your Mac and Linux machines.

# Install Linuxbrew in Linux

To install Linuxbrew on your Linux distribution, fist you need to install following dependencies as shown.

    ###--------- On Debian/Ubuntu ---------
    $ sudo apt-get install build-essential curl file git

    ###--------- On Fedora 22+ ---------
    $ sudo dnf groupinstall 'Development Tools' && sudo dnf install curl file git

    ###--------- On CentOS/RHEL ---------
    $ sudo yum groupinstall 'Development Tools' && sudo yum install curl file git

Once the dependencies installed, you can use the following script to install Linuxbrew package
in /home/linuxbrew/.linuxbrew (or in your home directory at ~/.linuxbrew) as shown.

$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

Next, you need to add the directories to your PATH

- /home/linuxbrew/.linuxbrew/bin - (or ~/.linuxbrew/bin)
- /home/linuxbrew/.linuxbrew/sbin (or ~/.linuxbrew/sbin)

And to your bash shell initialization script ~/.bashrc as shown:

    $ echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin/:$PATH"' >>~/.bashrc
    $ echo 'export MANPATH="/home/linuxbrew/.linuxbrew/share/man:$MANPATH"' >>~/.bashrc
    $ echo 'export INFOPATH="/home/linuxbrew/.linuxbrew/share/info:$INFOPATH"' >>~/.bashrc

Then source the ~/.bashrc file for the recent changes to take effect.

    $ source  ~/.bashrc

## How to Uninstall Linuxbrew in Linux

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/uninstall)"

# Formula Cookbook

https://docs.brew.sh/Formula-Cookbook.html

## How to build a new formula

    $ brew create https://example.com/foo-0.1.tar.gz


# Using Linuxbrew

For example you can install the gcc package (or formula) with the following command.
Take note of some of the messages in the output, there are some useful environmental variables that you need to set for some formulae to work correctly.

    $ brew help
    $ brew update         === download the newest version of homebrew from GitHub
    $ brew cleanup        === clean already install used downloaded

    $ brew install gcc

    ### To list all installed formulae, run.
    $ brew list

    ### You can uninstall a formula using following command.
    $ brew uninstall gcc

    ### You can search for packages using the following syntax.
    $ brew search    				#show all formulae
    OR
    $ brew search --desc <keyword>		#show a particular formulae

## Interesting Taps & Forks

We can find tag reps from here:
https://github.com/topics/homebrew

Or you can [create your own taps](https://robdalton.me/create-your-own-brew-package/).

For examples, like:
- goreleaser/goreleaser (4.2k) Deliver Go binaries as fast and easily as possible

A tap is Homebrew-speak for a Git repository containing extra formulae.
Homebrew has the capability to add (and remove) multiple taps to your local installation
with the `brew tap` and `brew untap` commands.
Type `man brew` in your terminal.
The main repository at <https://github.com/Homebrew/homebrew-core>, often called `homebrew/core`, is always built-in.

brew tap adds more repositories to the list of formulae that brew tracks, updates, and installs from.
By default, tap assumes that the repositories come from GitHub, but the command isn’t limited to any one location.

    $ brew tap
    domt4/crypto
    homebrew/core

    $ brew untap domt4/crypto

## How do I install these formulae?

    $ brew tap domt4/crypto
    $ brew install <formula>

    ### You can also install via URL:
    $ brew install https://raw.githubusercontent.com/DomT4/homebrew-crypto/master/Formula/<formula>.rb

## Troubleshooting:

1. First, please run `brew update` and `brew doctor`.

2. If you encounter any errors, feel free to file an issue.
A `brew gist-logs <formula>` is often handy. Thanks!

3. patch yourself

For example, when we install curl +TLS1.3, and found nghttp2 compile error,
    also there have a patch to fix that error, we can change the formulae like this:

```diff
    $ brew edit DomT4/crypto/curl-max

    diff --git a/Formula/curl-max.rb b/Formula/curl-max.rb
    index 1eed9eb..110ad14 100644
    --- a/Formula/curl-max.rb
    +++ b/Formula/curl-max.rb
    @@ -34,6 +34,14 @@ class CurlMax < Formula
       resource "nghttp2" do
         url "https://github.com/nghttp2/nghttp2/releases/download/v1.38.0/nghttp2-1.38.0.tar.xz"
         sha256 "ef75c761858241c6b4372fa6397aa0481a984b84b7b07c4ec7dc2d7b9eee87f8"
    +
    +    unless OS.mac?
    +      patch do
    +        # Fix: shrpx_api_downstream_connection.cc:57:3: error: array must be initialized with a brace-enclosed initializer
    +        url "https://gist.githubusercontent.com/iMichka/5dda45fbad3e70f52a6b4e7dfd382969/raw/19797e17926922bdd1ef21a47e162d8be8e2ca65/nghttp2?full_index=1"
    +        sha256 "0759d448d4b419911c12fa7d5cbf1df2d6d41835c9077bf3accf9eac58f24f12"
    +      end
    +    end
       end

       resource "libssh2" do
```

## example

Your taps are Git repositories located at `$(brew --repository)/Library/Taps`.
```sh
    $ brew tap "Homebrew/brew"
        Same as:
        $ git clone https://github.com/Homebrew/brew /home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/homebrew/homebrew-brew --depth=1
            Cloning into '/home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/homebrew/homebrew-brew'...
            remote: Enumerating objects: 1877, done.
            remote: Counting objects: 100% (1877/1877), done.
            remote: Compressing objects: 100% (1704/1704), done.
            remote: Total 1877 (delta 188), reused 781 (delta 96), pack-reused 0
            Receiving objects: 100% (1877/1877), 1.98 MiB | 6.05 MiB/s, done.
            Resolving deltas: 100% (188/188), done.
    $ brew tap
        domt4/crypto     <=== Used to install curl +TLS1.3 by 'brew install DomT4/crypto/curl-max',
                              and the really url is https://github.com/DomT4/homebrew-crypto, so "homebrew-" is default prefix.
                              If you found there have some error, you just edit the formulae by `brew edit DomT4/crypto/curl-max`
        homebrew/brew
        homebrew/cask
        homebrew/core
    $ brew install vim                     # installs from your custom repository
    $ brew install homebrew/core/vim       # installs from homebrew/core
```

## What Packages Are Available?

- Type `brew search` for a list all formulae.
- Or visit [formulae.brew.sh](https://formulae.brew.sh/formula/) to browse packages online.
- Or use brew search --desc <keyword> to browse packages from the command line.

### Unsupported interesting taps
*   [varenc/ffmpeg](https://github.com/varenc/homebrew-ffmpeg): A tap for FFmpeg with additional options, including nonfree additions.

*   [denji/nginx](https://github.com/denji/homebrew-nginx): A tap for NGINX modules, intended for its `nginx-full` formula which includes more module options.

*   [InstantClientTap/instantclient](https://github.com/InstantClientTap/homebrew-instantclient): A tap for Oracle Instant Client. The packages need to be downloaded manually.

*   [osx-cross/avr](https://github.com/osx-cross/homebrew-avr): GNU AVR toolchain (Libc, compilers and other tools for Atmel MCUs, useful for Arduino hackers and AVR programmers).

*   [petere/postgresql](https://github.com/petere/homebrew-postgresql): Allows installing multiple PostgreSQL versions in parallel.

*   [titanous/gnuradio](https://github.com/titanous/homebrew-gnuradio):  GNU Radio and friends running on macOS.

*   [dunn/emacs](https://github.com/dunn/homebrew-emacs): A tap for Emacs packages.

*   [sidaf/pentest](https://github.com/sidaf/homebrew-pentest): Tools for penetration testing.

*   [osrf/simulation](https://github.com/osrf/homebrew-simulation): Tools for robotics simulation.

*   [brewsci/bio](https://github.com/brewsci/homebrew-bio): Bioinformatics formulae.

*   [davidchall/hep](https://github.com/davidchall/homebrew-hep): High energy physics formulae.

*   [lifepillar/appleii](https://github.com/lifepillar/homebrew-appleii): Formulae for vintage Apple emulation.

### Unsupported interesting forks

*   [mistydemeo/tigerbrew](https://github.com/mistydemeo/tigerbrew): Experimental Tiger PowerPC version.

# Howtos

## Install by version

```sh
  ### 1) Check, whether the version is already installed (but not activated)
    $ brew info postgresql
    ### if the version is already exist, just switch
    $ brew switch postgresql 9.1.5
    $ brew info postgresql

  ### 2) Check, whether the version is available as a tap
    $ brew search postgresql
    $ brew tap homebrew/versions
    $ brew install postgresql@8

  ### 3) Try some formula from the past
    #$ brew versions postgresql

    ### To find SHA from commit log
    $ brew log tmux
    $ brew uninstall tmux

    $ brew install tmux --commit=<COMMIT-SHA>
    <or>
    $ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/<COMMIT-SHA>/Formula/tmux.rb
  ### 4) Pin the version
    $ brew pin tmux
    $ brew list --pinned
```

# troubleshooting

## fix compile error: install curl with TLS1.3 supported

When we want to install curl with TLS1.3,

    $ brew install DomT4/crypto/curl-max
Found there have compile error for nhttp2 lib

    ### disable nghttp
    $ brew edit DomT4/crypto/curl-max

Found there have compile error for libldap
    ### add --disable-ldap to curl's config
    $ brew edit DomT4/crypto/curl-max

    $ brew link --overwrite --dry-run curl-max

Check by:
      curl -kvvv https://www.tired.com --tlsv1.3

