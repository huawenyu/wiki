# Doc
https://embeddedartistry.com/blog/2020/07/27/exploiting-the-preprocessor-for-fun-and-profit/
https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms
https://renenyffenegger.ch/notes/development/languages/C-C-plus-plus/preprocessor/macros/__VA_ARGS__/index
https://codecraft.co/2014/11/25/variadic-macros-tricks/
https://belkadan.com/blog/2016/08/Macromancy/
https://belkadan.com/blog/2016/08/Macromancy-2/

IDE-online: https://godbolt.org/           Give a gcc option `-E` to get macros.

# Stringify

That was the standard the codified the # and ## operators in macros and mandates recursively
expanding macros in args before substituting them into the body **if and only if** the body does
not apply a # or ## to the argument.

This macro concatenates two expressions, and we want the same behavior:

```c
  #define PP_STRINGIFY_IMPL(X) #X
  #define PP_STRINGIFY(X) PP_STRINGIFY_IMPL(X)


  #define VALUE 42
  auto x = PP_STRINGIFY_IMPL(VALUE); // yields "VALUE"
  auto y = PP_STRINGIFY(VALUE); // "42"


  #define NAME Thingy
  #define INDEX _1
  int PP_CONCAT_IMPL(NAME, INDEX) = 1; // declares a variable name 'NAMEINDEX'
  int PP_CONCAT(NAME, INDEX) = 1; // declares a variable name 'Thingy_1'
```

# Generic-program: '_Generic'

## choose function depend on type

Provides a way to choose one of several expressions at compile time, based on a type of a controlling expression:

	_Generic ( controlling-expression , association-list )		(since C11)


```c
  #include <stdio.h>
  #include <math.h>

  // Possible implementation of the tgmath.h macro cbrt
  #define cbrt(X) _Generic((X), \
                long double: cbrtl, \
                    default: cbrt,  \
                      float: cbrtf  \
  )(X)

  int main(void)
  {
      double x = 8.0;
      const float y = 3.375;
      printf("cbrt(8.0) = %f\n", cbrt(x)); // selects the default cbrt
      printf("cbrtf(3.375) = %f\n", cbrt(y)); // converts const float to float,
                                              // then selects cbrtf
  }
```

## choose function depend on args number

### Step 1: find the size of the variadic macro.

```c
  #define PP_NARG(...)  PP_NARG_(__VA_ARGS__, PP_RSEQ_N())
  #define PP_NARG_(...) PP_ARG_N(__VA_ARGS__)

  #define PP_RSEQ_N() 8, 7, 6, 5, 4, 3, 2, 1, 0
  #define PP_ARG_N(_1, _2, _3, _4, _5, _6, _7, _8,  N, ...) N

  //PP_NARG(1,2,3) -> yields 3
  //
  // PP_ARG_N gets called with the sequence we pass into PP_NARG, which is concatenated with
  //   the integer sequence declared by PP_RSEQ_N. Then the element at position 9 is returned from
  //   PP_ARG_N. Since PP_RSEQ_N is defined as a sequence where PP_RSEQ_N[N] == 8 - N , this gives
  //   us the size. Stated in another way, the arguments passed to PP_NARG shift the sequence of
  //   PP_RSEQ_N.
  //
  // => PP_NARG_(1, 2, 3, 8, 7, 6, 5, 4, 3, 2, 1, 0)
  // => PP_ARG_N(1, 2, 3, 8, 7, 6, 5, 4, 3, 2, 1, 0)
  // => PP_ARG_N(_1, _2, _3, _8, _7, _6, _5, _4,  3, 2, 1, 0)
  // => PP_ARG_N(_1, _2, _3, _4, _5, _6, _7, _8,  N, ...) N
  // => 3
  //
  //
  // PP_NARG(1,2,3) -> PP_NARG_(1,2,3, PP_RSEQ_N())
  //              -> PP_NARG_(1, 2, 3, 8, 7, 6, 5, 4, 3, 2, 1, 0)
  // #define PP_ARG_N(_1, _2, _3, _4, _5, _6, _7, _8,  N, ...) N
  //         PP_ARG_N( 1,  2,  3,  8,  7,  6,  5,  4,  3, 2, 1, 0) -> 3 // because 3 == N
  //
  //
  //  To visualize it with concatenated strings:
  #define STRLEN(X) ( X "876543210" )[8] - '0'
  // If we put in "Hello" the string concatenation gives us the following:
  //  STRLEN(X) ( "Hello" "876543210" )[8] - '0'
  //  "Hello876543210"[8] == '5'
  //       ^
```

### Step 2: Generate a new function by args count.

With the ability to determine the size of our variadic list it now actually easy to implement the overload:

    #define PP_OVERLOAD(Macro, ...) PP_CONCAT(Macro, PP_NARG(__VA_ARGS__))

```c
// #define PP_CONCAT_IMPL(x, y) x##y
// #define PP_CONCAT(x, y) PP_CONCAT_IMPL( x, y )
//
// #define PP_NARG(...)  PP_NARG_(__VA_ARGS__, PP_RSEQ_N())
// #define PP_NARG_(...) PP_ARG_N(__VA_ARGS__)
//
// #define PP_RSEQ_N() 8, 7, 6, 5, 4, 3, 2, 1, 0
// #define PP_ARG_N(_1, _2, _3, _4, _5, _6, _7, _8,  N, ...) N

// #define PP_OVERLOAD(Macro, ...) PP_CONCAT(Macro, PP_NARG(__VA_ARGS__))

void my_func_1(const char *, int);
void my_func_2(const char *, int, int);
void my_func_3(const char *, int, int, int);

// Please note that this solution doesn’t work with zero arguments.
#define my_func(fmt, ...) PP_OVERLOAD(my_func_, __VA_ARGS__)(fmt, __VA_ARGS__)

void test()
{
    my_func("Thingy", 1);
    my_func("Thingy", 1, 2);
    my_func("Thingy", 1, 2, 3);
}
```


# typeof

https://gcc.gnu.org/onlinedocs/gcc/Typeof.html

```c
  #define max(a,b) \
    ({ typeof (a) _a = (a); \
        typeof (b) _b = (b); \
      _a > _b ? _a : _b; })
```

## use of typeof:

```c

  typeof (*x) y;		// This declares y with the type of what x points to.
  typeof (*x) y[4];		// This declares y as an array of such values.

  typeof (typeof (char *)[4]) y;	// This declares y as an array of pointers to characters, equivalent: char *y[4];
      // To see the meaning of the declaration using typeof, and why it might be a useful way to write, rewrite it with these macros:
      #define pointer(T)  typeof(T *)
      #define array(T, N) typeof(T [N])

      // Now the declaration can be rewritten this way:
      array (pointer (char), 4) y;
      // Thus, array (pointer (char), 4) is the type of arrays of 4 pointers to char.
```

# __COUNTER__

Predefined preprocessor macro __COUNTER__
- __COUNTER__ is a non-standard compiler extension for the GNU compiler. Apparently, it's also implemented in Microsoft's compiler and the clang compiler.
- __COUNTER__ evaluates to an integer literal whose value is increased by one every time it is found in a source code text.

```c
  #include <stdio.h>

  int a = __COUNTER__;
  int b = __COUNTER__;
  int c = __COUNTER__;

  int main() {
    printf("__COUNTER__=%d\n", __COUNTER__); // output 3
    printf("a=%d, b=%d, c=%d\n", a, b, c);   // output: a=0, b=1; c=2
  }

```
## Reset __COUNTER__ macro to zero

Reset the __COUNTER__ macro at the start of a header file to make its evaluation within the header file consistent over several compile units?

```c
enum { COUNTER_BASE = __COUNTER__ };

#define LOCAL_COUNTER (__COUNTER__ - COUNTER_BASE)
```

# Compile ifndef-fence code: change ifndef to if (true)

## Support MACRO style: `#define CONFIG_XYZ 1`

https://plus.google.com/+LinusTorvalds/posts/9gntjh57dXt

```c
    /*
     * Reference: https://plus.google.com/+LinusTorvalds/posts/9gntjh57dXt
     *
     * Given a configuration macro such as:
     *     #define CONFIG_XYZ 1
     *
     * This macro allows one to write
     *
     *     if (is_set(CONFIG_XYZ)) {
     *         ...
     *     }
     *
     * without having to make ugly #ifdef sections.  It will also work in
     * preprocessor conditions such as:
     *
     *       #if is_set(CONFIG_XYZ)
     *
     * NOTE: This only works when the config macro is set to 1, as above,
     * and not all definitions in our platform headers do.
     *
     */

    #define is_set(macro) is_set_(macro)
    #define macrotest_1 ,
    #define is_set_(value) is_set__(macrotest_##value)
    #define is_set__(comma) is_set___(comma 1, 0)
    #define is_set___(_, v, ...) v
```

## Support MACRO style: `#define CONFIG_XYZ`

https://stackoverflow.com/questions/5464170/using-definedmacro-inside-the-c-if-statement

Ok, based on the previous post I got this idea, which seems to work:

```c
    #define is_define_(NAME) ((#NAME)[0] == 0)
    #define is_define(NAME) is_define_(NAME)
```

This will check if NAME is defined and therefore it expands to the empty string with 0 at its first character, or it is undefined in which case it is not the empty string. This works with GCC, so one can write

```c
    if (is_define(MACRO) ) {
    }
```

