
# Howto

## cherry-pick

### cherry-pick with commit

    git rebase --onto a b f

### cherry-pick without commit

Using cherry-pick to show committed eco as a gitgutter:

    git cherry-pick -n <commit> # get your patch, but don't commit (-n = --no-commit)
    [OR]
    git cherry-pick A^..B       # multiple commit

    git reset                   # unstage the changes from the cherry-picked commit
        `git rm --cached` unstages the file but doesn't remove it from the working directory.
        git reset -- <filePath> will unstage any staged changes for the given file(s)

        [git-version > 2.24]
        git restore --staged instead of `git reset`
          but "fatal: you must specify path(s) to restore"

    git add -p                  # -p(patch): make all your choices (add the changes you do want)
    git commit                  # make the commit!

If you really want a git cherry-pick -p <commit> (that option does not exist), your can use

    git checkout -p <commit>

