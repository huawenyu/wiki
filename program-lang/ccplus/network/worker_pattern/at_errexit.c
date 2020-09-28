// va_list
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

// Print error information
int at_errexit(const char* format, ...)
{
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
    exit(1);
}

// Print work information
void at_echo(const char* format, ...)
{
    return;
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
}

void at_warn(const char* format, ...)
{
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
}
