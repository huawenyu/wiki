# Shell Setup

## Change Shell
```sh
    [ejr@hobbes ejr]$ cat /etc/shells
        /bin/bash
        /bin/sh
        /bin/tcsh
        /bin/csh
        /bin/zsh

    [ejr@hobbes ejr]$ chsh
        Changing shell for ejr.
        Password:
        New shell [/bin/bash]: /bin/zsh
        Shell changed.

    ejr@hobbes ~ $ su - ejr     <=== check the new shell
        Password:
```

## Shortkey

Command Line Shortkey

```
    CTRL + A                <<< Move to the beginning of the line
    CTRL + E                <<< Move to the end of the line

    CTRL + U                <<< not work linux, Clear the characters on the line before the current cursor position
    CTRL + K                <<< Clear the characters on the line after the current cursor position

    CTRL + _                <<< Undo the last change

    <Others>:
    CTRL + [left arrow]     <<< Move one word backward (on some systems this is ALT + B)
    CTRL + [right arrow]    <<< Move one word forward (on some systems this is ALT + F)
    ESC + [backspace]       <<< Delete the word in front of the cursor
    Alt + [backspace]       <<< Delete the word in front of the cursor
    CTRL + W                <<< Delete the word in front of the cursor
    ALT + D                 <<< Delete the word after the cursor

    CTRL + L                <<< Clear screen
    CTRL + S                <<< Stop output to screen
    CTRL + Q                <<< Re-enable screen output
    CTRL + C                <<< Terminate/kill current foreground process
    CTRL + Z                <<< Suspend/stop current foreground process
```

## shell wildcard:

```
    ?       do you have this character, zero or one ?
    .        yes, I have just one.
    +       yes, I have at least one, one or more.
    *        who knows, have or none.
    ^        begin with
    [^]      not set
    $       end with
```

## shell Multiline

### 1. Passing multiline string to a variable:

```
    Examples of Bash cat <<EOF syntax usage:

    $ sql=$(cat <<EOF
    SELECT foo, bar FROM db
    WHERE foo='baz'
    EOF
    )
```

The $sql variable now holds newlines as well, you can check it with echo -e "$sql" cmd:

    $ echo $sql

### 2. Passing multiline string to create a script file:

```
    $ cat <<EOF > print.sh
    #!/bin/bash
    echo \$PWD
    echo $PWD
    EOF
```

The print.sh file now contains:

    #!/bin/bash
    echo $PWD
    echo /home/user

### 3. Passing multiline string to a command/pipe:

```
    $ cat <<EOF | grep 'b' | tee b.txt | grep 'r'
    foo
    bar
    baz
    EOF
```

# Shell Script

## () vs {}: prefer {cmd1;}

If you want the side-effects of the command list to affect your current shell, use {...}
If you want to discard any side-effects, use (...)

```sh
	{ echo abc; cat 1.txt; } > 2.txt
	<or>
	echo abc | cat - 1.txt > 2.txt
```

(list)

list is executed in a `subshell environment` (see COMMAND EXECUTION ENVIRONMENT below).
Variable assignments and builtin commands that affect the shell's environment do not remain in effect after the command completes.
The return status is the exit status of list.

{ list; }

list is simply executed in the `current shell environment`.
list must be terminated with a newline or semicolon.
This is known as a group command. The return status is the exit status of list.
Note that unlike the metacharacters ( and ),  { and } are reserved words and must occur where a reserved word is permitted to be recognized.  Since they do not cause a word break, they must be separated from list by whitespace or another shell metacharacter.

The first option (subshell environment) has a bunch of side effects, most if not all of which are irrelevant to your scenario; however, if redirecting a bunch of commands' output is all you need, then Option #2 here (group command) is preferred.

## $(command) vs ${variable} == $variable

```sh
	$ animal=cat
	$ echo $animal
	cat

	$ cat=tabby
	$ echo $cat
	tabby

	# !: a level of variable indirection is introduced
	$ echo ${!animal}
	tabby                           # If $animal is "cat", then ${!animal} is $cat, i.e., “tabby”

	# #: length
	$ animal=cat
	$ echo ${#animal}
	3                               # String length

	# substitution
	$ echo ${animal/at/ow}
	cow                             # Substitution
```

## pass all files to a command

```sh
ls -1 *.json | sed 's/.json$//' | while read col; do 
    mongoimport -d db_name -c $col < $col.json; 
done
```

## read

### read array

```sh
    echo "one two three four" | while read -a wordarray; do
      echo ${wordarray[1]}
    done

    <<<output:
    two
```

### pipe line with `find`

For every iteration of the while loop, read reads one word (a single file name) and puts that value into the variable `file`, which we specified as the last argument of the read command.

When there are no more file names to read, read will return false, which triggers the end of the while loop, and the command sequence terminates.

```sh
    while IFS= read -r -d $'\0' file; do
      echo "$file"
    done < <{find . -print0}
```

 - *while IFS=*
    `IFS=` (with nothing after the equals sign) sets the `internal field separator` to "no value".
    Spaces, tabs, and newlines are therefore considered part of a word.
    Note:
        that IFS= comes after while, ensuring that IFS is altered only inside the while loop. For instance, it won't affect find.

 - *read -r*
    Using the -r option is necessary to preserve any backslashes in the file names.

 - *-d $'\0'*
    The -d option sets the newline delimiter. Here, we're setting it to the NULL character

 - *< <{find . -print0;}*
    + Here, `find . -print0` will create a list of every file in and under `.` (the working directory) and delimit all file names with a NULL. 
    + Enclosing the find command in `<{ ... }` performs process substitution: the output of the command can be read like a file. In turn, this output is redirected to the while loop using the first "<".

