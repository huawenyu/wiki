
#define FOO_1(x)        printf("One arg: %s\n", x)
#define FOO_2(x, y)     printf("Two args: %s %s\n", x, y)
#define FOO_3(x, y, z)  printf("Three args: %s %s %s\n", x, y, z)

#define GET_FOO(_1, _2, _3, NAME, ...) NAME
#define FOO(...) GET_FOO(__VA_ARGS__, FOO_3, FOO_2, FOO_1)(__VA_ARGS__)

FOO("1")
FOO("1", "2")
FOO("1", "2", "3")

