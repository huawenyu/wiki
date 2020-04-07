#include <stdio.h>
#include "bits.h"

void bitset_dump (char *desc, bitset_t *bits)
{
    printf ("%-20.20s:\t", desc);
    for (int pos = 0; pos < (bits->sz + 32) / 32; pos++)
        printf (" $%02x", bits->data[pos]);
    printf (":\t");
    for (int pos = 0; pos < bits->sz; pos++) {
        if ((pos % 8) == 0)
            putchar (' ');
        printf ("%d", bitset_test(bits, pos));
    }
    for (int pos = bits->sz; (pos % 8) != 0; pos++)
        putchar ('_');
    putchar ('\n');
}

#define SZ 40

int main (void)
{
    bitset_t *bits = bitset_alloc(SZ);
    if (bits == NULL) {
        puts ("Could not allocate bitset");
        return 1;
    }

    bitset_dump ("Initial         ", bits);

    for (int pos = 0; pos < SZ; pos++) bitset_set(bits, pos);
    bitset_dump ("Set all         ", bits);

    for (int pos = 1; pos < SZ; pos += 2) bitset_clear (bits, pos);
    bitset_dump ("Clear every two ", bits);

    for (int pos = 0; pos < SZ; pos++) bitset_toggle (bits, pos);
    bitset_dump ("Toggle all      ", bits);

    for (int pos = 1; pos < SZ; pos += 2) bitset_clear (bits, pos);
    bitset_dump ("Clear every two ", bits);

    for (int pos = 4; pos < SZ; pos += 5) bitset_set (bits, pos);
    bitset_dump ("Set every five  ", bits);

    for (int pos = 0; pos < SZ; pos++) bitset_toggle (bits, pos);
    bitset_dump ("Toggle all      ", bits);

    for (int pos = 0; pos < SZ; pos += 2) bitset_clear (bits, pos);
    bitset_dump ("Clear odd       ", bits);

    for (int pos = 1; pos < SZ; pos += 2) bitset_clear (bits, pos);
    bitset_dump ("Clear even      ", bits);

    bitset_free (bits);

    return 0;
}

