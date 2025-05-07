#include "stdio.h"

// ---- Core Macro Machinery ----
#define EMPTY()
#define DEFER(id) id EMPTY()  // Delays expansion by one step
#define EVAL(...) __VA_ARGS__  // Forces immediate expansion

// ---- MAP Macro ----
// Base case: Empty list
#define MAP_END(...)
// Helper: Apply `f` to first element, then recurse
#define MAP_IMPL(f, x, ...) f(x) DEFER(MAP_AGAIN)() (f, __VA_ARGS__)
// Dispatcher: Choose between MAP_IMPL or MAP_END
#define MAP(f, ...) EVAL(MAP_IMPL(f, __VA_ARGS__, MAP_END))

// Required for recursion
#define MAP_AGAIN() MAP_IMPL

// ---- Example Usage ----
// Print an integer
#define PRINT_INT(x) printf("%d\n", x)

int main() {
    // Map PRINT_INT over 3 integers
    MAP(PRINT_INT, 1, 2, 3);

    return 0;
}
