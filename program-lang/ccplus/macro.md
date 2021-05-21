
# Tricks: [Using](Using) defined(MACRO) inside the C if statement

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

