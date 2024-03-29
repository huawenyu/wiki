# Quick Start:

  - https://en.wikipedia.org/wiki/Call_stack
  - Disassemble the `static int a = 0;`
    + https://www.recurse.com/blog/7-understanding-c-by-learning-assembly
  -
  - Gdbserver
    + https://sourceware.org/gdb/onlinedocs/gdb/gdbserver-man.html
    + $ sudo apt-get install gdbserver
  - GUI front-end: [neovim][5], eclipse, others(insight, nemiver)

## Enhanced gdb

- Using alias to using different gdbinit

    $ cat ~/.gdbinit_gef
    source /home/hyu/dotfiles/.gdbinit-gef.py

    alias gdx1='pwndbg -x ~/.gdbinit_pwndbg'
    alias gdx2='gdb -x ~/.gdbinit_gef'

- pwndbg
  1. Install

    download [pwndbg_2023.07.17_amd64.deb](https://github.com/pwndbg/pwndbg/releases/tag/2023.07.17-pkgs)
    sudo dpkg -i pwndbg_2023.07.17_amd64.deb
  2. Install tmux-base GUI: [splitmind](https://github.com/jerdna-regeiz/splitmind)
- [gef](https://github.com/hugsy/gef)

## howto generate core file

    $ ulimit -a                 <=== show current system limit
    $ ulimit -c unlimited

    $ gdb --args pcregrep -f ../regex.txt ../test.txt

    # coredump a hunging process
    gcore <pid>
    <OR>
    kill -ABRT <pid>


# Useful command:

[command doc][2][3]

## Registers
  * Integer arguments (including pointers) are placed in the registers `%rdi, %rsi, %rdx, %rcx, %r8, and %r9`, in that order.

```
|__64__|__56__|__48__|__40__|__32__|__24__|__16__|__8___|
|__________________________RAX__________________________|
|xxxxxxxxxxxxxxxxxxxxxxxxxxx|____________EAX____________|
|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|_____AX______|
|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|__AH__|__AL__|
```

## most useful

``` gdb
    handle SIGUSR1 noprint nostop
    handle SIGUSR2 noprint nostop

    watch *(int *) 0x600850	# break if the address's value changed

    p (int)&((struct A*)0)->a	# struct member’s offset
    p/c (unsigned char[4])addr.addr	# int2ipaddr
    dump binary memory /tmp/log.bin buf (buf + len)
    p *array@len		# int *array = malloc (5 * sizeof(int))
    p/s str
    x/s str
    p *str@length

    set disassembly-flavor intel
    set disassemble-next-line on    # show asm of nexti

    finish			    # show current function's return value
    type/whatis			# check value's type
    set $sp += 4        # change register/return value
```

## normal useful

```gdb
    set args
    info args			# View all function arguments
    set print pretty on		# Prints out prettily formatted C source code
    set logging on		# Log debugging session to show to others for support
    set print array on		# Pretty array printing

    # disable the "Type <return> to continue, or q <return> to quit" pagination prompt in GDB
    set height 0
    set pagination off

    backtrace full		# Complete backtrace with local variables
    up, down, frame <#>		# Move through frames
    until <line#>		# run to somewhere
    where			# Line number currently being executed
    list			# view source
    info locals			# View all local variables

    # finding out quickly what all threads are doing.
    thread apply all bt
    thread apply all print $pc

    # define hook/function
    # define user commands, <hook-stop> auto-exec when stop, <setup> auto-exec when gdb start
    define hook-stop
        printf “%d” i
        refresh
        echo hello\n
    end
```

## set source path

  [Ref][https://sourceware.org/gdb/onlinedocs/gdb/Source-Path.html]

If gdb debug sometimes cannot find source because the source path is different. So how to tell gdb where the source code path:
```gdb
    show directories                            # Print the source path: show which directories it contains.
    dir dirname                                 # Add directory dirname to the front of the source path.

    show substitute-path [path]
    set substitute-path from to                 # have different src path `to`
    set substitute-path /usr/src/include /mnt/include
    unset substitute-path [path]
```
## ARM

  [Arm ASM Doc][6], and also we can search a command 'cbnz' by google like:

    cbnz site:infocenter.arm.com

```
    $ sudo apt-get install gdb-multiarch
    $ gdb-multiarch sysinit/init
    gdb> 
```

# Front-end: insight

https://stackoverflow.com/questions/26190094/setup-insight-on-ubuntu-14-04-or-linux-mint-17

Well for the sake of jeff duntemann's book , I made a simple portable version of insight , All you have to do is to download a single binary ( AppImage ) and mark it executable , Then you are ready to rock. Remember this is only for 64 Bits for now. Also you have to use absolute paths for command line. This method does not require root and does not touch the host operating system.

$ wget -O Insight-continuous-x86_64.AppImage https://git.io/vp4uE
$ chmod +x ./Insight-continuous-x86_64.AppImage 
$ ./Insight-continuous-x86_64.AppImage # Thats it.
See the project at https://github.com/antony-jr/insight

I repeat that this project was created by me , only the build scripts and not the source files.


# TUI command/shortcut:

    wh			Enter TUI, but now cannot leave TUI mode use command
    Ctrl-x a		switch tui-mode, then should focus cmd, in tui-mode, cannot use log-redirect
    Ctrl+C		if enter <TAB> and make gdb dead-like, you can enter this to interrupt current command and back to gdb interact win
    layout src		Standard layout—source on top, command window on the bottom
    layout asm		Just like the "src" layout, except it's an assembly window on top
    layout split	Three windows: source on top, assembly in the middle, and command at the bottom
    layout reg		Opens the register window on top of either source or assembly, whichever was opened last
    tui reg general	Show the general registers
    tui reg float	Show the floating point registers
    tui reg system	Show the "system" registers
    tui reg next	Show the next page of registers


# howto

## gdbserver

gdbserver is a program that allows you to run GDB on a different machine than the one which is running the program being debugged.

```

Table: gdbserver sample
| =======================================           | =============================================== |
| remote embedded env: gdbserver                    | local linux: gdb code                           |
|                                                   |                                                 |
| target> gdbserver comm program [args ...]         |                                                 |
| =======================================           | =============================================== |
|                                                   |                                                 |
| [=single process mode=]                           |                                                 |
| ---------------------------------------           | --------------------------------------------    |
| $ gdbserver localhost:2000 my_prg                 | $ gdb my_prg                                    |
| >  Process program created; pid = 2045            | (gdb) target remote 192.168.1.10:2000           |
| >  Listening on port 2000                         | (gdb) b main                                    |
|                                                   | (gdb) run                                       |
|                                                   |                                                 |
| $ gdbserver :2000 --attach pid                    | $ gdb my_prg                                    |
| >  Process program created; pid = 2045            | (gdb) target remote 192.168.1.10:2000           |
| >  Listening on port 2000                         | (gdb) b main                                    |
|                                                   | (gdb) run                                       |
|                                                   |                                                 |
| $ gdbserver host:2345 /uploaded/to/my_prg my-arg1 | $ gdb my_prg                                    |
| >  Process program created; pid = 2045            | (gdb) target remote 192.168.1.10:2000           |
| >  Listening on port 2000                         | (gdb) b main                                    |
|                                                   | (gdb) run                                       |
|                                                   |                                                 |
| [=Multi-process Mode=]                            |                                                 |
| ---------------------------------------           | --------------------------------------------    |
| $ gdbserver --multi localhost:2000                | $ gdb                                           |
| > Listening on port 2000                          | (gdb) target extended-remote 192.168.1.10:2000  |
|                                                   | (gdb) set remote exec-file /uploaded/to/my_prg  |
|                                                   | (gdb) file ./sysinit/my_prg                     |
|                                                   | (gdb) b main                                    |
|                                                   | (gdb) run                                       |
| ---------------------------------------           | --------------------------------------------    |
| ***************************************           | ********************************************    |
|                                                   |                                                 |
| #######################################           | ############################################    |
| =======================================           | =============================================== |

```
## ignore signal

For the same SIGUSR1 example above, you can query the gdb handler rules like so:

```gdb
    (gdb) info signal SIGUSR1
    Signal        Stop      Print   Pass to program Description
    SIGUSR1       Yes       Yes     Yes             User defined signal 1
    And if deemed to not be of interest, where you just want your program to continue without prompting or spamming, something like the following does the trick:

    (gdb) handle SIGUSR2 noprint nostop
    Signal        Stop      Print   Pass to program Description
    SIGUSR1       No        No      Yes             User defined signal 1
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

## Set variable's value.

```gdb
    (gdb) set variable node->_data = 5
    (gdb) set variable $address = &(node->_data)
    (gdb) set variable *(int *)($address) = 1024
```

## breakpoints

```gdb
    # break
    enable/disable <#>		# Enable/disable breakpoints
    tbreak			# Break once, and then remove the breakpoint
    rbreak			# break on function matching regular expression
        (gdb) rbreak file.c:.   # break on all function of the file
        (gdb) rbreak file.cpp:.*StudentClass.*

    save breakpoints <file>	# save breakpoints
    source <file>
    del br 1-11
    break <line-func> if COND
    cond 1 strcmp($secret_code, c ) == 0	# set conditional to existed breakpoint
```

## watchpoints: monitor the variable's value changed

```gdb
    info watchpoints [n...]

    # break when the addr's content be written again
    watch *(int *) 0x600850

    # break when the value of expr is read
    rwatch [-l|-location] expr [thread threadnum] [mask maskvalue]

    # break when expr is either read from or written into
    awatch [-l|-location] expr [thread threadnum] [mask maskvalue]
```

## check data

```gdb
    info registers
        - $pc program counter register
        - $sp stack pointer
        - $fp current stack frame
        - $ps processor status

    print (‘x’, ‘d’, ‘u’, ‘o’, ‘t’, ‘a’, ‘c’, ‘f’, ‘s’)
    x/nfu addr    n, f, and u are all optional parameters that specify how much memory to display and how to format it;
                  u, the unit size:
                    - b Bytes,
                    - h Halfwords(two bytes),
                    - w Words (four bytes). This is the initial default.
                    - g Giant words (eight bytes).

    p /x $pc		# print the program counter in hex with
    x 3/i $pc		# print the instruction to be executed next 3 with
    set $sp += 4	# add four to the stack pointer(10)

    p (int [3]) *a	$8 = {1, 2, 3}
    p *a@3		$11 = {1, 2, 3}
    p/x

    x/x <addr>	displays elements in hex,
    x/10x $sp	check the stack in HEX
    x/d		displays them as signed decimals,
    x/c		displays characters,
    x/i		disassembles memory as instructions,
    x/s		interprets memory as C strings.
    x/5i main	ASM of main
    x/s <var>	examine an ansistring?
    x/s 0xffffffff81946000
```

### Gdb trick: array

```sh
(gdb) p *a@3

(gdb) set $pos=0
(gdb) print array[$pos++]
  content of array[0]
(gdb)
  content of array[1]
(gdb)
  content of array[2]
```

## Automatic batch commands

### batch from terminal

```shell
    $ gdb --batch --command=test.gdb --args ./test.exe 5
```

### .gdbinit

gdb executes file .gdbinit before running the program

### hit breakpoint automatic execute batch commands

```sh
    $ cat test.gdb
    set width 0
    set height 0
    set verbose off

    # at entry point - cmd1
    br main
    commands 1		# assume break-num =#1
      print argc
      continue
    end

    $ gdb --batch --command=test.gdb --args ./test.exe 5
```

  [2]: https://sourceware.org/gwiki/FAQ
  [3]: https://blogs.oracle.com/ksplice/entry/8_gdb_tricks_you_should
  [4]: http://sourceware.org/gdb/onlinedocs/gdb/Continuing-and-Stepping.html
  [5]: https://github.com/huawenyu/neogdb.vim
  [6]: http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0489f/CIHDGFEG.html
