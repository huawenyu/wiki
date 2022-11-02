# doc

https://www.cyberciti.biz/tips/understanding-linux-unix-umask-value-usage.html

`umask` is used to remove the right from user-group-others when user create a new file/directory.

## Explain Octal umask Mode 022 And 002

As I said earlier, if the default settings are not changed:
- directories with 777.
- and files are created with the access mode 666

In this example:
The default umask 002 used for `normal user`. With this mask:
- default directory permissions are 775
- and default file permissions are 664.

The default umask for the `root user` is 022 result into:
- default directory permissions are 755
- and default file permissions are 644.

For directories, the base permissions are (rwxrwxrwx) 0777 and for files they are 0666 (rw-rw-rw).

## In short

A umask of `022` allows `only you to write data, but anyone can read data`.
A umask of `077` is good for a `completely private` system. No other user can read or write your
data if umask is set to 077.

A umask of 002 is good when you share data with other users in the same group. Members of your
group can create and modify data files; those outside your group can read data file, but cannot
modify it. Set your umask to 007 to completely exclude users who are not group members.

