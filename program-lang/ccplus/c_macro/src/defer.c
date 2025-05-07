
#define EMPTY()
#define DEFER(m) m EMPTY()  // Prevents immediate expansion
#define EVAL(...) __VA_ARGS__  // Forces re-scan

// Recursive SUM (artificial example)
#define SUM_INDIRECT() SUM  // Points back to SUM
#define SUM(x, y) EVAL(DEFER(SUM_INDIRECT)()(x, y))  // Needs DEFER

int main() {
    int result = SUM(1, 2);  // Without DEFER, this would infinite loop
    return 0;
}


