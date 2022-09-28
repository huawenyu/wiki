int dup2(int oldfd, int newfd)
==========
Redirect the io-newfd to oldfd.
`dup2(f1, 0)` -- redirect the std-input `0` from the opened file `f1`.

https://stackoverflow.com/questions/24538470/what-does-dup2-do-in-c

`dup2` doesn't switch the file descriptors, it makes them equivalent. After `dup2(f1, 0)`,
whatever file was opened on descriptor `f1` is now also opened (with the same mode and position)
on descriptor 0, i.e. on standard input.

If the target file descriptor (here, 0) was open, it is closed by the `dup2` call. Thus:

    before                         after
    -------------------------------------------------------
    0: closed, f1: somefile        0: somefile, f1:somefile
    0: otherfile, f1: somefile     0: somefile, f1:somefile

No locking is involved.

`dup2` is useful (among other things) when you have part of a program that reads or write from
the standard file descriptors. For example, suppose that `somefunc()` reads from standard input,
but you want it to read from a different file from where the rest of the program is getting
its standard input. Then you can do (error checking omitted):

```c
    int save_stdin = dup(0);
    int somefunc_input_fd = open("input-for-somefunc.data", O_RDONLY);
    dup2(somefunc_input_fd, 0);
    /* Now the original stdin is open on save_stdin, and input-for-somefunc.data on both somefunc_input_fd and 0. */
    somefunc();
    close(somefunc_input_fd);
    dup2(save_stdin, 0);
    close(save_stdin);
```


Redirect child-process in/out to files
---------------------------------------

https://stackoverflow.com/questions/14543443/in-c-how-do-you-redirect-stdin-stdout-stderr-to-files-when-making-an-execvp-or
```c
    pid_t pid = fork();
    if (pid == -1) {
        // ...
    } else if (pid == 0) { // child
        /** can't work
        stdin = someopenfile;
        stdout = someotherfile;
        stderr = somethirdopenfile;
        execvp(args[0], args);
        // handle error ...
        */

        dup2(fileno(someopenfile), STDIN_FILENO);
        dup2(fileno(someotherfile), STDOUT_FILENO);
        dup2(fileno(somethirdopenfile), STDERR_FILENO);
        fclose(someopenfile);
        fclose(someotheropenfile);
        fclose(somethirdopenfile);
        execvp(args[0], args);
        // handle error ...
    } else { // parent
        // ...
    }
```

