# neovim: substitue vim on Unix-Like OSs

## Shortcut

Vim provides many ways to move the cursor. Becoming familiar with them leads to more effective text editing.

h   move one character left
j   move one row down
k   move one row up
l   move one character right
w   move to beginning of next word
b   move to previous beginning of word
e   move to end of word
W   move to beginning of next word after a whitespace
B   move to beginning of previous word before a whitespace
E   move to end of word before a whitespace
All the above movements can be preceded by a count; e.g. 4j moves down 4 lines.

0   move to beginning of line
$   move to end of line
_   move to first non-blank character of the line
g_  move to last non-blank character of the line

gg  move to first line
G   move to last line
ngg move to n'th line of file (n is a number; 12gg moves to line 12)
nG  move to n'th line of file (n is a number; 12G moves to line 12)
H   move to top of screen
M   move to middle of screen
L   move to bottom of screen

zz  scroll the line with the cursor to the center of the screen
zt  scroll the line with the cursor to the top
zb  scroll the line with the cursor to the bottom

Ctrl-d  move half-page down
Ctrl-u  move half-page up
Ctrl-b  page up
Ctrl-f  page down
Ctrl-o  jump to last (older) cursor position
Ctrl-i  jump to next cursor position (after Ctrl-O)
Ctrl-y  move view pane line up
Ctrl-e  move view pane line down

n   next matching search pattern
N   previous matching search pattern
*   next whole word under cursor
#   previous whole word under cursor
g*  next matching search (not whole word) pattern under cursor
g#  previous matching search (not whole word) pattern under cursor
gd  go to definition/first occurrence of the word under cursor
%   jump to matching bracket { } [ ] ( )

fX  to next 'X' after cursor, in the same line (X is any character)
FX  to previous 'X' before cursor (f and F put the cursor on X)
tX  til next 'X' (similar to above, but cursor is before X)
TX  til previous 'X'
;   repeat above, in same direction
,   repeat above, in reverse direction

See :help {command} (for example, :help g_) for all of the above if you want more details.

## vim command line move:

  :h cmdline-editing

for details. I am listing a few of the interesting non-arrow commands that do something similar to what you want.

ctrl-b: cursor to beginning of command-line
ctrl-e: cursor to end of command-line
ctrl-w: delete the word before the cursor
ctrl-u: remove all characters between the cursor position and the beginning of the line

# handbook

## `:! command`

You can use the :! command to filter selected text through an external program. The text is
fed to stdin and substituted with the results from stdout.

    vnoremap <leader>jf :!fmt -c -w 100 -u -s <cr>

# Tags system

[Tags](https://zhuanlan.zhihu.com/p/36279445)
[C++](https://www.zhihu.com/question/47691414/answer/373700711)

## Install tags tools

### global tags [not good]: may cscope it's better

This only tool can support tags & cscope-likes at the sametime

```sh
    $ brew search global
    $ brew info global
    $ brew install global
    ### check
    $ global --version
    $ gtags --version
```

### univeral ctags [better]: is continue active from ex-ctags

```sh
    $ brew tap universal-ctags/universal-ctags
    $ brew install --HEAD universal-ctags
    ### if fail, please build from source
    $ git clone
    $ ./autogen.sh
    $ ./configure
    $ make
    $ sudo make install
```

# Indexer

1. ctags
2. cscope
3. back-end: ccls base on clang, front-end: coc.vim
4. features list:
    - support `-fms-extentions`: unname struct
    - should not take too much space, also keep quick
    - support shares index-cache, or every project independ

So far, `clang` could meet the requirement, we also choose `ccls`(@note:ccls) as clang-based
indexer, and use coc.vim be the vim plugins.

# text handle

## "Zoom" anchors

Vim support two kinds of regex-lookaround mode, perl-mode:
 - \@=      positive lookahead
 - \@!      negative lookahead
 - \@<=     positive lookbehind
 - \@<!     negative lookbehind

vim-mode (better use and understand):
 - \zs      set the match start pos
 - \ze      set the match end pos

There are many situations where you can use the zero-width anchors `\zs` and `\ze` instead of
positive lookaround. These anchors define the start (`\zs`) and the end (`\ze`) of the match
within the full pattern.

### Search/match Examples

`https://jdhao.github.io/2018/10/18/regular_expression_nvim/`

The text is `foobar foo barfoo`

```vim
    1. To match foo which is followed by bar (bar not part of the match):
    /foo\(bar\)\@=
    <or> The `very magic` mode is activate by preceding the search pattern with \v. In the very magic mode, you have to remove the \ character from the look around pattern.
    /\vfoo(bar)@=
    <or>
    /foo\zebar

    2. Match foo which is not followed by bar
    /foo\(bar\)\@!

    3. Match foo which is preceded by bar
    /\(bar\)\@<=foo
    <or>
    /bar\zsfoo

    4. Match foo which is not preceded by bar
    /\(bar\)\@<!foo

* `foo\zsbar` will match `bar` preceded by `foo` (`foo` not part of the match)
* `foo\zebar` will match `foo` followed by `bar` (`bar` not part of the match)
* `myFunction(\zs.*\ze)` will match the parameters in a function call *(for demonstration purposes, I'm not focusing on greedy vs non-greedy matching)*
```

### Putting it to use

These become most useful when using the `:substitute` command. For example, say I wanted to replace the parameters in a function call to `myFunction()` with `foo`:

    :%s/myFunction(\zs.*\ze)/foo/

This will leave `myFunction(` and `)` intact, and you don't have to worry about capturing them in your *pattern* or repeating them in your *replacement*.

You could do this using the lookaround feature of Vim's regex, but it's quite clunky:

    :%s/\(myFunction(\)\@<=.*\()\)\@=/foo/

(I find this syntax causes me to forget what I was trying to do in the first place.)

### You still need lookaround sometimes

There are still situations where you need lookaround. Using `\zs` and `\ze` are great for
simple situations where you have *something before* followed by *text to match* followed by
*something after*. But if it's more complex than that, you'll probably have to stick to the
heavier lookaround syntax.

### Fun fact

Though they're considerably uglier, Vim's lookarounds are more powerful than those in PCRE! They
support variable-length negative lookbehind, meaning you can assert that some pattern whose
length is not predetermined is *not* before your match.

PCRE doesn't support this, as it's fairly computationally expensive. That's not a huge concern
in Vim, since the most common use cases of regex tend to involve interactive searching where
the computation time is nearly imperceptible to the user. You'd probably notice it if it were
used for syntax highlighting, though.

### Relevant Help Topics

* `:help \zs`
* `:help \ze`
* `:help perl-patterns`

# vimscript

## Ref docs

 * [Anti-pattern of vimrc](http://rbtnn.hateblo.jp/entry/2014/12/28/010913)
 * [Write vim plugin using python](https://davidlowryduda.com/tag/vimscript/)
 * [Effective VimScript](https://www.arp242.net/effective-vimscript.html)
 * [vim-lambda](http://secret-garden.hatenablog.com/entry/2016/07/24/000000)

## variables

Vimscript Variable Scoping:

g:varname	The variable is global
s:varname	The variable is local to the current script file
w:varname	The variable is local to the current editor window
t:varname	The variable is local to the current editor tab
b:varname	The variable is local to the current editor buffer
l:varname	The variable is local to the current function
a:varname	The variable is a parameter of the current function
v:varname	The variable is one that Vim predefines
A similar table that I want to keep with it:

Vimscript Pseudovariables:

&varname	A Vim option (local option if defined, otherwise global)
&l:varname	A local Vim option
&g:varname	A global Vim option
@varname	A Vim register
$varname	An environment variable<Paste>

Please install plugin [vim-eval](https://github.com/amiorin/vim-eval) which can be used to execute current snippets code.

## funcion ref

  https://vim-jp.org/vimdoc-en/eval.html

### functor

```vim
    " Usage: selected; Press <leader>ee; then <leader>el to show output
    function! s:functor(a, b)
        call vlog#debug(a:a + a:b)
    endfunction

    let Func1 = function('s:functor', [16])
    call Func1(3)
```

### 1.2 Function references
                                        Funcref E695 E718
A Funcref variable is obtained with the function() function, the funcref()
function or created with the lambda expression expr-lambda.  It can be used
in an expression in the place of a function name, before the parenthesis
around the arguments, to invoke the function it refers to.  Example:

```vim
        :let Fn = function("MyFunc")
        :echo Fn()
```
                                                        E704 E705 E707
A Funcref variable must start with a capital, "s:", "w:", "t:" or "b:".  You
can use "g:" but the following name must still start with a capital.  You
cannot have both a Funcref variable and a function with the same name.

A special case is defining a function and directly assigning its Funcref to a
Dictionary entry.  Example:
```vim
        :function dict.init() dict
        :   let self.val = 0
        :endfunction
```

The key of the Dictionary can start with a lower case letter.  The actual
function name is not used here.  Also see numbered-function.

A Funcref can also be used with the :call command:
        :call Fn()
        :call dict.init()

The name of the referenced function can be obtained with string().
        :let func = string(Fn)

You can use call() to invoke a Funcref and use a list variable for the
arguments:
        :let r = call(Fn, mylist)

                                                                Partial
A Funcref optionally binds a Dictionary and/or arguments.  This is also called
a Partial.  This is created by passing the Dictionary and/or arguments to
function() or funcref().  When calling the function the Dictionary and/or
arguments will be passed to the function.  Example:
```vim
        let Cb = function('Callback', ['foo'], myDict)
        call Cb('bar')
```

This will invoke the function as if using:
```vim
        call myDict.Callback('foo', 'bar')
```

### binding a function to a Dictionary

This is very useful when passing a function around, e.g. in the arguments of
ch_open().

Note that binding a function to a Dictionary also happens when the function is
a member of the Dictionary:

        let myDict.myFunction = MyFunction
        call myDict.myFunction()

Here MyFunction() will get myDict passed as "self".  This happens when the
"myFunction" member is accessed.  When making assigning "myFunction" to
otherDict and calling it, it will be bound to otherDict:

```vim
        let otherDict.myFunction = myDict.myFunction
        call otherDict.myFunction()
```

Now "self" will be "otherDict".  But when the dictionary was bound explicitly
this won't happen:

```vim
        let myDict.myFunction = function(MyFunction, myDict)
        let otherDict.myFunction = myDict.myFunction
        call otherDict.myFunction()
```

Here "self" will be "myDict", because it was bound explicitly.

### Dictionary function

Dictionary function
                                Dictionary-function self E725 E862
When a function is defined with the "dict" attribute it can be used in a
special way with a dictionary.  Example:
```vim
        :function Mylen() dict
        :   return len(self.data)
        :endfunction
        :
        :let mydict = {'data': [0, 1, 2, 3], 'len': function("Mylen")}
        :echo mydict.len()
```

This is like a method in object oriented programming.  The entry in the
Dictionary is a Funcref.  The local variable "self" refers to the dictionary
the function was invoked from.

It is also possible to add a function without the "dict" attribute as a
Funcref to a Dictionary, but the "self" variable is not available then.

                                numbered-function anonymous-function
To avoid the extra name for the function it can be defined and directly
assigned to a Dictionary in this way:
```vim
        :let mydict = {'data': [0, 1, 2, 3]}
        :
        :function mydict.len()
        :   return len(self.data)
        :endfunction
        :
        :echo mydict.len()
```

The function will then get a number and the value of dict.len is a Funcref
that references this function.  The function can only be used through a
Funcref.  It will automatically be deleted when there is no Funcref
remaining that refers to it.

It is not necessary to use the "dict" attribute for a numbered function.

If you get an error for a numbered function, you can find out what it is with
a trick.  Assuming the function is 42, the command is:
        :function {42}


#### Functions for Dictionaries
                                                        E715
Functions that can be used with a Dictionary:
        :if has_key(dict, 'foo')        " TRUE if dict has entry with key "foo"
        :if empty(dict)                 " TRUE if dict is empty
        :let l = len(dict)              " number of items in dict
        :let big = max(dict)            " maximum value in dict
        :let small = min(dict)          " minimum value in dict
        :let xs = count(dict, 'x')      " count nr of times 'x' appears in dict
        :let s = string(dict)           " String representation of dict
        :call map(dict, '">> " . v:val')  " prepend ">> " to each item

## lambda

```vim
    let Counter = {
    \   -> function({
    \       value -> [
    \           execute("let value[0] += 1"),
    \           value[0]
    \       ][-1]
    \   }, [[0]])
    \}

    let Count = Counter()

    echo Count()
    echo Count()
    echo Count()

    " => 1
    " 2
    " 3
```

## OOP
[modularizing-vimscript](http://bling.github.io/blog/2013/08/16/modularizing-vimscript/)
[vim-jslike-oop](https://github.com/t9md/vim-jslike-oop/blob/master/vim-jslike-oop.vim)

### Modularizing VimScript

Let’s take a look at how we can create an object that is transient, has state, and contains
methods you can invoke, like any modern OOP language can do.

```vim

    function! myobject#new()
      let obj = {}
      let obj._cats = []

      function! obj.add_cat()
        call add(self._cats, '(^.^)')
      endfunction

      function! obj.meow()
        for cat in self._cats
          echo cat
        endfor
      endfunction

      return obj
    endfunction

    " somewhere else
    let x = myobject#new()
    call x.add_cat()
    call x.meow()
```

This might look familiar to some of you. Yes, it’s almost the same as the JavaScript Module
Pattern. Unfortunately, closures are not supported, but otherwise all of the usual benefits
apply here, mainly controlled visibility into private state and transience!

### static,public,private functions

You can even take this concept further and replicate “static” functions:
```vim

    function! s:object#private_static()
    endfunction

    function! g:object#public_static()
    endfunction

    function! g:object#new()
      let obj = {}

      function! obj.public()
      endfunction

      function! obj._private()
      endfunction

      return obj
    endfunction
```

Yep, same story as JavaScript here – _ variables/functions are “private”.

## Dictionaries

You create a dictionary in Vimscript by using curly braces around a list of key/value pairs. In each pair, the key and value are separated by a colon. For example:

### Creating a dictionary

    let seen = {}   " Haven't seen anything yet

    let daytonum = { 'Sun':0, 'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6 }
    let diagnosis = {
        \   'Perl'   : 'Tourettes',
        \   'Python' : 'OCD',
        \   'Lisp'   : 'Megalomania',
        \   'PHP'    : 'Idiot-Savant',
        \   'C++'    : 'Savant-Idiot',
        \   'C#'     : 'Sociopathy',
        \   'Java'   : 'Delusional',
        \}

### Access item of a dictionary

#### by bracket

    let lang = input("Patient's name? ")
    let Dx = diagnosis[lang]

If the key doesn't exist in the dictionary, an exception is thrown:

    let Dx = diagnosis['Ruby']
    **E716: Key not present in Dictionary: Ruby**

#### get() function

Using the get() function. get() takes two arguments: the dictionary itself, and a key to look up in it.

  - If the key exists in the dictionary, the corresponding value is returned;
  - if the key doesn't exist, get() returns zero.
  - Alternately, you can specify a third argument, in which case get() returns that value if the key isn't found:

    let Dx = get(diagnosis, 'Ruby')
    " Returns: 0

    let Dx = get(diagnosis, 'Ruby', 'Schizophrenia')
    " Returns: 'Schizophrenia'

#### by dot notation

    let Dx = diagnosis.Lisp                    " Same as: diagnosis['Lisp']
    diagnosis.Perl = 'Multiple Personality'    " Same as: diagnosis['Perl']

This special limited notation makes dictionaries very easy to use as records or structs or object:

    let user = {}

    let user.name    = 'Bram'
    let user.acct    = 123007
    let user.pin_num = '1337'

### Iterator

Vimscript provides functions that allow you to get a list of all the keys in a dictionary,
a list of all its values, or a list of all its key/value pairs:

    let keylist   = keys(dict)
    let valuelist = values(dict)
    let pairlist  = items(dict)

    for [k, v] in items(dict)
        let result = process(v)
        echo "Result for " k " is " result
    endfor

### Assignments and identities

    let dict2 = dict1             " dict2 just another name for dict1

    let dict3 = copy(dict1)       " dict3 has a copy of dict1's top-level elements

    let dict4 = deepcopy(dict1)   " dict4 has a copy of dict1 (all the way down)

#### compare

    if dictA is dictB
        " They alias the same container, so must have the same keys and values
    elseif dictA == dictB
        " Same keys and values, but maybe in different containers
    else
        " Different keys and/or values, so must be different containers
    endif

### Adding and removing entries

    " Add
    let diagnosis['COBOL'] = 'Dementia'

    " Merge
    call extend(diagnosis, new_diagnoses)
    call extend(diagnosis, {'COBOL':'Dementia', 'Forth':'Dyslexia'})

    " remove a single entry
    let removed_value = remove(dict, "key")
    unlet dict["key"]

### Batch-processing of dictionaries

#### function filter()

When removing multiple entries from a dictionary, it is cleaner and more efficient to use filter().
The filter() function works much the same way as for lists, except that in addition to testing
each entry's value using v:val, you can also test its key using v:key. For example:

    " Remove any entry whose key starts with C...
    call filter(diagnosis, 'v:key[0] != "C"')

    " Remove any entry whose value doesn't contain 'Savant'...
    call filter(diagnosis, 'v:val =~ "Savant"')

    " Remove any entry whose value is the same as its key...
    call filter(diagnosis, 'v:key != v:val')


#### function map

The map() built-in is particularly handy for normalizing the data in a dictionary.
For example, given a dictionary containing the preferred names of users (perhaps indexed by
userids), you could ensure that each name was correctly capitalized, like so:

    call map( names, 'toupper(v:val[0]) . tolower(v:val[1:])' )

The call to map() walks through each value, aliases it to v:val, evaluates the expression in
the string, and replaces the value with the result of that expression.
In this example, it converts the first character of the name to uppercase, and the remaining
characters to lowercase, and then uses that modified string as the new name value.

### Other dictionary-related functions

In addition to filter(), dictionaries can use several other of the same built-in functions and
procedures as lists. In almost every case (the notable exception being string()), a list function
applied to a dictionary behaves as if the function had been passed a list of the values of the
dictionary. Listing 3 shows the most commonly used functions.

    let is_empty = empty(dict)           " True if no entries at all

    let entry_count = len(dict)          " How many entries?

    let occurrences = count(dict, str)   " How many values are equal to str?

    let greatest = max(dict)             " Find largest value of any entry
    let least    = min(dict)             " Find smallest value of any entry

    call map(dict, value_transform_str)  " Transform values by eval'ing string

    echo string(dict)                    " Print dictionary as key/value pairs


### Deploying dictionaries for cleaner code

#### Passing optional arguments in a dictionary

    function! CommentBlock(comment, opt)
        " Unpack optional arguments...
        let introducer = get(a:opt, 'intro', '//'                 )
        let box_char   = get(a:opt, 'box',   '*'                  )
        let width      = get(a:opt, 'width', strlen(a:comment) + 2)" Build the comment box and put the comment inside it...
        return introducer . repeat(box_char,width) . "\<CR>"
        \    . introducer . " " . a:comment        . "\<CR>"
        \    . introducer . repeat(box_char,width) . "\<CR>"
    endfunction

# Howtos

## How to disable the leader key in vim insert mode

    https://superuser.com/questions/945329/how-to-disable-the-leader-key-in-vim-insert-mode

    The leader key is not special at all: if you don't use it in any mapping it works exactly like any other key.

Think of <leader> as some kind of constant that is automatically expanded to its current value
when it is used. When Vim sources your vimrc and sees something like:

    nnoremap <leader>b :ls<CR>:b

it will use the current value of mapleader and actually do:

    nnoremap <Space>b :ls<CR>:b

What causes the delay you are observing is the fact that <Space> is used (via the <leader>
mechanism in your case) at the beginning of an insert mode mapping: Vim is simply waiting a
bit to see if you actually want to insert a <Space> or trigger one of the registered insert
mode mappings starting with <Space>.

To see what insert mode mappings use your <leader> and where they come from, do:

  :verbose imap <space>
  :verbose imap <leader>

If the culprit is defined by a plugin, search its documentation for a way to unmap it.

Once you've found the culprits you can make a folder ~/.vim/after/plugin and put a new file
in there called something like unmap.vim. In this file you can put unmap commands. One of mine
are iunmap <Leader>is which is a mapping from a.vim. – Paymahn Moghadasian

