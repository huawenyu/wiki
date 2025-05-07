# QuickStart

## build ppstep

```sh
    # Build `ppstep` from source
    ### Download source code from: https://github.com/notfoundry/ppstep

        sudo apt install libboost-all-dev
        git clone https://github.com/notfoundry/ppstep.git
        cd ppstep
        mkdir build
        cd build
        cmake ..

    # Install nix-env
    sh <(curl -L https://nixos.org/nix/install) --daemon

    # Install clang-format
    nix-env -iA nixpkgs.clang-tools

    # Install rlwrap with fitler feature
    ### [Source](https://github.com/hanslub42/rlwrap/)
    nix-env -iA nixpkgs.rlwrap

    # Install heytmux
    sudo apt install ruby ruby-dev rubygems build-essential
    sudo gem install heytmux

    # Demo start
    code=foreach.c heytmux main.yml

    # Demo stop
    heytmux main.yml --kill
```

# Help

```plaintext
Usage: rlwrap [-options] -z ./filter.py <command>

Source:
    https://github.com/notfoundry/ppstep
    /nix/store/238vrcj4b0fcp0yivxcp7mzl1m9jrmkk-rlwrap-0.46.1/share/rlwrap/filters/rlwrapfilter.py

Pre-requirement:
    clang-format: nix-env -iA nixpkgs.clang-tools

pp-shell:
prompt: pp>
commands:
    q-quit
    s-step
    c-continue

    bt-backtrace
    ft-forwardtrace
    b-break: break call <macro>, break expand <macro>
    d-delete: delete call <macro>
process-status:
    called,exanded,rescanned,lexed
```

# Preprocessor

The Two-Phase Expansion Process:

When the preprocessor encounters a macro, it performs expansion in two key phases:
- Phase 1: Argument Expansion (Blue Paint)
- Phase 2: Rescan & Further Expansion

##  Phase 1: Argument Expansion (Blue Paint)

Blue-painting: The preprocessor marks tokens as "blue" (not yet expanded) or "white" (already expanded)
- Arguments are expanded first (turned "white") unless they are:
  + Operands of # (stringification) or ## (token pasting)
  + Part of a nested macro call

## Phase 2: Rescan & Further Expansion

After initial substitution, the result is rescanned:
- Any new macro calls generated during substitution are expanded
- This repeats until no more expansions are possible

## Macro Expansion

- Step 1: Argument Collection
- Step 2: Argument Expansion (If Needed)
- Step 3: Macro Substitution
- Step 4: Rescanning (Blue-Painting & Re-expansion)
  The preprocessor prevents infinite recursion by marking expanded macros as "white."
  + The substituted text is rescanned for further macro expansions.
  + Tokens are marked as blue (not yet expanded) or white (already expanded).
  + Blue tokens are eligible for re-expansion.
  + White tokens are left as-is (prevents infinite recursion).

```c
    #define A 1
    #define B A
    #define C B   // Rescanning happens here:
                  // C → B → A → 1
```

```c
    #define A B
    #define B A     // Expands once, then stops
    A               // → B → A (but A is now "white," so expansion stops)
```

- Step 5: Stringification (#) & Token Pasting (##), no expansion of it's operand,

- Blue-painting explains why some arguments aren't expanded
- Rescanning enables multi-step macro expansion
- # and ## change expansion rules for their operands
- Indirect expansion (like STR()) is often needed for full macro expansion

## Understanding DEFER and OBSTRUCT macros

[Defer](https://stackoverflow.com/questions/29962560/understanding-defer-and-obstruct-macros)

```c
#define EMPTY()
#define DEFER(id) id EMPTY()
#define OBSTRUCT(...) __VA_ARGS__ DEFER(EMPTY)()
#define EXPAND(...) __VA_ARGS__

#define A() 123
A() // Expands to 123
DEFER(A)() // Expands to A () because it requires one more scan to fully expand
EXPAND(DEFER(A)()) // Expands to 123, because the EXPAND macro forces another scan
```

The use of macros like DEFER, and complicated C macrology in general, depends on understanding
how the C preprocessor actually expands macro expressions. It doesn't just attempt to reduce
all expression trees the way a conventional programming language does, but rather, it works on
a linear token stream, and has an implicit "cursor" at the point where it's currently examining
the stream for possible replacements. Within any given "stack frame" of the expansion process,
the cursor never moves backwards, and once a token has been passed in the stream it is not
examined again.

Walking through the first example of DEFER's operation:

```c
 DEFER(A)()  // cursor starts at the head of the sequence
^            // identifies call to DEFER - push current position

 DEFER( A )()  // attempt to expand the argument (nothing to do)
       ^
 // replace occurrences of id in DEFER with A,
 // then replace the call to it with the substituted body

 A EMPTY() ()  // pop cursor position (start of pasted subsequence)
^              // doesn't find an expansion for A, move on
 A EMPTY() ()  // move to next token
  ^            // EMPTY() is a valid expansion
 A  ()         // replace EMPTY() with its body in the same way
   ^           // continuing...
 A ()          // `(` is not a macro, move on
  ^
 A ( )         // `)` is not a macro, move on
    ^
 A ()          // end of sequence, no more expansions
     ^
```

The cursor moved past A during the "rescan" of DEFER's body, after the arguments had been
substituted, which is the second and last attempt to expand that set of tokens. Once the cursor
has moved past A it does not return to it during that expansion sequence, and since the "rescan"
is at the top level there is no following expansion sequence.

Now consider the same expression, but wrapped in a call to EXPAND:
```c
 EXPAND(DEFER(A)())    // cursor starts at the head etc.
^                      // identifies call to EXPAND
 
 EXPAND( DEFER(A)() )  // attempt to expand the argument
        ^              // this does the same as the first
		               // example, in a NESTED CONTEXT
					   
 // replace occurrences of __VA_ARGS__ in EXPAND with A ()
 // then replace the call with the substituted body
 
 A ()          // pop cursor position (start of pasted subsequence)
^              // identifies A, and can expand it this time
```

Because argument lists are expanded in a stacked context, and the cursor position is restored
to the position in front of the original call for the rescan pass, placing a macro invocation in
any macro's argument list - even one that actually does nothing, like EXPAND - gives it a "free"
extra run over by the expansion cursor, by resetting the cursor's position in the stream an extra
time for an extra rescan pass, and therefore giving each freshly constructed call expression
(i.e. the pushing together of a macro name and a parenthesized argument list) an extra chance
at being recognised by the expander. So all EVAL does is give you 363 (3^5+3^4+3^3+3^2+3,
someone check my math) free rescan passes.

So, addressing the questions in light of this:

"painting blue" doesn't work quite like that (the explanation in the wiki is a bit misleadingly
phrased, although it's not wrong). The name of a macro, if generated within that macro, will
be painted blue permanently (C11 6.10.3.4 "[blue] tokens are no longer available for further
replacement even if they are later (re)examined"). The point of DEFER is rather to ensure that
the recursive invocation doesn't get generated on the macro's expansion pass, but instead is
...deferred... until an outer rescan step, at which point it won't get painted blue because
we're no longer within that named macro. This is why REPEAT_INDIRECT is function-like; so that
it can be prevented from expanding into anything mentioning the name of REPEAT, as long as
we're still within the body of REPEAT. It requires at least one further free pass after the
originating REPEAT completes to expand away the spacing EMPTY tokens.

yes, EXPAND forces an additional expansion pass. Any macro invocation grants one extra expansion
pass to whatever expression was passed in its argument list.

the idea of DEFER is that you don't pass it a whole expression, just the "function" part;
it inserts a spacer between the function and its argument list that costs one expansion pass
to remove.

therefore the difference between EXPAND and DEFER is that DEFER imposes the need for an extra
pass, before the function you pass it gets expanded; and EXPAND provides that extra pass. So
they are each other's inverse (and applied together, as in the first example, are equivalent
to a call using neither).

yes, OBSTRUCT costs two expansion passes before the function you pass it gets expanded. It
does this by DEFERing the expansion of the EMPTY() spacer by one (EMPTY EMPTY() ()), burning
the first cursor reset on getting rid of the nested EMPTY.

OBSTRUCT is needed around REPEAT_INDIRECT because WHEN expands (on true) to a call to EXPAND,
which will burn away one layer of indirection while we're still within the call to REPEAT. If
there was only one layer (a DEFER), the nested REPEAT would be generated while we're still in
REPEAT's context, causing it to be painted blue and killing the recursion right there. Using
two layers with OBSTRUCT means that the nested REPEAT won't be generated until we reach the
rescan pass of whatever macro call is outside REPEAT, at which point we can safely generate
the name again without it being painted blue, because it's been popped from the no-expand stack.

So, this method of recursion works by using an external source of a large number of rescan
passes (EVAL), and deferring the expansion of a macro's name within itself by at least one
rescan pass so it happens further down the call stack. The first expansion of the body of REPEAT
happens during the rescan of EVAL[363], the recursive invocation is deferred until the rescan
of EVAL[362], the nested expansion deferred... and so on. It's not true recursion, as it can't
form an infinite loop, but instead relies on an external source of stack frames to burn through.

# Ref

https://github.com/hirrolot/awesome-c-preprocessor
http://jhnet.co.uk/articles/cpp_magic
https://stackoverflow.com/questions/29962560/understanding-defer-and-obstruct-macros
https://github.com/pfultz2/Cloak/wiki
