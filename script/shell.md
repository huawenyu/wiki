# sed

## How to pass a variable containing slashes to sed

Use an alternate regex delimiter as sed allows you to use `any` delimiter (including control characters):

    """ Common choices for the delimiter are the pipe character | or the hash #
    sed "s~$var~replace~g" $file
    <or>
    sed "s;$var;replace;g" $file

# awk

## awk replace a specific pattern under another pattern

    $ cat test.txt
    [ABC]
    value1=bla
    value2=bla
    value3=bla
    [XYZ]
    value1=bla
    value2=bla
    value3=bla

    $ awk '
      BEGIN {FS=OFS="=";}
      /\[.*\]/ {if ($0 == "[ABC]") edit=1; else edit=0;}
      {if (edit && $1 == "value1" ) $2="notbla";}1
     ' test.txt

## print only matching field itself and not line

     $ awk 'match($0,/regexp/) {print substr($0,RSTART,RLENGTH)}' inputfile

     !! for multiple matched
     $ awk '/regexp/{for(i=1;i<=NF;++i)if($i~/regexp/)print $i}' /path/to/inputfile

     <or>
     !! <output> cd
     $ echo "abcdef" | awk 'match($0, /b(.*)e/, arr) {print arr[1]}'
     $ echo "abcdef" | awk 'match($0, /b[^e]*/) {print substr($0, RSTART+1, RLENGTH-1)}'

## Substitute a regex pattern using awk

     """ replace one or more '+' symbols present in a file with a space
     $ echo This++++this+++is+not++done | awk '{gsub(/\++/," ");}1'


## Getting shell variables into `awk`

     https://stackoverflow.com/questions/19075671/how-do-i-use-shell-variables-in-an-awk-script

may be done in several ways. Some are better than others. This should cover most of them.  If you have a comment, please leave below.

----
### Using `-v`  (The best way, most portable)
Use the `-v` option: (P.S. use a space after `-v` or it will be less portable. E.g., `awk -v var=` not `awk -vvar=`)

    variable="line one\nline two"
    awk -v var="$variable" 'BEGIN {print var}'
    line one
    line two

This should be compatible with most `awk`, and the variable is available in the `BEGIN` block as well:

If you have multiple variables:

    awk -v a="$var1" -v b="$var2" 'BEGIN {print a,b}'

**Warning**.  As Ed Morton writes, escape sequences will be interpreted so `\t` becomes a real `tab` and not `\t` if that is what you search for. Can be solved by using `ENVIRON[]` or access it via `ARGV[]`

**PS** If you like three vertical bar as separator `|||`, it can't be escaped, so use `-F"[|][|][|]"`


> Example on getting data from a program/function inn to `awk` (here date is used)

    awk -v time="$(date +"%F %H:%M" -d '-1 minute')" 'BEGIN {print time}'

----

### Variable after code block
Here we get the variable after the `awk` code. This will work fine as long as you do not need the variable in the `BEGIN` block:

    variable="line one\nline two"
    echo "input data" | awk '{print var}' var="${variable}"
    or
    awk '{print var}' var="${variable}" file

This also works with multiple variables
`awk '{print a,b,$0}' a="$var1" b="$var2" file`

Using variable this way does not work in `BEGIN` block:

    echo "input data" | awk 'BEGIN {print var}' var="${variable}"

----

### Here-string
Variable can also be added to `awk` using a [here-string][1] from shells that support them (including Bash):

    awk '{print $0}' <<< "$variable"
    test

This is the same as:

    printf '%s' "$variable" | awk '{print $0}'

P.S. this treats the variable as a file input.

----

### `ENVIRON` input
As TrueY writes, you can use the `ENVIRON` to print **Environment Variables**.
Setting a variable before running AWK, you can print it out like this:

    X=MyVar
    awk 'BEGIN{print ENVIRON["X"],ENVIRON["SHELL"]}'
    MyVar /bin/bash


----
### `ARGV` input
As Steven Penny writes, you can use `ARGV` to get the data into awk:

    v="my data"
    awk 'BEGIN {print ARGV[1]}' "$v"
    my data

To get the data into the code itself, not just the BEGIN:

    v="my data"
    echo "test" | awk 'BEGIN{var=ARGV[1];ARGV[1]=""} {print var, $0}' "$v"
    my data test

----

### Variable within the code: USE WITH CAUTION
You can use a variable within the `awk` code, but it's messy and hard to read, and as `Charles Duffy` points out, this version may also be a victim of code injection.  If someone adds bad stuff to the variable, it will be executed as part of the `awk` code.

This works by extracting the variable within the code, so it becomes a part of it.

If you want to make an `awk` that changes dynamically with use of variables, you can do it this way, but DO NOT use it for normal variables.

    variable="line one\nline two"
    awk 'BEGIN {print "'"$variable"'"}'
    line one
    line two

Here is an example of code injection:

    variable='line one\nline two" ; for (i=1;i<=1000;++i) print i"'
    awk 'BEGIN {print "'"$variable"'"}'
    line one
    line two
    1
    2
    3
    .
    .
    1000

You can add lots of commands to `awk` this way.  Even make it crash with non valid commands.

----
### Extra info:
#### Use of double quote
It's always good to double quote variable `"$variable"`
If not, multiple lines will be added as a long single line.

Example:

    var="Line one
    This is line two"

    echo $var
    Line one This is line two

    echo "$var"
    Line one
    This is line two

Other errors you can get without double quote:

    variable="line one\nline two"
    awk -v var=$variable 'BEGIN {print var}'
    awk: cmd. line:1: one\nline
    awk: cmd. line:1:    ^ backslash not last character on line
    awk: cmd. line:1: one\nline
    awk: cmd. line:1:    ^ syntax error

And with single quote, it does not expand the value of the variable:

    awk -v var='$variable' 'BEGIN {print var}'
    $variable


# bash shell-script

## get output of a command

    """In addition to backticks `command` you can use $(command) or "$(command)" which I find easier to read, and allow for nesting.
    """  Quoting (") does matter to preserve multi-line values.

    OUTPUT="$(ls -1)"
    echo "${OUTPUT}"

    MULTILINE=$(ls \
       -1)
    echo "${MULTILINE}"


## exit if a command failed?

Try:

    my_command || { echo 'my_command failed' ; exit 1; }

Four changes:
  - Change `&&` to `||`
  - Use `{ }` in place of `( )`
  - Introduce `;` after `exit` and
  - spaces after `{` and before `}`

Since you want to print the message and exit only when the command fails ( exits with non-zero value) you need a `||` not an `&&`.

    cmd1 && cmd2

will run `cmd2` when `cmd1` succeeds(exit value `0`). Where as

    cmd1 || cmd2

will run `cmd2` when `cmd1` fails(exit value non-zero).
Using `( )` makes the command inside them run in a ***sub-shell*** and calling a `exit` from there causes you to exit the sub-shell and not your original shell, hence execution continues in your original shell.
To overcome this use `{ }`
The last two changes are required by bash.

