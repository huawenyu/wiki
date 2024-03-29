# QuickStart

[Svn Doc][2]

```
                                     "file://$(pwd)/git-code-dir"
                                             |
$ git clone --depth 1 --single-branch file:///home/wilson/workref/fos-git [new-dir-name]
```

## config password local

```
$ vi ~/.netrc
machine github.com
       login yourusername
       password yourpassword
machine gitlab.com
       login yourusername@mail
       password yourpassword
```

# Command


Next we'll take a look at some commands that you will need for working.
Following is a list of the common svn commands that we use all the time and their analogs in git.

## svn

### ignore

```ini
$ cat .subversion/config

[miscellany]
global-ignores = *.o *.lo *.la *.al .libs *.so *.so.[0-9]* *.a *.pyc *.pyo __pycache__
   *.rej *.orig *.diff *~ #*# .#* .*.swp .DS_Store
   .rb_genco .gdb_history .gdb.break
   tage tags tagx .tage .tags .tagx
```

### Routine

    svn checkout http://remote local-dir
    svn up
    … modify …
    svn diff
    svn commit -m "new feature"
    svn revert -R .

### Create repository

    svnadmin create ~/myrep

    vi ~/myrep/conf/svnserve.conf
    vi ~/myrep/conf/passwd

    svn mkdir  <dir>
    svn import  <file>
    svnserve -d

### Clone remote repository

    svn checkout -r<revision> <URL>

### [backup whole repository][4]

    svnadmin dump -q /path/to/repo | bzip2 -9 > filename.bz2
    svnadmin dump /var/www/svn/testrepo | gzip -9 > /backups/testrepo.dump.gz
    svnadmin load /var/www/svn/testrepo < /backups/testrepo.dump

### List repository info

    svn info

### Update/Pull

    svn update

### New branch

    svn copy URL/trunk URL/branches/5.x/trunk
    svn copy URL/branches/5.x/trunk URL/branches/5.x/5.0/trunk

### Submit

    svn commit -m ‘message’

### Add/Del/Rename

    svn add|delete|rm

### Conflict

    svn status | grep -E '^.{0,6}C'
    <or>
    svn status | egrep '^.{0,6}C'

### Check changed

    svn diff
    svn diff --diff-cmd='meld'

### Merge

    When trying to merge a feature branch into trunk:

    $ svn co https://foo.bar.com/subversion/project/trunk project
    $ cd project
    $ svn merge https://foo.com/subversion/project/trunk https://foo.com/subversion/project/branches/feature1
    $ svn st

    If there are any conflicts, you can resolve them with:

        ... edit the conflict files, ...
    $ svn resolve --accept=working <file-1>
    $ svn resolve --accept=working <file-2>

    Commit the changes:
    $ svn commit -m "Merged DEV to trunk."

### Status

    svn -q st
    svn status

### Clean for rebuild

    svn cleanup . --remove-unversioned

Old svn version use the 'status' to implement like:
Should add option `--no-ignore` and check two beginwith characters 'I', '?'.

```sh
    $ svn st --no-ignore | grep '^?' | wc -l
    2591
    $ svn st --no-ignore | grep '^[I?]' | wc -l
    5009
    $ svn st | grep '^[I?]' | wc -l
    2591

    svn st --no-ignore | awk '/^[I?]/{print $2}' | xargs rm -rf
    svn status --no-ignore | grep '^[I?]' | cut -c 9- | while IFS= read -r f; do rm -rf "$f"; done

    ### svn status | egrep '^\?' | cut -c 8- | xargs rm
    ### svn status | grep ^\? | cut -c 9- | xargs -d \\n rm -r     <<< It handles unversioned folders and spaces in filenames
```

### Log Search & historical

    svn log
    svn log -q file | grep '^r' | cut -f1 -d' '

### View old version file

    svn update -r 666 file <<< checkout that version of the file
    svn cat -r 666 file | less <<< just view the file directly

### Blame

    svn blame -- <file>

### Revert & Discard changes

    svn revert <file>
    svn revert -R .		# flush all changes

### Tag

    svn tag

## Git

### ignore

```ini
$ cat .gitignore_global

Session.vim
session.vim
Default.vim
default.vim
log.*
patch.*
tage
tags
tagx
.tage
.tags
.tagx
*.orig
*.rej
.gdb_history
migadmin/node_modules/grunt-jscs/*
```

### Routine

[Doc][3]

```
    git clone --depth 3 git://some/repo myshallowcopyrepo
    git pull --all

    git checkout -b upstream origin/upstream	# trace remote branch
    git checkout -b new_feature

    git checkout master		# first, update from the remote trunk
    git svn rebase		# update it to HEAD

    git checkout bug123		# next, branch feature rebase
    git rebase master		# bug123 on top of master

    ... implement feature ...

    git checkout master		# merge feature to trunk
    git merge bug123		# this should be a fast-forward

    git add file4		# only add the changes from some file
    <or> git add -i file2	# only add part of changes from some file

    git diff			# show uncommitted changes
    git diff --cached		# show the added changes for next commit

    git commit -m "commit message"

    git checkout master
    git merge new_feature	# merge into master
    git commit -am "more modify"

    git log v2.43.. mydir	# view changes since 2.43 tag.


    $ git log -p ORIG_HEAD.. dir <<< look at the changes done upstream since last time we checked
    $ git pull URL ALL <<< fetch from a specific branch from a specific repository and merge
    $ git reset --hard ORIG_HEAD <<< revert the pull
    $ git gc <<< garbage collect leftover objects from reverted pull
    $ git fetch --tags <<< obtain official tags from the origin and store them under .git/refs/tags/.
```

### Create repository

    $ tar zxf frotz.tar.gz
    $ cd frotz

    $ git init
    $ git add . <<< add everything under the current directory
    $ git commit -m "Init"
    $ git tag -s -m "GIT 0.99.9x" v0.99.9x   <<< make a lightweight, unannotated tag

### Clone remote repository

    git clone <URL>

    # get the last n revisions
    git clone --depth 3 git://some/repo myshallowcopyrepo

    git clone --depth=1 file:////home/wilson/work/fos_git  fos_study
    git clone -b 0198879-url-match-config --no-hardlinks /home/wilson/work/fos/.git	# clone local git reposition

    # clone local reps
    git clone fos-git fos-git-5.2
    cd fos-git-5.2; vi .git/config		# change origin url to remote

### Clone directly from local filesystem

```
    ==clone==
    $  git clone --depth 1 --single-branch file:////home/wilson/workref/fos-git    <<< Quickest


    $ git clone ssh://username@host.xz/absolute/path/to/repo.git/     <<< forward slash for absolute path on server
    <OR>
    $ git clone username@host.xz:relative/path/to/repo.git/                <<< a colon (it mustn't have the ssh:// for relative path on server (relative to home dir of username on server machine)


    ==push,pull==
    On the client machine you can push your repo to the server.
    $ git remote add origin ssh://user@server:/GitRepos/myproject.git
    $ git push origin master
```

### backup whole repository

    git bundle create /tmp/repo-proj --all
    git clone /tmp/repo-proj newFolder


### create patch

#### patch和diff 的区别

Git 提供了两种补丁方案，一是用git diff生成的UNIX标准补丁.diff文件，二是git format-patch生成的Git专用.patch 文件。
  - .diff文件只是记录文件改变的内容，不带有commit记录信息,多个commit可以合并成一个diff文件。
  - .patch文件带有记录文件改变的内容，也带有commit记录信息,每个commit对应一个patch文件

#### commands
    ==from branch==
    git checkout -b feature1
    git format-patch master --stdout > fix_feature1.patch


    ==from commit==
    git format-patch HEAD~5
    git format-patch -2 --stdout > patch.diff   # merge the last 2 commits into one patch file
    <OR>
    git format-patch commit-id-start..commit-id-end

    ==apply==
    git apply --stat fix_feature1.patch     # check patch file status
    git apply --check fix_feature1.patch	# dry-run to check the patch can patched succ or not
        ==resolve conflict==
        ###if fail, we should back to conflict resolve status:
        git am newpatch.patch
        git am --skip
        git am --abort

        git am --continue       <=== finally, commit it.

    ==apply & commit==
    git am --signoff file.patch			# commit the patch with original author information
    <OR>
    git apply fix_feature1.patch		# apply the changes, not commit them.

    ==troubleshoot==
    git rebase -i HEAD~5			# will open an editor: select or delete commits that you want

### List repository info

    cat .git/config
    git remote show origin

### Update/Pull

    git pull --all

### Branch

#### Checkout to local
    git checkout -b my-new-feature
    git branch -m <oldname> <newname>		# rename

    # branch from a spicific commit
    git branch <branch-name> <sha1-of-commit>
    git checkout -b <branchname> <sha1-of-commit or HEAD~3>

    # Easily track a remote branch
    git checkout -t origin/feature

    # Fetch all of the remote branches
    git fetch origin

    # List all branch local & remote
    git branch -v -a

    # Checkout a branch to local
    git checkout -b test origin/test

#### Link local branch to remote branch

    # Make an existing Git branch track a remote branch: Given a branch `foo` and a remote upstream
    git branch -u upstream/foo foo

#### Create remote branch

    # push local remote branch to remote
    git push origin <branch-name>

### Submit

    git commit -am 'message'

### Add/Del/Rename

    git add|delete|rm

### Search & Log

    git log -- foo.py bar.py		# by file

#### Log Search & historical

    git log
    git log -3
    git log --after="2014-7-1"		# by date
    git log --after="2014-7-1" --before="2014-7-4"
    git log --author="John"		# by author
    git log --author="John\|Mary"

    git log --grep="JRA-224:"		# by commit message, -i ignore case
    git log --grep="foo" --grep="bar"               # or
    git log --grep="foo" --grep="bar" --all-match   # and

    git log -- foo.py bar.py		# by files
    git log -S"Hello, World!"		# by patch content
    git log master..feature		# by range

    git log -p filename			# with diff file
      --stat xxxxxxx..xxxxxxx
      --name-status
      --name-only
      --since "10 Sep 2012" --until "12 Nov 2012" --stat


### Check changed

    git diff
    git difftool -t meld b3dc7d75~1 b3dc7d75

### Merge

    git merge|rebase

### Status

    git status

### Clean for rebuild

    sudo git clean -nxd
    sudo git clean -fxd

    sudo git clean -nxd -e "log*" -e "cscope*" -e "patch*" -e "commit*" -e ".git*" -e "change*"      # dry-run to check with grep or some others
    sudo git clean -fxd -e "log*" -e "cscope*" -e "patch*" -e "commit*" -e ".git*" -e "change*"      # really remove files

### View old version file

    git show <SHA>:<file>

### Blame

    git blame <SHA> -- <file>    <<< use --follow to make blame follow renames

#### Vim Plugin - Fugitive: Gblame reblame options

https://stackoverflow.com/questions/25286726/vim-fugitive-gblame-reblame-options

    ref~ is shorthand for ref~1 and means the commit's first parent.
    ref~2 means the commit's first parent's first parent.
    ref~3 means the commit's first parent's first parent's first parent. And so on.

    ref^ is shorthand for ref^1 and means the commit's first parent.
    But where the two differ is that ref^2 means the commit's second parent (remember, commits can have two parents when they are a merge).

Think of reblame as navigating to a commit and then running blame on your file or `git blame <commit> -- <file>`

* `-` the simplest case. Use the commit in question under your cursor and reblame the file.
* `~` Is equivalent to running  `git blame <rev>~[count] -- <file>`
* `P` Is equivalent to running  `git blame <rev>^[count] -- <file>`

For the common case, i.e. no `[count]`, `~` and `P` are the equivalent. (Note that `[count]` defaults to 1)

Quick revision tutorial taken from `git help gitrevisions`:

    Here is an illustration, by Jon Loeliger.
    Both commit nodes B and C are parents of commit node A (usually as `HEAD`).
    Parent commits are ordered left-to-right.

    G   H   I   J
     \ /     \ /
      D   E   F      <=== `B^3`: F is B's third-parent
       \  |  / \
        \ | /   |
         \|/    |
          B     C    <=== `A^2`: C is A's second-parent
           \   /
            \ /
             A (`HEAD`)

    A =      = A^0
    B = A^   = A^1     = A~1
    C = A^2  = A^2
    D = A^^  = A^1^1   = A~2
    E = B^2  = A^^2
    F = B^3  = A^^3
    G = A^^^ = A^1^1^1 = A~3
    H = D^2  = B^^2    = A^^^2  = A~2^2
    I = F^   = B^3^    = A^^3^
    J = F^2  = B^3^2   = A^^3^2



### Revert & Discard changes

    git checkout HEAD [filenames or directories]

    git checkout .		# revert changes of working copy
    git checkout -- <file>
    git reset			# revert changes of made to index

    git revert ...		# revert change that have committed

    git clean -f		# remove all untracked files (e.g., new files, generated files)
    git clean -d		# remove all untracked directories


### Branch info

    git branch -a    <<< show all branch
    git branch -r    <<< only show remote branch

    =link with same name=
    git checkout -t origin/feature    <<< track remote branch as local
    git branch -u upstream/foo

    =link with diff name=
    git branch --track feature1 origin/feature    <<< if want another name
    git branch -u upstream/foo foo

### Tag

    git tag

### Stash

    $ git stash
    ...
    $ git stash pop

    =stash detail=
    git stash [save [message] ]
    git stash list
    git apply stash@{0}
    git stash drop stash@{0}

    =stash revert=
    git stash show -p stash@{0} | git apply -R


## git-svn

### QuickStart

    # If use "-r r465327:HEAD" will fail
    git svn clone --prefix=svn/ -r465327:HEAD http://.../svn/FortiCache/trunk
    git svn clone -r HEAD http://.../trunk	# only checkout the last version

    git svn rebase				# like: svn update
    git commit -am "more modify"


    git rebase -i HEAD~10			# squash more commit into one or two
    git svn dcommit				# send the git commits to svn remote

### Create repository


### Clone remote repository

    # get the last serveral revisions
    git svn clone -r65000:HEAD <URL> my-dev

    <OR>
    # -s svn repos have normal layout, such as trunk, branches, tags
    git svn init -s <URL>

    git svn fetch			# fetch all version history from svn-repository
    git svn fetch -r <rev>

### List repository info

    git svn info


### Update/Pull

    git svn rebase


### Submit

    git svn dcommit -m 'message'


# Git

## Empty commit
That means you are pushing a different history than the one others might have already cloned.
If you are sure that won't be a problem, you need to force the push:

    // $ git push -f origin master
    $ git commit --allow-empty

You would have created a new (empty) commit, which you could have pushed without any issue.


## Read the log grah

    git log -n 10 --graph --pretty="%h %ad %s(%an)" --date=short
    git log --graph --oneline --date-order --decorate --color --all

    Another interesting thing you can do is visualize the commit graph with the '--graph' option, like so:
    $ git log --pretty=format:'%h : %s' --graph
    * 2d3acf9 : ignore errors from SIGCHLD on trap
    *   5e3ee11 : Merge branch 'master' of git://github.com/dustin/grit
    |\
    | * 420eac9 : Added a method for getting the current branch.
    * | 30e367c : timeout code and tests
    * | 5a09431 : add timeout protection to grit
    * | e1193f8 : support for heads with slashes in them
    |/
    * d6016bc : require time for xmlschema
    It will give a pretty nice ASCII representation of the commit history lines.

    ===========================================================================

    The asterisks show where something was committed:
      - e1193f8, 5a09431 and 30e367c were committed to the left branch (yielding a | on the right branch)
      - whereas 420eac9 was committed to the right branch (yielding a | on the left branch).
      - And that is what 420eac9 does different from the rest:
         it's the only commit to the right branch.

    For the sake of completeness:
      - d6016bc was the branching point
      - 5e3ee11 is the merging commit
      - 2d3acf9 is the first commit after merging


## Git notes (used as TODOS)

### git notes add

    $ git notes add HEAD
    $ git notes add -m 'I approve - Scott' master~1
    $ git log master
    Notes:
      I approve - Scott
    $ git notes edit master~1


    git notes new namespace for default namespace ‘commits’
    $ git notes --ref=bugzilla add -m 'bug #15' 0385bcc3       <<< add new notes to a specific namespace, if not exist, create the new notes namespace.
    $ git log --show-notes=bugzilla             <<< show notes at specific namespace, not the only ‘commits’
    $ git log -1 --show-notes=*                   <<< show notes from all namespace, not only namespace ‘commits’


### git push notes

    $ git push origin refs/notes/bugzilla      <<< push a specific notes namespace
    $ git push origin refs/notes/*                 <<< push all notes namespace, the same as: $ git push origin --tags it basically expands to git push origin refs/tags/*.
    $ git fetch origin refs/notes/*:refs/notes/*


    git push notes using config
    [remote "origin"]
      fetch = +refs/heads/*:refs/remotes/origin/*
      url = git@github.com:schacon/kidgloves.git
      fetch = +refs/notes/*:refs/notes/*


## Git Config

### Git Config global

```
$ git config --global user.name "Your Name"
$ git config --global user.email "yname@you.com"
$ git config --global core.excludesfile '~/.gitignore'

$ git config --global core.autocrlf true                <<< Run these git setup commands to avoid choking on Windows newlines
$ git config --global user.name "My Name"
$ git config --global user.email me@mydomain.com
$ git config --global diff.noprefix true
$ git config --global color.diff auto
$ git config --global color.status auto
$ git config --global color.branch auto
$ git config --global color.grep auto
$ git config --global color.interactive auto
$ git config --global color.ui auto

$ cat ~/.gitconfig
[user]
        name = My Name
        email = me@mydomain.com
[color]
        diff = auto
        status = auto
        branch = auto

[remote "mw.com"]
        url = ssh://mydomain.com/home/myusername/shared/myproject.git

$ cat .gitignore
*
!*/
!Makefile
!*.[ch]

[sample2]
*
!*/**/migbase/
!*/**/daemon/wad/
!*/**/daemon/miglogd/
!Makefile
!*.[ch]

```

### Git Config local

    $ git config --bool core.bare true          <<< Solve local bare repository push fail
    $ git config --unset core.bare              <<< fatal: This operation must be run in a work tree

## Git bundle backup repository

    $ git bundle create repo.bundle --all

    # Create lightweight repos only have one commit log
    $ git bundle create ~/git_fch_repos master 852478174                <=== SHA is the last commit.

    $ git clone repo.bundle

## Git workflow

    $ git remote
    $ git remote update
    $ git remote show origin		# repositon info, like svn info
    $ git remote

    $ git remote add pb git://github.com/paulboone/ticgit.git
    $ git remote -v
      origin        git://github.com/schacon/ticgit.git
      pb        git://github.com/paulboone/ticgit.git
    $ git fetch pb				# the trunk <master>: pb/master
    $ git pull --all


    fetch remote server’s git branch:
    git branch -l -r    #list remote branch, choose what you want
    git branch test origin/test
    git checkout test
    git pull
    <or>
    git fetch origin             # fetch all branch into local if you want.
    get checkout -b test origin/test      # relate local branch to remote branch


## pull vs fetch

    $ git pull,  like git fetch + git merge
    $ git fetch + git rebase

## merge vs rebase

Merge takes all the changes in one branch and merge them into another branch in a new commit log.
Rebase says I want the point at which I branched to move to a new starting point

  - merge will append a new log action.
  - rebase just move the commit-log, but no create a new.

So when do you use either one?

### Merge

Let's say you have created a branch for the purpose of developing a single feature.
When you want to bring those changes back to master,
you probably want merge (you don't care about maintaining all of the interim commits).

### Rebase

A second scenario would be if you started doing some development
and then another developer made an unrelated change.
You probably want to pull and then rebase to base your changes from the current version from the repo.


### experimented with a test repository

It's simple, with rebase you say to use another branch as the new base for your work so...

If you have for example a branch `master` and you create a branch to implement a new feature,
say you name it `cool-feature`, of course the master branch is the base for your new feature.

Now at a certain point you want to add the new feature you implemented backto the master branch.
You could just switch to master and merge the cool-feature branch:

    $ git checkout master
    $ git merge cool-feature

but this way a batch of commit-logs for your `cool-feature` will be added to `master`,
if you want to avoid spaghetti-history and of course be sexier you can rebase:

    $ git checkout master
    $ git rebase cool-feature

Alternatively if you want to resolve conflicts in your topic branch as VonC suggested you can rebase you branch this way:

    $ git checkout cool-feature
    $ git rebase master

and then merge it backto master:

    $ git checkout master
    $ git merge cool-feature

This time, since the topic branch has the same commits of master plus the commits with the new feature,
the merge will be just a fast-forward ;)


## fetch vs pull

    more safe, cause we can check status before merge
    git fetch origin master
    git log -p master..origin/master
    git merge origin/master

    <OR>

    git fetch origin master:tmp
    git diff tmp
    git merge tmp
    $ git pull        <<< fetch+merge
    git pull origin master


## rollback: reset vs revert

### How can I rollback to a special commit?

    // I have 2 commits that I did not push:
    // How can I roll back my first one (the oldest one), but keep the second one?
    $ git status
    $ git log
      commit 3368e1c
      ...
      commit baf8d5e

    // Do I just need to do:
    $ git reset --hard baf8d5e


### How can I rollback the last commit

### only committed but not `git push origin master`

#### Discard the last-commit changes

    git reset --hard HEAD~1

HEAD~1 is a shorthand for the commit before head.
Note that when using --hard any changes to tracked files in the working tree since the commit before head are `lost`.

#### Rollback the last-commit-log but keep changed in the working tree

    git reset --soft HEAD~1

### Have already `git push origin master`

`This will create a new commit that reverses everything introduced by the accidental commit.`

    git revert HEAD


### Revert vs Checkout vs Reset?

  - `revert` is used to undo a previous pushed commit.
      In git, you can't alter or erase an earlier commit. (Actually you can, but it can cause problems.)
      So instead of editing the earlier commit, revert introduces a new commit that reverses an earlier one.
  - `reset` is used to undo changes in your working directory or undo the index that comitted but haven't pushed yet:
      It actually does a couple of different things depending on how it is invoked.
      It modifies the index (the so-called "staging area"). Or it changes what commit a branch head is currently pointing at.
      This command may alter history (by changing the commit that a branch references).
  - `checkout` is used to copy a file from some other commit to your current working tree. It doesn't automatically commit the file.


### revert all local changes

    git checkout .	# If you want to revert changes made to your working copy
    git reset		# If you want to revert changes made to the index (i.e., that you have added)
    git revert ...	# If you want to revert a change that you have committed


### revert vs reset

    $ git reset --hard HEAD
    $ svn revert foo.c		# rollback changes to a file
    $ svn revert -R .		# rollback a whole directory of files


    git revert ...		# rollback a committed change, and also can 'redo'
    git checkout -- .		# rollback the working copy: drop changes in the tree, but keep changed in index.
    git reset			# rollback changed in the index, can be recovery by 'git reflog'


    # Rollback current branch head to <commit> including index and working-tree,
    which depend on <mode> = "--mixed"[default]:

    git reset [<mode>] [<SHA1>]
      --soft		# Does not touch the index file nor the working tree
      --mixed		# rollback the index but not the working tree
      --hard		# rollback the index and working tree, should be done with care, as it cannot be undone.
      --merge		# rollback the index and updates the files in the working tree
      --keep		# rollback the index and updates files in the working tree that are different between <commit> and HEAD

### checkout vs. reset

  * A commit holds a certain state of a directory and a pointer to its antecedent commit.
  * A commit is identified by a so-called ref looking something like 7153617ff70e716e229a823cdd205ebb13fa314d.
  * HEAD is a pointer that is always pointing at the commit you are currently working on. Usually, it is pointing to a branch which is pointing to that commit.
  * Branches are nothing but pointers to commits. You are 'on a branch' when HEAD is pointing to a branch.

#### checkout

  git checkout <commit> <paths> tells git to replace the current state of paths with their state in the given commit.
  * paths can be files or directories.
  * If no branch (or commit hash, see basic facts) is given, git assumes the HEAD commit.
     * –> git checkout <path> restores path from your last commit. It is a 'filesystem-undo'.
  * If no path is given, git moves HEAD to the given commit (thereby changing the commit you're sitting and working on).
     * –> git checkout branch means switching branches.

  * Example:
      * git checkout HEAD~2 app/models/foo.rb drops all modifications of foo.rb
      * and replaces the file with its version two commits ago.

#### reset

  git reset <commit> re-sets the current pointer to the given commit.

  * If you are on a branch (you should usually be), HEAD and this branch are moved to commit.
  * If you are in detached HEAD state, git reset does only move HEAD. To reset a branch, first check it out.

  * Example:
      * You are currently working upon commit 123abc.
      * After resetting to a previous commit xyz789 (e.g. with git reset HEAD~2),
      * you have no easy access to commit 123abc anymore,
      * because HEAD and the branch are both pointing to xyz789.
      * To move the branch pointer 'back to the front', you can't use git checkout, as it only moves HEAD.
      * You have to reset your branch to that commit: git reset 123abc.
      * (If you didn't save the first commit's hash (123abc), git reflog will help you finding it.)


### Using these commands


If a commit has been made somewhere in the project's history,
and you later decide that the commit is wrong and should not have been done,
then `git revert` is the tool for the job.
It will undo the changes introduced by the bad commit, recording the "undo" in the history.


If you have modified a file in your working tree, but haven't committed the change,
then you can use `git checkout` to checkout a fresh-from-repository copy of the file.


If you have made a commit, but haven't shared it with anyone else and you decide you don't want it,
then you can use `git reset` to rewrite the history so that it looks as though you never made that commit.


## Tags

    $ git tag <tagname>, Git will create a tag at the current revision but will not prompt you for an annotation. It will be tagged without a message.
    $ git tag -a <tagname>, Git will prompt you for an annotation unless you have also used the -m flag to provide a message.
    $ git tag -a -m <msg> <tagname>, Git will tag the commit and annotate it with the provided message.
    $ git tag -m <msg> <tagname>, Git will behave as if you passed the -a flag for annotation and use the provided message.

    $ git tag -m "Message for log" "my-tag-name"
    $ git log --pretty=oneline -3  // find SHA1
    $ git tag v1.0 ec32d32    // add
    $ git tag -a v1.2 9fceb02 -m "Message here"
    $ git tag -d v1.0              // delete
    $ git push origin --tags   // push to remote


## rebase conflict

    $ git status			# check the confict info
    $ vim app/models/user.c		# solve conflict
    $ git add app/models/user.rb
    $ git commit -c <id>
    rebase conflict
    $ git checkout master
    $ git pull
    $ git checkout your-feature
    $ git rebase master

    method 1:
    > git mergetool

    method 0:
    > git checkout --ours filename.c		# [this is the reposit master newer version, maybe need use this to use the master’s version, and copy your modify to this file]
    > git checkout --theirs filename.c		# [this is the your local repos version]
    > git add filename.c			# After you have solve the conflict
    > git rebase --continue


## Log & diff

    git log --after=jun9 --before=jun10

    git format-patch -1 <sha>
    git diff bbc2845 -- > patch.diff          # Difference between a git commit <SHA1> and the unstaged working directory

    git diff 66f93d7..f1ba363
    git diff --name-only SHA1 SHA2
    git diff --name-only HEAD~10 HEAD~5
    git log --name-status --oneline [SHA1 [SHA2]]
    git diff --name-status [SHA1 [SHA2]]
    $ git diff origin/master...HEAD
    $ git diff --name-status master..branch
    $ git diff --stat --color master..branchName
    $ git log --pretty=format:"%h - %an, %ar : %s"
      ca82a6d - Scott Chacon, 11 months ago : changed the version number
      085bb3b - Scott Chacon, 11 months ago : removed unnecessary test code
      a11bef0 - Scott Chacon, 11 months ago : first commit
    $ git log --oneline --graph --color --all --decorate
    $ git log --graph --decorate --date=relative --all --pretty='%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)'

### Git Diff Unstaged
Shows the changes between the Working Directory and the Staging Area:

$ git diff

### Git Diff Staged
Shows the changes between the Staging Area and the HEAD:

$ git diff --staged
- or -
$ git diff --cached
- or -
$ git status -v

### Create an alias git diffs, if you need to check these changed often:

$ git config --global alias.diffs 'diff --staged'

### Git Diff Staged and Unstaged

### Shows all the changes between the Working Directory and the HEAD:

$ git diff HEAD
- or -
$ git status -vv

### Create an alias git diffh, if you need to check these changed often:

$ git config --global alias.diffh 'diff HEAD'

## Search commit message

    $ git show :/fix
    $ git show :/^Merge
    # shows the last merge commit


## command compaire files


    $ diff -u -I 'revision' 5tr_40c/patch.diff 5tr/patch.diff | vim -		# compare two diff-files
      -u unified context,
      -I RE, ignore changes whose lines all match RE
      -p show which c function each change is in
      -w ignore all white space, -B ignore changes whose lines are all blank
      -D/--ifdef		# can generate enclose by #ifdef


## reflog vs log


    git reflog 可以查看所有分支的所有操作记录（包括（包括commit和reset的操作），包括已经被删除的commit记录，git log则不能察看已经删除了的commit记录
    具体一个例子，假设有三个commit， git st:
    commit3: add test3.c
    commit2: add test2.c
    commit1: add test1.c
    如果执行git reset --hard HEAD~1则 删除了commit3，如果发现删除错误了，需要恢复commit3，这个时候就要使用
    git reflog
     HEAD@{0}: HEAD~1: updating HEAD
    63ee781 HEAD@{1}: commit: test3:q
    运行git log则没有这一行记录
    可以使用git reset --hard 63ee781将红色记录删除，则恢复了cmmit3，运行git log后可以看到：
    commit3: add test3.c
    commit2: add test2.c
    commit1: add test1.c
    这里也可以使用另外一种方法来实现：git cherry-pick 63ee781


## view changes only for a branch?

    Assuming that your branch was created off of master :
    git cherry -v master
    or
    git log master..
    git log --no-merges master..
    If your branch was made off of origin/master, then say origin/master instead of master.
    but if you update the master, it’s hard to get diff-file just for your branch:
    git checkout new-branch
    ...after several commit...
    git log -n 3 --pretty=format:”%h%x09%an%x09%ad%x09%s”         # to find the commit hash-id just before this branch’s first commit
    0. what you should do is find diff between your newest commit with the commit before your oldest commit
    1. git log master.. --oneline                   # to find the oldest commit of your branch’s commit , assume it as ‘ad1123’
    2. git log ad1123~2..HEAD --oneline    # to find the commit before your oldest  commit, assume it as ‘ad0000’
    3. git diff ad0000..ad1123                    # this is the diff of your branch’s change


    git diff -U10|dwdiff --diff-input -c|less -R
    git diff -w   => ignore whitespace
    git diff -W   => show the context function
    git diff -U   => show more context before and after the diff-line
    dwdiff is another tools, you should install it before use, better than wdiff
    method 1
    1. git log master.. --oneline                   # to find the oldest commit of your branch’s commit , assume it as ‘ad1123’
    2. git log ad1123~2..HEAD --oneline    # to find the commit before your oldest  commit, assume it as ‘ad0000’
    3. git diff ad0000..ad1123                    # this is the diff of your branch’s change
    method 2
    or just use one command
    git --no-pager log --children -n6 HEAD --oneline
    make diff ignore some files or file’s lines according some pattern
    What you really want to do is to unset the diff attribute, not set it to a bogus command. Try this in your .gitattributes:
    Project.xcodeproj/* -diff
    or
    You may use an alias in your .git/config
    [alias]
            mydiff = !git diff | filterdiff -x "*/Project.xcodeproj/*"
    You need filterdiff (from patchutils) for this trick.
    sudo apt-get install patchutils
    Patchutils contains a collection of tools for manipulating patch files: interdiff, combinediff, flipdiff, filterdiff, fixcvsdiff, rediff, lsdiff, grepdiff, splitdiff, recountdiff, and unwrapdiff. You can use interdiff to create an incremental patch between two patches that are against a common source tree, combinediff for creating a cumulative diff from two incremental patches, and flipdiff to transpose two incremental patches. filterdiff is for extracting or excluding patches from a patch set based on modified files matching shell wildcards. lsdiff lists modified files in a patch. rediff, recountdiff, and unwrapdiff correct hand-edited (or otherwise broken) patches.




## Git/svn blame

### Svn blame

    if you want to check specific “match-str”, which can do like this way:
    svn blame --your-file-- | grep “match-str”
      5x  svn blame --your-file | grep match-str
     76846      kwang         struct some-struct *ptr;
     76846      kwang                         ptr = function();
    svn diff -c 76846 | vim -          <<< check the patch of this commit.
    ECO number


    $ svn blame <file> [-rXXX] | vim -        <<< find that modify lines, and the first field is the revision XXXX
    $ svn blame <file>[@XXX] | vim -        <<< find that modify lines, and the first field is the revision XXXX


    $ svn log -rXXXX                        <<< r101766 | hyu | 2013-08-29 12:12:24 -0700 (Thu, 29 Aug 2013) | 9 lines,
    hyu-5436-fix Explicit Proxy add/remove HTTP headers <<< the 5436 is eco-number


    Git blame
    http://zsoltfabok.com/blog/2012/02/git-blame-line-history/


    git blame --your-file-- | grep “match-str”   <<< find the commit SHA
    git show --sha-- | vim -
    “blame” a deleted line
    $ git log -S<string> -- file        <<< know the delete content
    $ git log -G<string> -- file         <<< same thing with regular expressions!
    $ git blame --reverse -- file        <<< Walk history forward instead of backward.
    $ git blame -L10,+1 fe25b6d^ -- src/options.cpp        <<< blame according line, and also start from a revision (instead of the default of HEAD); fe25b6d^is the parent of fe25b6d.
    todo list:
    two kind-of dir:  summit-dir, working-dir, please keep them update-sync as svn-update==git.master.HEAD
    working on your working-dir, add @todo @fixme @note @code, @test up to you, for example, you can add your code comment like this:
    //@note wad_vd: vdom config data
    //@note   - store: add into wad_vd_list and wad_vds-hashmap
    //@note   - iter:  wad_vd_iter[2]
    //@note   - pwd:   wad_vd_get_cur_vd()
    //@note   - find:  wad_vd_find/findname()




## apply patch failed


    $ git apply -v --check fix_empty_poster.patch
            error: patch failed: mm/vmalloc.c:469
            error: mm/vmalloc.c: patch does not apply
            Patch failed at file.patch.


    $ git apply --reject --whitespace=fix file.patch    <<<  By using “git apply” with the –reject it will apply the patch leaving bad files with “xxx.rej” in my case mm/Kconfig.rej was the culprit. I resolved the problem with mm/Kconfig. Next I tried “git am –resolved”:


    $ git am --resolved
    * Did you forget to use 'git add'?
    * When you have resolved this problem run "git-am --resolved".
    * If you would prefer to skip this patch, instead run "git-am --skip"


    rebase to a specific commit?
    You can avoid using the --onto parameter by making a temp branch on the commit you like and then use rebase in it's simple form:
    git branch temp master^
    git checkout topic
    git rebase temp
    git branch -d temp

## stage

  - Staging area gives the controll to make commit smaller.

    Just make one logical change in the code, add the changed files to the staging area and finally if the changes are bad then checkout to the previous commit or otherwise commit the changes.
    It gives the flexibility to split the task into smaller tasks and commit smaller changes.
    With staging area it is easier to focus in small tasks.

  - It also gives you the offer to take break and forgetting about how much work you have done before taking break.

    Suppose you need to change three files to make one logical change and you have changed the first file and need a long break until you start making the other changes.
    At this moment you cannot commit and you want to track which files you are done with so that after comming back you do not need to try to remember how much work have been done.
    So add the file to the staging area and it will save your work.
    When you come back just do `git diff --staged` and check which files you changed and where and start making other changes.

  - When you commit it's only going to commit the changes in the index (the "staged" files).
    There are many uses for this, but the most obvious is to break up your working changes into smaller, self-contained pieces.
    Perhaps you fixed a bug while you were implementing a feature.

    You can `git add` just that file (or `git add -p` to add just part of a file!) and then commit that bugfix before committing everything else.

    If you are using `git commit -a` then you are just forcing an `add` of everything right before the commit.
    Don't use `-a` if you want to take advantage of staging files.

  - You can also treat the staged files as an intermediate working copy with the `--cached` to many commands.
    For example, `git diff --cached` will show you how the stage differs from `HEAD` so you can see what you're about to commit without mixing in your other working changes.


## todo list

    $ git commit --allow-empty -m "TODO: $*"
    $ git log --oneline master..
    ### if branch from <br_5-8_global_vdom_profile>
    $ git log br_5-8_global_vdom_profile..

      9ca4a06 TODO: Check if feature X works under edge-case
      ca343b0 implemented awesometastic feature X

# Tig: command-line-ui based front-end for git

    [Getit from here][4]
    The author manual site: http://jonas.nitro.dk/tig/manual.html
    $ sudo apt-get install tig

It is the mutt to your Outlook, the Vim to your Emacs, the w3m to your Firefox.

## commands

    $ tig               <<< It’s basically a git log, with a bit of ASCII-art to represent the history (you can hide the graph with `g`)
      - option: the name of a branch
      - Without any argument, it displays the current branch.
      - "--all" for all branches, show the branch relation with pretty graphic.
      - a range of commits as git log would expect (e.g. tig master..branch).

    $ tig grep "patch-string"

## Routine
    Open with the list of commits in the history view.

    <Enter> key         <<< opens that commit in a split diff view.
      At the beginning of the diff is the list of files that the commit touched.
      If you select one of them and press <Enter>, you will directly jump to the beginning of that file in the diff.
    <t> key             <<< open the tree view, with the files at the commit point even don't need checkout the old version.
    <q> key             <<< Press q to close the child views (and press q a second time to quit tig).
    arrow keys or <j/k> <<< navigate through the commits, navigate in the diff view
    the </> key         <<< search (match is done on summary or author).

### [Killer feature] Status view: interactive git status

    $ tig status <or> shift-s in the main view

    ### list three kinds of files:
    - the files that you've modified and staged
    - the files you've modified but haven't staged yet,
    - and the files that are no yet tracked by git.

    <shift-c>           <<< open editor to enter the commit message (make sure you close any open diff view first).
    <u> key             <<< Toggle stage/unstage the selected file
    <!> key             <<< Revert all uncommitted changes to the selected file. No need to remember that pesky git reset HEAD <file> command.
    <Enter> key         <<< View the diff that file, Move like `j/k` keys (line by line), or the `@` key (chunk by chunk)
        press <u>       <<< it will only stage the current diff chunk

### Blame view

    $ tig blame <file>

### View old version of repos:
    <t> key on a commit in the history view     <<< open the tree view. In this view, you browse the content of your repository in exactly the state it was at that point in time (just use the arrow keys and Enter), without having to do a git checkout.

## Shortcuts

1. View Switching
    m   Switch to main view.
    d   Switch to diff view.
    l   Switch to log view.
    p   Switch to pager view.
    t   Switch to (directory) tree view.
    f   Switch to (file) blob view.
    g   Switch to grep view.
    b   Switch to blame view.
    r   Switch to refs view.
    y   Switch to stash view.
    h   Switch to help view
    s   Switch to status view
    c   Switch to stage view

2. View Manipulation
    q       Close view, if multiple views are open it will jump back to the previous view in the view stack. If it is the last open view it will quit. Use Q to quit all views at once.
    Enter   This key is "context sensitive" depending on what view you are currently in. When in log view on a commit line or in the main view, split the view and show the commit diff. In the diff view pressing Enter will simply scroll the view one line down.
    Tab     Switch to next view.
    R       Reload and refresh the current view.
    O       Maximize the current view to fill the whole display.
    Up      This key is "context sensitive" and will move the cursor one line up. However, if you opened a diff view from the main view (split- or full-screen) it will change the cursor to point to the previous commit in the main view and update the diff view to display it.
    Down    Similar to Up but will move down.
    ,       Move to parent. In the tree view, this means switch to the parent directory. In the blame view it will load blame for the parent commit. For merges the parent is queried.

3. View Specific Actions
    u   Update status of file. In the status view, this allows you to add an untracked file or stage changes to a file for next commit (similar to running git-add <filename>). In the stage view, when pressing this on a diff chunk line stages only that chunk for next commit, when not on a diff chunk line all changes in the displayed diff are staged.
    M   Resolve unmerged file by launching git-mergetool(1). Note, to work correctly this might require some initial configuration of your preferred merge tool. See the manpage of git-mergetool(1).
    !   Checkout file with unstaged changes. This will reset the file to contain the content it had at last commit.
    1   Stage single diff line.
    @   Move to next chunk in the stage view.
    ]   Increase the diff context.
    [   Decrease the diff context.

# Svn

## svn status -q

    U: Working file was updated
    G: Changes on the repo were automatically merged into the working copy
    M: Working copy is modified
    C: This file conflicts with the version in the repo
    ?: This file is not under version control
    !: This file is under version control but is missing or incomplete
    A: This file will be added to version control (after commit)
    A+: This file will be moved (after commit)
    D: This file will be deleted (after commit)
    S: This signifies that the file or directory has been switched from the path of the rest of the working copy (using svn switch) to a branch
    I: Ignored
    X: External definition
    ~: Type changed
    R: Item has been replaced in your working copy. This means the file was scheduled for deletion, and then a new file with the same name was scheduled for addition in its place.


## svn list

    $ svn help [item]
    $ svn ls url
    $ svn list --verbose https://www.thegeekstuff.com/project/branches/release/migration/data/bin
       16 sasikala        28361         Apr 16 21:11 README.txt
      21 sasikala         0         Apr 18 12:22 INSTALL
      22 sasikala                Apr 18 10:17 src/
    $ svn co -r1019 https://www.thegeekstuff.com/project/branches/release/migration/data/cfg /home/sasikala/cfg/


    $ svn info       <<< show configuration-url and current version
    $ svn up[date]        <<< Updates working copy from repository.
    $ svn st[atus] | grep  -v ‘^?’
    $ svn add [path]     <<< Adds new files/directories to SVN.
    $ svn revert [file or path]
    $ svn resolve --accept working <FILENAME>
    $ svn c[omm]i[t] -m “msg”   <<< Checks in changes.


    $ svn log -l 10 [file]
    $ svn log -r 1:HEAD
    $ svn log -r HEAD:1
    $ svn log -r {2011-02-02}:{2011-02-03}
    $ svn log -v --l 4
      r58687 | mr_x | 2012-04-02 15:31:31 +0200 (Mon, 02 Apr 2012) | 1 line Changed
      paths:
      A /trunk/java/App/src/database/support
      A /trunk/java/App/src/database/support/MIGRATE
      A /trunk/java/App/src/database/support/MIGRATE/remove_device.sql


    $ svn di[ff] Shows how working copy differs from last update (line-by-line).
    $ svn diff -x -p    <<< like git diff to show the c outer function name
    $ svn diff -r 578 [file]
    $ svn diff -r 578:592 [file] [--summarize]
    $ svn diff -c --number--   <<< view diff of the commit



  [1]: http://mislav.uniqpath.com/2010/07/git-tips/
  [2]: http://git.or.cz/course/svn.html
  [3]: http://trac.parrot.org/parrot/wiki/git-svn-tutorial
  [4]: http://www.if-not-true-then-false.com/2012/svn-subversion-backup-and-restore/

