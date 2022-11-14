/** https://stackoverflow.com/questions/4306186/structure-padding-and-packing
  Memory align & padding - for struct.
  compile: gcc memory_align.c
  execute: ./a.out

1. Member alignment,
    Before each individual member, there will be padding so that to make it start at an address that is divisible by its size.
    e.g on 64 bit system,int should start at address divisible by 4, and long by 8, short by 2.
2. char alignment,
    char and char[] are special, could be any memory address, so they don't need padding before them.
3. struct alignment,
    For struct, other than the alignment need for each individual member, the size of whole struct itself will be aligned to a size divisible by size of largest individual member, by padding at end.
    e.g if struct's largest member is long then divisible by 8, int then by 4, short then by 2.

 */
#include <stdio.h>

enum em_test_type {
	em_test_a,
	em_test_b,
};

struct stu_A {
	//enum em_test_type t1;
	char *n;
	short t1;
	char a;
};

// size is 8, 4 + 1, then round to multiple of 4 (int's size),
struct stu_a {
	int i;
	char c;
};

// size is 16, 8 + 1, then round to multiple of 8 (long's size),
struct stu_b {
	long l;
	char c;
};

// size is 24, l need padding by 4 before it, then round to multiple of 8 (long's size),
struct stu_c {
	int i;
	long l;
	char c;
};

// size is 16, 8 + 4 + 1, then round to multiple of 8 (long's size),
struct stu_d {
	long l;
	int i;
	char c;
};

// size is 16, 8 + 4 + 1, then round to multiple of 8 (double's size),
struct stu_e {
	double d;
	int i;
	char c;
};

// size is 24, d need align to 8, then round to multiple of 8 (double's size),
struct stu_f {
	int i;
	double d;
	char c;
};

// size is 4,
struct stu_g {
	int i;
};

// size is 8,
struct stu_h {
	long l;
};

// test - padding within a single struct,
int test_struct_padding()
{
	printf("%s: %ld\n", "stu_a", sizeof(struct stu_a));
	printf("%s: %ld\n", "stu_b", sizeof(struct stu_b));
	printf("%s: %ld\n", "stu_c", sizeof(struct stu_c));
	printf("%s: %ld\n", "stu_d", sizeof(struct stu_d));
	printf("%s: %ld\n", "stu_e", sizeof(struct stu_e));
	printf("%s: %ld\n", "stu_f", sizeof(struct stu_f));

	printf("%s: %ld\n", "stu_g", sizeof(struct stu_g));
	printf("%s: %ld\n", "stu_h", sizeof(struct stu_h));

	return 0;
}

// test - address of struct,
int test_struct_address()
{
	printf("%s: %ld\n", "stu_A", sizeof(struct stu_A));
	printf("%s: %ld\n", "stu_g", sizeof(struct stu_g));
	printf("%s: %ld\n", "stu_h", sizeof(struct stu_h));
	printf("%s: %ld\n", "stu_f", sizeof(struct stu_f));

	struct stu_A A;
	struct stu_g g;
	struct stu_h h;
	struct stu_f f1;
	struct stu_f f2;
	int x = 1;
	long y = 1;

	printf("address of %s[%ld]: %p\n", "A", sizeof(A), &A);
	printf("address of %s: %p\n", "A.t1", &A.t1);
	printf("address of %s: %p\n", "A.a", &A.a);

	printf("address of %s: %p\n", "g", &g);
	printf("address of %s: %p\n", "h", &h);
	printf("address of %s: %p\n", "f1", &f1);
	printf("address of %s: %p\n", "f2", &f2);
	printf("address of %s: %p\n", "x", &x);
	printf("address of %s: %p\n", "y", &y);

	// g is only 4 bytes itself, but distance to next struct is 16 bytes(on 64 bit system) or 8 bytes(on 32 bit system),
	printf("space between %s and %s: %ld\n", "g", "h", (long)(&h) - (long)(&g));

	// h is only 8 bytes itself, but distance to next struct is 16 bytes(on 64 bit system) or 8 bytes(on 32 bit system),
	printf("space between %s and %s: %ld\n", "h", "f1", (long)(&f1) - (long)(&h));

	// f1 is only 24 bytes itself, but distance to next struct is 32 bytes(on 64 bit system) or 24 bytes(on 32 bit system),
	printf("space between %s and %s: %ld\n", "f1", "f2", (long)(&f2) - (long)(&f1));

	// x is not a struct, and it reuse those empty space between struts, which exists due to padding, e.g between g & h,
	printf("space between %s and %s: %ld\n", "x", "f2", (long)(&x) - (long)(&f2));
	printf("space between %s and %s: %ld\n", "g", "x", (long)(&x) - (long)(&g));

	// y is not a struct, and it reuse those empty space between struts, which exists due to padding, e.g between h & f1,
	printf("space between %s and %s: %ld\n", "x", "y", (long)(&y) - (long)(&x));
	printf("space between %s and %s: %ld\n", "h", "y", (long)(&y) - (long)(&h));

	return 0;
}

int main(int argc, char * argv[])
{
	test_struct_padding();
	test_struct_address();

	return 0;
}
