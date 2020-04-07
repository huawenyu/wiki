#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>

typedef struct {
	int sz;
	uint32_t data[];
} bitset_t;

bitset_t *bitset_alloc (int sz);
void bitset_free (bitset_t *bits);
void bitset_set (bitset_t *bits, int pos);
void bitset_clear (bitset_t *bits, int pos);
void bitset_toggle (bitset_t *bits, int pos);
int bitset_test (bitset_t *bits, int pos);

