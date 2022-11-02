GCC compile process
===================
https://www3.ntu.edu.sg/home/ehchua/programming/cpp/gcc_make.html

The compilation process has 4 steps:    $ gcc -v -o hello.exe hello.c
- preprocessing                         $ cpp hello.c > hello.i
- compiling (gcc/g++)                   $ gcc -S hello.i    ### output `hello.s`
- assembling (as)                       $ as -o hello.o hello.s
- linking (ld)                          $ ld -o hello.exe hello.o ...libraries...

The preprocessor
----------------
[Related Option](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html):
- Directory Options
- Warning Options

Command:

    $ cpp
    $ gcc -E    preprocess only

Detail:
- removing comments
- expanding macros
- expanding included files

The compiler
------------
This step takes the output of the preprocessor and generates assembly language, an intermediate
human readable language, specific to the target processor.

[Related Option](https://caiorss.github.io/C-Cpp-Notes/compiler-flags-options.html#org3aa59c3)

Command:

    $ gcc -S    compiles only

Detail:
- gcc for C,
- g++ for c++/cpp/cxx

The assembler
-------------
Transforms the assembly code into object code, that is code in machine language.

Command:

    $ as
    $ gcc -c    compiles and assembles

The linker
----------
Connects any libraries, and other Obj files of the same project into one executable file.
[Related Option](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html)

Command:

    $ ld

Detail:
- If we are using a function from libraries, linker will link our code with that library function code.
- In static linking, the linker makes a copy of all used library functions to the executable file.
- In dynamic linking, the code is not copied, it is done by just placing the name of the library in the binary file.

Telling gcc directly to link a library statically
-------------------------------------

Use `-l:` instead of `-l`. For example `-l:libXYZ.a` to link with `libXYZ.a`. Notice the `lib` and `.a` are written out, as opposed to `-lXYZ` which would auto-expand to `libXYZ.so`/`libXYZ.a`.

It is an [option of the GNU `ld` linker](https://sourceware.org/binutils/docs/ld/Options.html):

> `-l namespec` ... If *namespec* is of the form `:filename`, `ld` will search the library path for a file called *filename*, otherwise it will search the library path for a file called `libnamespec.a`. ... on ELF ... systems, `ld` will search a directory for a library called `libnamespec.so` before searching for one called `libnamespec.a`. ... Note that this behavior does not apply to `:filename`, which always specifies a file called *filename*."

(Since [binutils 2.18](https://sourceware.org/binutils/docs-2.18/ld/Options.html))

Note that this only works with the GNU linker. If your `ld` isn't the GNU one you're out of luck.



Some known variables
--------------------
- CPPFLAGS - is the variable name for flags to the C preprocessor.
- CXXFLAGS - is the standard variable name for flags to the C++ compiler.
- CFLAGS is - the standard name for a variable with compilation flags.
- LDFLAGS - should be used for search flags/paths (-L) - i.e. -L/usr/lib (/usr/lib are library binaries).
- LDLIBS - for linking libraries.
