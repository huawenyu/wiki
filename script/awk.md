# Doc
https://www.tutorialspoint.com/awk/awk_user_defined_functions.htm
https://github.com/freznicek/awesome-awk

## libs
https://github.com/e36freak/awk-libs
https://github.com/dubiousjim/awkenough

Unlike in many languages, there is no way to make a variable local to a { … } block in awk, but you can make a variable local to a function.
To make a variable local to a function, simply declare the variable as an argument after the actual function arguments
So except the function local variable, all the other variables are global.

## Function
```awk
!# So here the `i, ret` is local variable.
function maxelt(vec,   i, ret)
{
     for (i in vec) {
          if (ret == "" || vec[i] > ret)
               ret = vec[i]
     }
     return ret
}

# Load all fields of each record into nums.
{
     for(i = 1; i <= NF; i++)
          nums[NR, i] = $i
}

END {
     print maxelt(nums)
}
```

Given the following input:

     1 5 23 8 16
    44 3 5 2 8 26
    256 291 1396 2962 100
    -6 467 998 1101
    99385 11 0 225

the program reports (predictably) that 99,385 is the largest value in the array.

## function sample 2

So here foo()'s  i and bar()'s i is the same global variable

```awk
function bar()
{
    for (i = 0; i < 3; i++)
        print "bar's i=" i
}

function foo(j)
{
    i = j + 1
    print "foo's i=" i
    bar()
    print "foo's i=" i
}

BEGIN {
      i = 10
      print "top's i=" i
      foo(0)
      print "top's i=" i
}
```
