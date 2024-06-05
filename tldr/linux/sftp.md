# sftp client

Assue we already have a sftp-server, and we want access it by no-pass which means we should upload our pub-key to our directory.

    ### [Local-linux]: Generate keypair
    $ ssh-keygen -t ecdsa
      <default>
      Enter passphrase (empty for no passphrase):   <=== if we don't want to input passphrase, keep empty here
    $ cd ~/.ssh

    ### [sftp-server: hyu@172.16.101.145]: upload our pub-key to our dir
    $ sftp hyu@172.16.101.145
        hyu@172.16.101.145's password:  <=== Our real password, just this time.
        Connected to 172.16.101.145.
        sftp> cd hyu
        sftp> mkdir .ssh
        sftp> cd .ssh/
        sftp> put id_ecdsa.pub authorized_keys
            Uploading id_ecdsa.pub to /jxiong/.ssh/authorized_keys
            id_ecdsa.pub 100% 177 185.8KB/s 00:00
        sftp> dir
            authorized_keys
        sftp> exit

    ### [Local-linux]: test the keypair works
    $ sftp -i ~/.ssh/id_ecdsa hyu@172.16.101.145
        Connected to 172.16.101.145.
        sftp> cd hyu
        sftp> dir
        sftp> exit

    ### [Local-linux]: alias local
    $ alias newfileserver="sftp -i ~/.ssh/id_ecdsa hyu@172.16.101.145"
    $ newfileserver
        Connected to 172.16.101.145.
        sftp>
    $ alias lsfile="echo "'ls jxiong"' | newfileserver"
    $ lsfile
        Connected to 172.16.101.145.
        === Generate ssk key pair ===sftp> ls hyu


## Use script for sftp GET and PUT

### getfile

``` echo getfile
#/usr/bin/bash
# $1 sftp server, the format can be "username@sftp server", or only uses server ip without username, the user name will use your current user if
# $2 remote file, which is in sftp server

echo "get $2" | sftp $1
```

### putfile
``` echo putfile
#/usr/bin/bash
# $1 local file, which will be put to sftp server
# $2 sftp server, the format can be "username@sftp server", or only uses server ip without username, the user name will use your current user if
# $3 remote file, which is in sftp server

echo "put $1 $3" | sftp $2
```
### commands
    $ chmod +x getfile
    $ chmod +x putfile

    $ cp getfile putfile /usr/local/bin

    $ getfile hyu@172.16.101.145 /hyu/test/aaa.txt.gz

    $ putfile /tmp/aaa.txt.gz hyu@172.16.101.145 /hyu/test

## Use sftp over socks 

### through `paramiko`

    https://www.paramiko.org/installing.html

### trhough `nc`

https://stackoverflow.com/questions/69627222/sftp-using-socks-proxy-command-with-password-authentication

This can be done using a local SSH config file.  Create a new file inside the .ssh directory within your home directory, and call the file "config".  Here is the full content of my ~/.ssh/config file

    host server.mywork.com
        ProxyCommand /usr/bin/nc -x localhost:8080 %h %p

## Use lftp as sftp-clint

### script
``` sh
lftp -f "
open -p port -u user,any_string_will_do sftp://server
mirror --no-empty-dirs  --only-newer --verbose $FTP_FOLDER $LOCAL_FOLDER
bye
```

### command

    ### lftp sftp://user@example.com        <=== will prompt the password-input
    ### There is a little trick to make lftp use your private key for authentication. The key is to pass an empty password to lftp as follows:
    $ lftp -u user, sftp://example.com    <=== connected directly
