# Tutorial

## purpose of .PHONY

By default, Makefile targets are "file targets" - they are used to build files from other files.
Make assumes its target is a file, and this makes writing Makefiles relatively easy:

    foo: bar
      create_one_from_the_other foo bar

However, sometimes you want your Makefile to run commands that do not represent physical files in the file system.
Good examples for this are the common targets "clean" and "all".
Chances are this isn't the case, but you *may* potentially have a file named `clean` in your main directory.
In such a case Make will be confused because by default the `clean` target would be associated with
this file and Make will only run it when the file doesn't appear to be up-to-date with regards to its dependencies.

These special targets are called *phony* and you can explicitly tell Make they're not associated with files, e.g.:

    .PHONY: clean
    clean:
      rm -rf *.o

Now `make clean` will run as expected even if you do have a file named `clean`.

In terms of Make, a phony target is simply a target that is always out-of-date,
so whenever you ask `make <phony_target>`, it will run, independent from the state of the file system.
Some common `make` targets that are often phony are: `all`, `install`, `clean`, `distclean`, `TAGS`, `info`, `check`.

## A target call another target

By calling `make fresh` you get first the clean target, then the `clearscreen` which runs clear and finally `all` which does the job.

```make
.PHONY : clearscr fresh clean all

all :
	compile executable

clean :
	rm -f *.o $(EXEC)

fresh : | clean clearscr all        <=== `make` will keep the orders same as them here, `|` enforce the orders even in parallel builds

clearscr:
	clear
```

### What happens in the case of parallel builds with make’s -j option?

In that case, you want to define order-only prerequisites.
Order-only prerequisites can be specified by placing a pipe symbol `|` in the prerequisites list:
- `targets : normal-prerequisites | order-only-prerequisites`
- any prerequisites to the left of the pipe symbol are normal;
- any prerequisites to the right are order-only

# Sample implement libs

## Implement: boilermake

https://github.com/dmoulding/boilermake.git

### the layout of sample

```sh
$ boilermake git:(master) git clone https://github.com/dmoulding/bebs_demo.git

$ boilermake git:(master) tree
.
├── COPYING
├── Makefile
├── MANUAL
├── README
└── test-app
    ├── animals
    │   ├── animal.cc
    │   ├── animal.hh
    │   ├── animals.mk
    │   ├── cat
    │   │   ├── cat.cc
    │   │   └── cat.hh
    │   ├── dog
    │   │   ├── chihuahua
    │   │   │   ├── chihuahua.cc
    │   │   │   ├── chihuahua.hh
    │   │   │   └── chihuahua.mk
    │   │   ├── dog.cc
    │   │   └── dog.hh
    │   ├── main.mk
    │   ├── Makefile -> ../Makefile
    │   └── mouse
    │       ├── mouse.cc
    │       └── mouse.hh
    ├── build
    │   ├── animals
    │   │   └── libanimals.a
    │   │       ├── animal.o
    │   │       ├── animal.P
    │   │       ├── cat
    │   │       │   ├── cat.o
    │   │       │   └── cat.P
    │   │       ├── dog
    │   │       │   ├── chihuahua
    │   │       │   │   ├── chihuahua.o
    │   │       │   │   └── chihuahua.P
    │   │       │   ├── dog.o
    │   │       │   └── dog.P
    │   │       └── mouse
    │   │           ├── mouse.o
    │   │           └── mouse.P
    │   ├── libanimals.a
    │   │   └── animals
    │   │       ├── animal.o
    │   │       ├── animal.P
    │   │       ├── cat
    │   │       │   ├── cat.o
    │   │       │   └── cat.P
    │   │       ├── dog
    │   │       │   ├── chihuahua
    │   │       │   │   ├── chihuahua.o
    │   │       │   │   └── chihuahua.P
    │   │       │   ├── dog.o
    │   │       │   └── dog.P
    │   │       └── mouse
    │   │           ├── mouse.o
    │   │           └── mouse.P
    │   └── talk
    │       ├── talk.o
    │       └── talk.P
    ├── libanimals.a
    ├── main.mk
    ├── Makefile -> ../Makefile
    ├── talk
    ├── talk.cc
    └── talk.mk

20 directories, 46 files
```
