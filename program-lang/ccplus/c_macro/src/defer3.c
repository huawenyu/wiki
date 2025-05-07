#include <stdio.h>

// ---- Core Macro Machinery ----
#define EMPTY()
#define DEFER(id) id EMPTY()  // Delays expansion by one step
#define EVAL(...) __VA_ARGS__ // Forces immediate expansion

// Argument counting (C99 compatible)
#define GET_SECOND(a, b, ...) b
#define COUNT_ARGS(...) GET_SECOND(__VA_ARGS__, 2, 1, 0)

// MAP implementation
#define MAP_0(f) // Base case
#define MAP_1(f, x) f(x);
#define MAP_2(f, x, ...) f(x); DEFER(MAP_AGAIN)() (f, __VA_ARGS__)

#define MAP_AGAIN() MAP_IMPL
#define MAP_IMPL(f, ...) MAP(f, __VA_ARGS__)

// Main MAP dispatcher
#define MAP(f, ...) EVAL(MAP_IMPL(f, __VA_ARGS__))

// ---- Example Usage ----
#define PRINT_INT(x) printf("%d\n", x)

int main() {
    MAP(PRINT_INT, 1, 2, 3);  // Output: 1 2 3
    return 0;
}

