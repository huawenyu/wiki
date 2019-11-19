# Quick Start:

  - [Gdbserver][1],
    + $ sudo apt-get install gdbserver
  - GUI front-end: [neovim][5], eclipse, others(insight, nemiver)

## howto generate core file

    $ ulimit -a                 <=== show current system limit
    $ ulimit -c unlimited

    $ gdb --args pcregrep -f ../regex.txt ../test.txt

    # coredump a hunging process
    gcore <pid>
    <OR>
    kill -ABRT <pid>


# Register

    https://en.wikipedia.org/wiki/Control_register

    CR2 - Contains a value called Page Fault Linear Address (PFLA).
    When a page fault occurs, the address the program attempted to access is stored in the CR2 register.


## cpu: ARM

  [Arm ASM Doc][6], and also we can search a command 'cbnz' by google like:

    cbnz site:infocenter.arm.com

```sh
    $ sudo apt-get install gdb-multiarch
    $ gdb-multiarch sysinit/init
    gdb> 
```

## disassemble from address

when crash, we can address (such as 0x090b5c6b) and registers list, then:

```gdb
    list *0x090b5c6b		view the related source code if the exe is debug version, or we have init.map file
    disas /m function		print mixed source+disassembly by specifying the /m modifier, and the function come from list
    disas 0x090b5c6b,+10	list disassemble from begin-addr to end-addr
    disas 0x090b5c6b		list current function’s disassemble
    x/5i 0x090b5c6b		list disassemble, like disas start,start+5
```

## ASM of current $pc

```gdb
    (gdb) display/4i $pc
    (gdb) x/10x $sp       	check the stack in HEX
    (gdb) x/10xb &buff[0]       check buffer in HEX onebye by one
    (gdb) ni
    (gdb) si
    (gdb) undisplay <ID>
    (gdb) <OR>   disable display <ID>
```

