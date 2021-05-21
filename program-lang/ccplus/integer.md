
# Why minus integer store as Complemental-code

为什么要使用补码？想必对于原码，反码，补码大家并不陌生，计算机专业的同学都会学到这方面的一些知识。

    当初在学这部分的时候，只知道用补码可以解决0和-0的问题，但是还是没明白为什么会想到用补码。

    前阵子看了斯坦福大学关于范式编程的公开课，里面老师讲了这方面的内容，三言两语给出了一个简单明了的解释，
    顿时觉得好棒！ 思路如下：
    我们主要要解决的问题就是负数的表示，而众所周知，绝对值相等的两个正负数之和为0。
    假设我们有正数 0000 0000 0000 1111，我们如何表示其相反数呢？
    一般我们的思路是，找一个数，跟它相加的结果等于0，
    但是我们发现，要找出一个与它相加后结果等于0的数还是要略加思考一下的（因为要计算进位），
    所以，为何不找出一个与它相加后结果是1111 1111 1111 1111的数，然后该数+1即是我们所要的答案啦。
    于是，很容易的:
        0000 0000 0000 1111 + 1111 1111 1111 0000 + 1 = 1111 1111 1111 1111 + 1 = （1）0000 0000 0000 0000
    一目了然，1111 1111 1111 0001 就是我们想要的答案了，那么我们是怎么得到这个相反数的呢？
      - 首先，找出一个数与它加起来结果是全1的，这个数便是它的反码，
      - 然后这个数再加1，这便是它的相反数了，也是我们说的补码。
    我们检验一下0的情况，0000 + 1111 + 1 =（1）0000，其中1111 + 1 = （1）0000 = 0000，即+0和-0的二进制表示均为0000。

    一个小小的例子解释了为何补码需要原码取反之后再加1，是不是很神奇？

# integer

```c
    void foo(void) {
        unsigned int a = 6;
        int b = -20;

        if (a+b > a) {
            printf("> a");
        } else {
            printf("< a");
        }
    }
```

I am trying to understand what is going on with the integer promotion example above. I know that for `a = 6` and `b = -20` the output should be `> a` due to `b` being promoted to `unsigned int`. However, the output goes to `< a` if I assign `b = -5`. Shouldn't the output be the same in this case as well since the value `b = -5` is also promoted to an `unsigned int`?

## Answer

The reason for this has to do with the method in which the signed value is converted to unsigned.

Section 6.3.1.3 of the [C standard](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) regarding conversions of signed and unsigned integers dictates how this occurs:

> *2* Otherwise, if the new type is unsigned, the value is converted by repeatedly adding or subtracting one more than the maximum value that
> can be represented in the new type until the value is in the range of
> the new type.<sup>60)</sup>
>
> ...
>
> 60) The rules describe arithmetic on the mathematical value, not the value of a given type of expression.

In your example with `b` equal to -20, when it is converted to unsigned  `UINT_MAX + 1` is added to the value, so the converted value is `UINT_MAX - 19`.  When you then add the value of `a` (6), you get `UINT_MAX - 13`.  This value is larger than `a`, so `"> a"` is printed.

If you set `b` equal to -5, the converted value is `UINT_MAX - 4`.  Adding 6 to this gives you `UINT_MAX + 2`.  Since math on `unsigned int` values occurs modulo `UINT_MAX + 1`, the actual result is 1.  This is less than 6, so `"< a"` is printed.

Also, what is happening here is not integer promotion but **integer conversion**.  Promotion happens first if any integer type in an expression has a rank less than `int`.  That is not the case here.

# integer promote

C was designed to implicitly and silently change the integer types of the operands used in expressions. There exist several cases where the language forces the compiler to either change the operands to a larger type, or to change their signedness.

The rationale behind this is to prevent accidental overflows during arithmetic, but also to allow operands with different signedness to co-exist in the same expression.

Unfortunately, the rules for implicit type promotion cause much more harm than good, to the point where they might be one of the biggest flaws in the C language. These rules are often not even known by the average C programmer and therefore causing all manner of very subtle bugs.

Typically you see scenarios where the programmer says "just cast to type x and it works" - but they don't know why. Or such bugs manifest themselves as rare, intermittent phenomenon striking from within seemingly simple and straight-forward code. Implicit promotion is particularly troublesome in code doing bit manipulations, since most bit-wise operators in C come with poorly-defined behavior when given a signed operand.

---

**Integer types and conversion rank**
-
The integer types in C are `char`, `short`, `int`, `long`, `long long` and `enum`.
`_Bool`/`bool` is also treated as an integer type when it comes to type promotions.

All integers have a specified _conversion rank_. C11 6.3.1.1, emphasis mine on the most important parts:

> Every integer type has an integer conversion rank defined as follows:
— No two signed integer types shall have the same rank, even if they have the same representation.
— The rank of a signed integer type shall be greater than the rank of any signed integer type with less precision.
**— The rank of `long long int` shall be greater than the rank of `long int`, which shall be greater than the rank of `int`, which shall be greater than the rank of `short int`, which shall be greater than the rank of `signed char`.
— The rank of any unsigned integer type shall equal the rank of the corresponding signed integer type, if any.**
— The rank of any standard integer type shall be greater than the rank of any extended integer type with the same width.
— The rank of char shall equal the rank of signed char and unsigned char.
— The rank of _Bool shall be less than the rank of all other standard integer types.
— The rank of any enumerated type shall equal the rank of the compatible integer type (see 6.7.2.2).

The types from `stdint.h` sort in here too, with the same rank as whatever type they happen to correspond to on the given system. For example, `int32_t` has the same rank as `int` on a 32 bit system.

Further, C11 6.3.1.1 specifies which types that are regarded as the _small integer types_ (not a formal term):

> The following may be used in an expression wherever an `int` or `unsigned int` may
be used:

> — An object or expression with an integer type (other than `int` or `unsigned int`) whose integer conversion rank is less than or equal to the rank of `int` and `unsigned int`.

What this somewhat cryptic text means in practice, is that `_Bool`, `char` and `short` (and also `int8_t`, `uint8_t` etc) are the "small integer types". These are treated in special ways and subject to implicit promotion, as explained below.

---

**The integer promotions**
-
Whenever a small integer type is used in an expression, it is implicitly converted to `int` which is always signed. This is known as the _integer promotions_ or _the integer promotion rule_.

Formally, the rule says (C11 6.3.1.1):

> If an `int` can represent all values of the original type (as restricted by the width, for a bit-field), the value is converted to an `int`; otherwise, it is converted to an `unsigned int`. These are called the _integer promotions_.

This text is often misunderstood as: "all small, signed integer types are converted to signed int and all small, unsigned integer types are converted to unsigned int". This is incorrect. The unsigned part here only means that if we have for example an `unsigned short` operand, and `int` happens to have the same size as `short` on the given system, then the `unsigned short` operand is converted to `unsigned int`. As in, nothing of note really happens. But in case `short` is a smaller type than `int`, it is always converted to (signed) `int`, _regardless of it the short was signed or unsigned_!


The harsh reality caused by the integer promotions means that almost no operation in C can be carried out on small types like `char` or `short`. Operations are always carried out on `int` or larger types.

This might sound like nonsense, but luckily the compiler is allowed optimize the code. For example, an expression containing two `unsigned char` operands would get the operands promoted to `int` and the operation carried out as `int`. But the compiler is allowed optimize the expression to actually get carried out as an 8 bit operation, as would be expected. However, here comes the problem: the compiler is _not_ allowed to optimize out the implicit change of signedness caused by the integer promotion. Because there is no way for the compiler to tell if the programmer is purposely relying on implicit promotion to happen, or if it is unintentional.

This is why example 1 in the question fails. Both unsigned char operands are promoted to type `int`, the operation is carried out on type `int`, and the result of `x - y` is of type `int`. Meaning that we get `-1` instead of `255` which might have been expected. The compiler may generate machine code that executes the code with 8 bit instructions instead of `int`, but it may not optimize out the change of signedness. Meaning that we end up with a negative result, that in turn results in a weird number when `printf("%u` is invoked. Example 1 could be fixed by casting the result of the operation back to type `unsigned char`.

With the exception of a few special cases like `++` and `sizeof` operators, the integer promotions apply to almost all operations in C, no matter if unary, binary (or ternary) operators are used.

---

**The usual arithmetic conversions**
-

Whenever a binary operation (an operation with 2 operands) is done in C, both operands of the operator has to be of the same type. Therefore, in case the operands are of different types, C enforces an implicit conversion of one operand to the type of the other operand. The rules for how this is done are named _the usual artihmetic conversions_ (sometimes informally referred to as "balancing"). These are specified in C11 6.3.18:

(Think of this rule as a long, nested `if-else if` statement and it might be easier to read :) )

> 6.3.1.8 Usual arithmetic conversions

> Many operators that expect operands of arithmetic type cause conversions and yield result
types in a similar way. The purpose is to determine a common real type for the operands
and result. For the specified operands, each operand is converted, without change of type
domain, to a type whose corresponding real type is the common real type. Unless
explicitly stated otherwise, the common real type is also the corresponding real type of
the result, whose type domain is the type domain of the operands if they are the same,
and complex otherwise. This pattern is called _the usual arithmetic conversions_:

> - First, if the corresponding real type of either operand is `long double`, the other operand is converted, without change of type domain, to a type whose corresponding real type is `long double`.
- Otherwise, if the corresponding real type of either operand is `double`, the other operand is converted, without change of type domain, to a type whose corresponding real type is `double`.
- Otherwise, if the corresponding real type of either operand is `float`, the other operand is converted, without change of type domain, to a type whose corresponding real type is float.
- Otherwise, the integer promotions are performed on both operands. Then the
following rules are applied to the promoted operands:

>  - If both operands have the same type, then no further conversion is needed.
  - Otherwise, if both operands have signed integer types or both have unsigned
integer types, the operand with the type of lesser integer conversion rank is
converted to the type of the operand with greater rank.
  - Otherwise, if the operand that has unsigned integer type has rank greater or
equal to the rank of the type of the other operand, then the operand with
signed integer type is converted to the type of the operand with unsigned
integer type.
  - Otherwise, if the type of the operand with signed integer type can represent
all of the values of the type of the operand with unsigned integer type, then
the operand with unsigned integer type is converted to the type of the
operand with signed integer type.
  - Otherwise, both operands are converted to the unsigned integer type
corresponding to the type of the operand with signed integer type.

Notable here is that the usual arithmetic conversions apply to both floating point and integer variables. In case of integers, we can also note that the integer promotions are invoked from within the usual arithmetic conversions. And after that, when both operands have at least the rank of `int`, the operators are balanced to the same type, with the same signedness.

This is the reason why `a + b` in example 2 gives a strange result. Both operands are integers and they are at least of rank `int`, so the integer promotions do not apply. The operands are not of the same type - `a` is `unsigned int` and `b` is `signed int`. Therefore the operator `b` is temporarily converted to type `unsigned int`. During this conversion it loses the sign information and ends up as a large value.

The reason why changing type to `short` in example 3 fixes the problem, is because `short` is a small integer type. Meaning that both operands are integer promoted to type `int` which is signed. After integer promotion, both operands have the same type (`int`), no further conversion is needed. And then the operation can be carried out on a signed type as expected.
