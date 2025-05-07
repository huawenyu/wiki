#define QUOTE(name) #name
#define STR(name) QUOTE(name)

#define VERSION 2.3

// Usage:
int main() {
    printf("Direct: %s\n", QUOTE(VERSION));  // Output: "VERSION"
    printf("Expanded: %s\n", STR(VERSION));  // Output: "2.3"
    return 0;
}

