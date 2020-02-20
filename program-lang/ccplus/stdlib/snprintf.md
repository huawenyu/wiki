# Usage

```c
    char dst[20];
    char src[20];

    scanf("%s", src);
    snprintf(dst, sizeof(dst), "%s-more", src);
    printf("%s\n", dst);
```

gcc8 version build error:

```sh
    test.c:8:33: warning: ‘/input’ directive output may be truncated writing 6 bytes into a region of size between 1 and 20 [-Wformat-truncation=]
    snprintf(dst, sizeof(dst), "%s-more", src);
                                 ^~~~~~
    test.c:8:3: note: ‘snprintf’ output between 7 and 26 bytes into a destination of size 20
    snprintf(dst, sizeof(dst), "%s-more", src);
    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

## -Wall: Why Is String Truncation a Problem?

It is well-known why buffer overflow is dangerous: writing past the end of an object can overwrite data in adjacent storage, resulting in data corruption. In the most benign cases, the corruption can simply lead to incorrect behavior of the program. If the adjacent data is an address in the executable text segment, the corruption may be exploitable to gain control of the affected process, which can lead to a security vulnerability. (See CWE-119 for more on buffer overflow.)

But string truncation does not overwrite any data, so why is it a problem? Inadvertently truncating a string can be considered data corruption: it is the creation of a sequence of characters from which some of the trailing characters are unintentionally missing. String truncation can take one of two general forms. One results in a NUL-terminated string that is shorter than the sum of the lengths of the concatenated strings. The other results in a sequence of bytes not terminated by a NUL character: that is, the result is not a string. Using such a result where a string is expected is undefined. (See CWE-170 for more about weaknesses resulting from improper string termination.) The different kinds of truncation are caused by different functions and their detection is controlled by different warning options, both of which are enabled by -Wall.

circumvent this kind of warning by check the return value from `snprintf`:

```c
    snprintf(dst, sizeof(dst), "%s-more", src);
    int ret = snprintf(dst, sizeof(dst), "%s!", src);
```

## return

    On error, Note that snprintf() only returns a negative number on error, though.
    On Succ, it returns the number of characters it have been written, plus one more to include NULL terminal '\0';
    On truncation, it returns the number of characters (exclude the NULL terminal '\0') it would have written if had the buffer been long enough
