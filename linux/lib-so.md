# sample - hello world

http://www.yolinux.com/TUTORIALS/LibraryArchives-StaticAndDynamic.html
[Shared libraries with GCC on Linux](https://www.cprogramming.com/tutorial/shared-libraries-linux-gcc.html)

## 1. source code:

file1: foo.h:

```c
    #ifndef foo_h__
    #define foo_h__

    extern void foo(void);

    #endif  // foo_h__
```

file2: foo.c:
```c
    #include <stdio.h>

    void foo(void)
    {
        puts("Hello, I am a shared library");
    }
```

file3: main.c:

```c
    #include <stdio.h>
    #include "foo.h"

    int main(void)
    {
        puts("This is a shared library test...");
        foo();
        return 0;
    }
```

## 2. build & run

```sh
    ### Step 1: Compiling with Position Independent Code
    $ gcc -c -Wall -Werror -fpic foo.c

    ### Step 2: Creating a shared library from an object file
    $ gcc -shared -o libfoo.so foo.o

    ### Step 3: Linking with a shared library
    $ gcc -Wall -o test main.c -lfoo
        /usr/bin/ld: cannot find -lfoo
        collect2: ld returned 1 exit status

    $ gcc -L/home/username/foo -Wall -o test main.c -lfoo

    ### Step 4: Making the library available at runtime
    $ ./test
    ./test: error while loading shared libraries: libfoo.so: cannot open shared object file: No such file or directory
    Oh no! The loader cannot find the shared library.3 We did not install it in a standard location, so we need to give the loader a little help. We have a couple of options: we can use the environment variable LD_LIBRARY_PATH for this, or rpath. Let us take a look first at LD_LIBRARY_PATH:

### run method-1: Offer library by Using LD_LIBRARY_PATH
    $ echo $LD_LIBRARY_PATH
    $ LD_LIBRARY_PATH=/home/username/foo:$LD_LIBRARY_PATH
    $ ./test
        ./test: error while loading shared libraries: libfoo.so: cannot open shared object file: No such file or directory
    $ export LD_LIBRARY_PATH=/home/username/foo:$LD_LIBRARY_PATH
    $ ./test
        This is a shared library test...
        Hello, I am a shared library

### run method-2: Offer library Using rpath
    #### Now let s try rpath (first we will clear LD_LIBRARY_PATH to ensure it is rpath that is finding our library). Rpath, or the run path, is a way of embedding the location of shared libraries in the executable itself, instead of relying on default locations or environment variables. We do this during the linking stage. Notice the lengthy â€œ-Wl,-rpath=/home/username/fooâ€ option. The -Wl portion sends comma-separated options to the linker, so we tell it to send the -rpath option to the linker with our working directory.
    $ unset LD_LIBRARY_PATH
    $ gcc -L/home/username/foo -Wl,-rpath=/home/username/foo -Wall -o test main.c -lfoo
    $ ./test
    This is a shared library test...
    Hello, I am a shared library

### rpath vs. LD_LIBRARY_PATH
        There are a few downsides to rpath, however. First, it requires that shared libraries be installed in a fixed location so that all users of your program will have access to those libraries in those locations. That means less flexibility in system configuration. Second, if that library refers to a NFS mount or other network drive, you may experience undesirable delays - or worse - on program startup.

### run method-3: Using ldconfig to modify ld.so
    $ cp /home/username/foo/libfoo.so /usr/lib
    $ chmod 0755 /usr/lib/libfoo.so
    $ ldconfig -p | grep foo
    libfoo.so (libc6) => /usr/lib/libfoo.so
    $ unset LD_LIBRARY_PATH
    $ gcc -Wall -o test main.c -lfoo
    $ ldd test | grep foo
    libfoo.so => /usr/lib/libfoo.so (0x00a42000)
    $ ./test
    This is a shared library test...
    Hello, I am a shared library

```

### run ld.so loading order

That about wraps it up. We have covered how to build a shared library, how to link with it, and how to resolve the most common loader issues with shared libraries - as well as the positives and negatives of different approaches.

1. It looks in the DT_RPATH section of the executable, unless there is a DT_RUNPATH section.
2. It looks in LD_LIBRARY_PATH. This is skipped if the executable is setuid/setgid for security reasons.
3. It looks in the DT_RUNPATH section of the executable unless the setuid/setgid bits are set (for security reasons).
4. It looks in the cache file /etc/ld/so/cache (disabled with the -z nodeflib linker option).
5. It looks in the default directories /lib then /usr/lib (disabled with the -z nodeflib linker option).

### what's fPIC

What is position independent code? PIC is code that works no matter where in memory it is placed. Because several different programs can all use one instance of your shared library, the library cannot store things at fixed addresses, since the location of that library in memory will vary from program to program. ↩

GCC first searches for libraries in /usr/local/lib, then in /usr/lib. Following that, it searches for libraries in the directories specified by the -L parameter, in the order specified on the command line. ↩

The default GNU loader, ld.so, looks for libraries in the following order

# cmd: ldconfig
```sh
    $ sudo ldconfig -v
```
    ldconfig  -- creates the necessary links and cache to the most recent shared libraries found in the directories specified on the command line

    By default, ldconfig looks in:
      - `/lib`, `/usr/lib`,
      - and directories listed in `/etc/ld.so.conf`
      - and directories listed in `$LD_LIBRARY_PATH`.

           $ LD_LIBRARY_PATH=/opt/intel/mkl/lib/ia32:$LD_LIBRARY_PATH  LD_PRELOAD=/opt/intel/mkl/lib/ia32/libmkl_core.so ./myexe

        Add to `~/.bashrc` file so it will run every time you log in:

            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/library

      - $LD_PRELOAD -- override symbols in the stock libraries by creating a library with the same symbols
            1. If you set LD_PRELOAD to the path of a shared object, that file will be loaded before any other library (including the C runtime, libc.so).
                $ LD_PRELOAD=/path/to/my/malloc.so /bin/ls
            2. One important thing to keep in mind: you usually want to specify an absolute path to LD_PRELOAD.
                The reason is that it being an environment variable,
                it's inherited by child processes - which may have a different working directory than the parent process.
                So any relative path would fail to locate the library to preload.

## list function

```sh
    $ nm -D /usr/lib/libopenal.so.1
    <or>
    $ objdump -T *.so
```

## a nonstandard directory

For example, if the libraries have been installed in: `/usr/local/lib`
If your library is somewhere else, you can do at least one of the following:
- either sudo add the directory on its own line to `/etc/ld.so.conf`,
- or append the library's path to `$LD_LIBRARY_PATH` environment variable during execution,
- or LIBDIR to the `LD_RUN_PATH' environment variable during linking
- or the `-Wl,--rpath -Wl,LIBDIR' linker flag
- or move the library into `/usr/lib`.
    $ sudo ln -sf /lib/$(arch)-linux-gnu/libudev.so.1 /lib/$(arch)-linux-gnu/libudev.so.0
- Then run `ldconfig` to reload into system cache.

    $ sudo ldconfig -n /usr/local/lib
    $ sudo ldconfig

## fix load shared libraries error: cannot open shared object file

    Which means the library is not in the standard path, so we should use LD_LIBRARY_PATH to told ldconfig where to find it.

    ### Find where the library is placed if you don't know it.
        $ locate that_library.so

        $ cd /
        $ sudo find ./ | grep that_library.so

    ### Check for the existence of the dynamic library path environnement variable(LD_LIBRARY_PATH)

        $ echo $LD_LIBRARY_PATH

    ### if there is nothing to be display we need to add the default path value (or not as you wish)
        $ export LD_LIBRARY_PATH=/usr/local/lib
        <or> temperary change:
        $ LD_LIBRARY_PATH=/usr/local/lib ./myexe

    ### We add the desire path and export it and try the application

        $ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/my_library/path.so.something
        $ ./my_app
        <or> temperary change:
        $ LD_LIBRARY_PATH=/opt/intel/mkl/lib/ia32:$LD_LIBRARY_PATH  LD_PRELOAD=/opt/intel/mkl/lib/ia32/libmkl_core.so ./myexe

    ### work with sudo:

        $ sudo LD_LIBRARY_PATH=/usr/local/lib ./myexe

## Install Dev package or wrong version

If that doesn't work, I would also check out [Paul's suggestion][2] and look for a "-dev" version of the library.
Many libraries are split into dev and non-dev packages. You can use this command to look for it:

    $ apt-cache search <libraryname>


  [1]: http://linux.die.net/man/8/ldconfig
  [2]: https://stackoverflow.com/a/480786/22781
  [3]: http://www.gnu.org/software/gsl/manual/html_node/Shared-Libraries.html
