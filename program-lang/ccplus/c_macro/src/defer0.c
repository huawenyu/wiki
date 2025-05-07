
#define EMPTY()  // Expands to nothing
#define DEFER(m) m EMPTY()
#define MY_MACRO() 123

// Without DEFER: Immediate expansion
MY_MACRO();  // Expands to 123 immediately

// With DEFER: Delayed expansion
DEFER(MY_MACRO)();  // Expands to MY_MACRO EMPTY() (), then to 123

