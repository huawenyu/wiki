github-hub

https://hub.github.com/

# hub: USE GITHUB FROM THE COMMAND-LINE

hub is an extension to command-line git that helps you do everyday GitHub tasks without ever leaving the terminal.

## Install

```sh
   # Homebrew/Linuxbrew: install the latest release
   $ brew install hub

   # Other platforms: fetch a precompiled binary release, or
   # build your own from source.

   $ hub version
   git version 2.20.1
   hub version 2.7.0 # ← it works!
```

## As a contributor to open-source
Whether you are beginner or an experienced contributor to open-source, hub makes it easier to fetch repositories, navigate project pages, fork repos and even submit pull requests, all from the command-line.

```sh
    # clone your own project
    $ hub clone dotfiles
       → git clone git://github.com/YOUR_USER/dotfiles.git

    # clone another project
    $ hub clone github/hub
       → git clone git://github.com/github/hub.git

    # open the current project's issues page
    $ hub browse -- issues
       → open https://github.com/github/hub/issues

    # open another project's wiki
    $ hub browse mojombo/jekyll wiki
       → open https://github.com/mojombo/jekyll/wiki

    # Example workflow for contributing to a project:
    $ hub clone github/hub
    $ cd hub
    # create a topic branch
    $ git checkout -b feature
    # make some changes...
    $ git commit -m "done with feature"

    # It's time to fork the repo!
    $ hub fork --remote-name=origin
       → (forking repo on GitHub...)
       → git remote add origin git@github.com:YOUR_USER/hub.git

    # push the changes to your new remote
    $ git push origin feature
    # open a pull request for the topic branch you've just pushed
    $ hub pull-request
       → (opens a text editor for your pull request message)
```

### As someone who loves automation

Scripting your workflows is much easier now that you can list and create issues, pull requests, and GitHub releases.

```sh
    # List issues assigned to you that are labeled "urgent"
    $ hub issue -a YOUR_USER -l urgent

    # List the URLs of at most 20 PRs based on "develop" branch:
    $ hub pr list -L 20 -b develop --format='%t [%H] | %U%n'

    # Create a GitHub release with notes from a file and copy the URL to clipboard:
    $ hub release create -c -F release-notes.txt v2.3.0
```

## As an open-source maintainer

    Maintaining a project is easier when you can easily fetch from other forks, review pull requests and cherry-pick URLs. You can even create a new repo for your next thing.

```sh
    # fetch from multiple trusted forks, even if they don't yet exist as remotes
    $ hub fetch mislav,cehoffman
       → git remote add mislav git://github.com/mislav/hub.git
       → git remote add cehoffman git://github.com/cehoffman/hub.git
       → git fetch --multiple mislav cehoffman

    # check out a pull request for review
    $ hub pr checkout 134
       → (creates a new branch with the contents of the pull request)

    # directly apply all commits from a pull request to the current branch
    $ hub am -3 https://github.com/github/hub/pull/134

    # cherry-pick a GitHub URL
    $ hub cherry-pick https://github.com/xoebus/hub/commit/177eeb8

    # open the GitHub compare view between two releases
    $ hub compare v0.9..v1.0

    # put compare URL for a topic branch to clipboard
    $ hub compare -u feature | pbcopy

    # create a repo for a new project
    $ git init
    $ git add . && git commit -m "It begins."
    $ hub create -d "My new thing"
       → (creates a new project on GitHub with the name of current directory)
    $ git push origin master
```

## Using GitHub for work

Save time at work by opening pull requests for code reviews and pushing to multiple remotes at once. Even GitHub Enterprise is supported.

```sh
    # whitelist your GitHub Enterprise hostname
    $ git config --global --add hub.host my.example.org

    # open a pull request using a message generated from script, then put its URL to the clipboard
    $ git push origin feature
    $ hub pull-request -c -F prepared-message.md
       → (URL ready for pasting in a chat room)

    # push to multiple remotes
    $ hub push production,staging
```

