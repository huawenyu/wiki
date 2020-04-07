/** @ref https://github.com/lemire/cbitset/blob/master/src/bitset.c
 */
#include <stdio.h>
#include "bits.h"

const int ELEM_BITS = sizeof(((bitset_t *)0)->data[0]) * 8;

bitset_t *bitset_alloc (int sz)
{
	int elem_num = (sz + ELEM_BITS - 1) / ELEM_BITS;
	bitset_t *bits =  malloc (sizeof (bitset_t) + elem_num);
	if (bits) {
		bits->sz = sz;
		for (int pos = 0; pos < elem_num; pos++)
			bits->data[pos] = 0;
	}
	return bits;
}

void bitset_free (bitset_t *bits)
{
	free (bits);
}

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

void bitset_set (bitset_t *bits, int pos)
{
	if (pos < bits->sz)
		bits->data[pos / ELEM_BITS] |= (1 << (pos % ELEM_BITS));
}

void bitset_clear (bitset_t *bits, int pos)
{
	if (pos < bits->sz)
		bits->data[pos / ELEM_BITS] &= (~(1 << (pos % ELEM_BITS)));
}

void bitset_toggle (bitset_t *bits, int pos)
{
	if (pos < bits->sz)
		bits->data[pos / ELEM_BITS] ^= (1 << (pos % ELEM_BITS));
}

int bitset_test (bitset_t *bits, int pos)
{
	if (pos < bits->sz)
		return ((bits->data[pos / ELEM_BITS] & (1 << (pos % ELEM_BITS))) == 0) ? 0 : 1;
	return 0;
}

