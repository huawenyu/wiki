# git:

# cherry-pick

## cherry-pick with commit

    git rebase --onto a b f

## cherry-pick without commit

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

# Add changes to cache

	git add -A		## stages all changes
	git add .		## stages new files and modifications, without deletions (on the current directory and its subdirectories).
	git add -u		## stages modifications and deletions, without new files

# Git diff

	git diff			## Shows the changes between the working directory and the index. This shows what has been changed, but is not staged for a commit.
	git diff --cached	## Shows the changes between the index and the HEAD (which is the last commit on this branch). This shows what has been added to the index and staged for a commit.
	git diff HEAD		## Shows all the changes between the working directory and HEAD (which includes changes in the index). This shows all the changes since the last commit, whether or not they have been staged for commit or not.
