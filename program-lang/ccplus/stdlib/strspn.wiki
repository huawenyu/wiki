# sample

     size_t strspn(const char *s, const char *accept);
     size_t strcspn(const char *s, const char *reject);

     注意两个函数的返回值的位置，都是按 s 的首位置为 0 开始计数的。

     * 第一个函数的作用是，从 s 第一个字符开始，逐个检查字符与 accept 中
     任意字符是否不相同，若不相同，则返回第一次出现不相同的位置且程序
     正常退出，否则返回的是 s 的长度.

     * 第二个函数作用是，从 s 第一个字符开始，逐个检查字符与 reject 中任
     意字符是否相同，若相同，则返回第一次出现相同的位置且程序正常退出,
     否则返回的是 s 的长度.

```c
/*
 * To understand the usage of strspn()
 */

#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
        char *str1 = "1234567890";
        char *str2 = "1234567890";

        char *str3 = "gdfa1234af5";
        char *str4 = "ha";

        // 10
        printf("%s in %s is %d\n", str2, str1, strspn(str1, str2));

        // 3
        printf("%s in %s is %d\n", str4, str3, strcspn(str3, str4));

        return 0;
}
```

