# REPL(Read, Eval, Print, Loop)

https://stackoverflow.com/questions/5671214/is-lisp-the-only-language-with-repl

There are languages other than Lisp (ruby, scala) that say they use REPL (Read, Eval, Print, Loop).

# A implement: reple - interactive command line env

Note: Should support input from pipe '|' or file, and then it's better intergrated with vim.

https://github.com/BenBrock/reple

"Replay-based" REPLs for compiled languages.

reple provides an "interpreter" (REPL) for compiled languages.
Each time you enter a line of code, reple will add the new code to your program,
     compile and run the new iteration of your program,
     and then print any new output. reple currently supports
     C, C++, Go, Rust, UPC, MPI, DASH, and BCL.

## Usage

    pip3 install reple
    reple -env cxx

## Adding a new language

Adding a new language to reple is easy.
All you need to do is write a short JSON file that describes:
  1. how to append REPL lines to form a program,
  2. how to compile and run a program,
  3. terminal options, which are things like characters that enclose expressions that can span multiple lines (like {} in C).

These config files are typically only about 20 lines, and you can find examples in /reple/configs.

# Vim related

## vim-slime

https://github.com/jpalardy/vim-slime

Many languages are supported without modifications, while others might tweak the text without explicit configuration:
  - coffee-script
  - fsharp
  - haskell / lhaskell -- README
  - ocaml
  - python / ipython -- README
  - scala
  - sml

## vim-repl

https://github.com/sillybun/vim-repl

