# Usage
Basic use: Using basic string format and address of variable you can easily get user input from console.

```c
char a;
int b;
float c;
double d;
char s[20];
scanf("%c %d %f %lf %s", &a, &b, &c, &d, s);
```
## `*`

The `*` in scanf: Sometimes, you may need to exclude some character or number from user input.
Suppose, the input is `30/01/2018` and you want to get day, month, year separately as integer.
You can achieve this, using `*`  in string format.

```c
int day,month,year;
scanf("%d%*c%d%*c%d", &day, &month, &year);

// Here, %c is character type specifier and %*c means one character would be read from the console but it wouldn’t be assigned to any variable. Here we excluded two “/” from the input.
// %*c would exclude one character. Remember, ‘/n’ and ‘/t’ are single characters.
// %*d would exclude one integer.
// %*f would exclude one float.
// %*s would exclude one word.
```

## `Number`

[Number](Number) in scanf: Sometimes, we need to limit the number of digit in integer or float, number of character in string.
We can achieve this by adding an integer(>0) in the string format.

```c
int a;
scanf("%5d", &a);
```

The code above, would take just first 5 digit as input. Any digits after 5th one would be ignored. If the integer has less that 5 digits, then it would be taken as it is.
%5c would take exact 5 characters as input. Remember, if you take 5 character as input and want to store in an array, then the array size must not be less than 6. This means, the extra position is reserved for a null character `\0`. Otherwise, you may face some unexpected difficulties.

%5d would take an integer of at most 5 digits.
%5f would take a float type number of at most 5 digits or 4 digits and one “ . ” as input.
%5s would take a string of at most 5 non white-space characters as input.

## `[set]`

[set] in scanf: You can achieve regular expression like flavor in scanf using [set] in string format.
This method does not work with integer or float type. Using [set], you can only take character type input.

```c
char str[100];
scanf("%[^\n]", str);
```

    %[^\n] would take all characters in a single line as input.
      You may know that, whenever we press Enter in keyboard, then “\n” character is written in the console.
      Here, “^” means up-to and “\n” means new line and finally, [^\n] means take input up-to new line.

    Similarly, %[^5] would take all characters as input up-to 5. If you write “abcde fghk5k zaq” in the console, then just “abcde fghk” would be taken as input.
    %[0–9] would take just number characters as input. If you write “1234abc567” in the console, then just first numbers “1234” would be taken as input.
    Similarly, %[a–z] would take just small letter alphabets as input. If you write “abc12ijkl” in the console, then just first small letters “abc” would be taken as input.
    %[123] would just take any combination of 1, 2, 3 as input. Anything other than 1,2,3 would be ignored. If you write “1123390123” in the console then just first “11233” would be taken as input.
    Combination of all: You can use any combination of “ * ”, number and [set] in scanf.

```c
char str[100];
scanf("%*[^:]%*2c%[^\n]", str);
```

If you write the following in the console:
Any combination: You are free to use any combination.
Then only “You are free to use any combination.” would be stored in str variable. Here,
“Any combination” this would be removed by `%*[^:]`
“: ” this, a colon and a space total two character would be removed by `%*2c`
Return Value: Another fun fact of scanf is that, it has return type of integer.
That means whenever we take input from console using scanf function, it returns an integer value which indicates, how many values are stored to the variables.

```c
int a, b, c;
c = scanf("%d %*d %d", &a, &b);
printf("%d\n", c);
```

The code above would print 2. Although three integer would be scanned from console, only 2 value would be stored in the variable.
You can use the return value in if-statement to overcome any EOF(End of File) error.

## `m`: dynamic allocation

To use the dynamic allocation conversion specifier, specify m as a length modifier (thus %ms or %m[range]).  The caller must free(3) the returned string, as in the following example:

```c
    char *p;
    int n;

    errno = 0;
    n = scanf("%m[a-z]", &p);
    if (n == 1) {
       printf("read: %s\n", p);
       free(p);
    } else if (errno != 0) {
       perror("scanf");
    } else {
       fprintf(stderr, "No matching characters\n");
    }
```

As shown in the above example, it is necessary to call free(3) only if the scanf() call successfully read a string.

