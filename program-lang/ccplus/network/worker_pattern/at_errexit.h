#ifndef __AT_ERREXIT_H__SYMBOL
#define __AT_ERREXIT_H__SYMBOL

//#include <stdbool.h>
#define true  1
#define false 0

int at_errexit(const char* format, ...);
void at_echo(const char* format, ...);
void at_warn(const char* format, ...);

#endif
