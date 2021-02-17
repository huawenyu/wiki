// https://en.cppreference.com/w/c/language/struct_initialization
//
#include <stdio.h>
#include <stdint.h>

struct example {
	struct addr_t {
		uint32_t port;
	} addr;
	union {
		uint8_t a8[4];
		uint16_t a16[2];
	} in_u;
};



int main(void)
{
	struct example ex1 = { // start of initializer list for struct example
		{ // start of initializer list for ex.addr
			80 // initialized struct's only member
		}, // end of initializer list for ex.addr
		.in_u = { // start of initializer-list for ex.in_u
			.a8 = {127,0,0,1} // initializes first element of the union
		}
	};

	struct example ex2 = {
		.addr.port = { 80 },
		.in_u = {
			.a16 = {3,5},      // the precede init will be ingore
			.a8 = {127,0,0,1}, // union only the last initialized is valid
		},
	};
	struct example *exs[4] = {&ex1, &ex2, };

	for (int i=0; i < 4; i++) {
		if (!exs[i]) continue;
		printf("%d.%d.%d.%d\n",
		       exs[i]->in_u.a8[0],
		       exs[i]->in_u.a8[1],
		       exs[i]->in_u.a8[2],
		       exs[i]->in_u.a8[3]);
	}

	return 0;
}
