# Multiple public keys for one user

You can have as many keys as you desire.  It's good practice to use separate private/public key sets for different realms anyway, like one set for your personal use, one for your work, etc.

First, generate two separate keypairs, one for home and one for work:

    ssh-keygen -t rsa -f ~/.ssh/id_rsa.home
    ssh-keygen -t rsa -f ~/.ssh/id_rsa.work

Next, add an entry to your `~/.ssh/config` file to pick the key to use based on the server you connect to:

    Host home
    Hostname home.example.com
    IdentityFile ~/.ssh/id_rsa.home
    User <your-home-acct>

    Host work
    Hostname work.example.com
    IdentityFile ~/.ssh/id_rsa.work
    User <your-work-acct>

Next, append the contents of your `id_rsa.work.pub` into `~/.ssh/authorized_keys` on the work machine, and do the same for the home key on your home machine.

Then when you connect to the home server you use one of the keys, and the work server you use another.

Note you probably want to add both keys to your `ssh-agent` so you don't have to type your passphrase all the time.

## github

https://gist.github.com/jexchan/2351996

$ git config user.name "jexchan"
$ git config user.email "jexchan@gmail.com"

$ git config user.name "activehacker"
$ git config user.email "jexlab@gmail.com"

# Howtos

## Delete commits history with git commands
https://gist.github.com/heiswayi/350e2afda8cece810c0f6116dadbe651

### First Method

Deleting the .git folder may cause problems in our git repository. If we want to delete all of
our commits history, but keep the code in its current state, try this:

# Check out to a temporary branch:
git checkout --orphan TEMP_BRANCH

# Add all the files:
git add -A

# Commit the changes:
git commit -am "Initial commit"

# Delete the old branch:
git branch -D master

# Rename the temporary branch to master:
git branch -m master

# Finally, force update to our repository:
git push -f origin master

This will not keep our old commits history around. But if this doesn't work, try the next method below.

### Second Method

# Clone the project, e.g. `myproject` is my project repository:
git clone https://github/heiswayi/myproject.git

# Since all of the commits history are in the `.git` folder, we have to remove it:
cd myproject

# And delete the `.git` folder:
git rm -rf .git

# Now, re-initialize the repository:
git init
git remote add origin https://github.com/heiswayi/myproject.git
git remote -v

# Add all the files and commit the changes:
git add --all
git commit -am "Initial commit"

# Force push update to the master branch of our project repository:
git push -f origin master
NOTE: You might need to provide the credentials for your GitHub account.

