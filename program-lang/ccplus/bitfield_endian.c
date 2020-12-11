/** http://mjfrazer.org/mjfrazer/bitfields/
 *
 * Usage: gcc -O0 bitfield_endian.c -o t
 *
 Just to nitpick, endianness is about byte order, not bit order.
   Most significant bit is always on the left in a byte, regardless of endianness.

  - Big endian machines pack bitfields from most significant byte to least.
  - Little endian machines pack bitfields from least significant byte to most.
  So the endian have relation to:
    - struct member: short/int/..., which have several bytes, and how to order the bytes
    - struct member: bitfields
    - not the whole struct
    - not the char array
    - not array

   When we read hexidecimal numbers ourselves, we read them from most significant byte to
   least. So reading big endian memory dumps is easer than reading little endian. When it comes
   to reading memory dumps of bitfields, it is even harder than reading integers.
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>

// Let us start initialize as [0]=0x12, [1]=0x34, and discuss under Linux,
// Linux is Litten-endian, and the network is Big-endian
union un_bitfield1
{
	unsigned char bytes[2];  // Let us start initialize as [0]=0x12, [1]=0x34; array have no relation with endian,
	                         // physical bits byte-0: 1-0001, 2-0010
				 // physical bits byte-1: 3-0011, 4-0100
	unsigned short value;    // endian related to the value of different byte-order in the uint16_t,
	struct {
		// always bytes-0, but endian related to a/b
		unsigned short a : 4;  // 2-0010, the LSB least-significant-bits put first
		unsigned short b : 4;  // 1-0001
		// always bytes-1, but endian related to c/d
		unsigned short c : 4;  // 4-0100
		unsigned short d : 4;  // 3-0011
	} field;

	struct {
		uint8_t a;  // always bytes-0, 18=0x12
		uint8_t b;  // always bytes-1, 52=0x34
	} byte;

	struct {
		// always bytes-0, but endian related to the bits-order
		// the LSB least-significant-field put first, a0-7 shoud be 0x12,
		// and the least-significant-field is a7, which should be the 1st bit of 0x12
		// 0x12: 0001-0010, and reverse it like: 0100-1000, is also the value of a0-7
		uint8_t a0 : 1;
		uint8_t a1 : 1;
		uint8_t a2 : 1;
		uint8_t a3 : 1;
		uint8_t a4 : 1;
		uint8_t a5 : 1;
		uint8_t a6 : 1;
		uint8_t a7 : 1;
		// always bytes-1, but endian related to the bits-order
		// 0x34: 0011-0100, and reverse it like: 0010-1100, is also the value of b0-7
		uint8_t b0 : 1;
		uint8_t b1 : 1;
		uint8_t b2 : 1;
		uint8_t b3 : 1;
		uint8_t b4 : 1;
		uint8_t b5 : 1;
		uint8_t b6 : 1;
		uint8_t b7 : 1;
	} bit;
};

union un_bitfield2 {
	unsigned char bytes[2];
	unsigned short value;

	// case-1.
	//     0x92: 1001-0010, 0x34: 0011-0100
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  1 0 0 1 0 0 1 0 0 0  1  1  0  1  0  0
	//   Assign-to-short: byte-0 as lower byte, reverse two bytes as 0x34-0x92
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  0 0 1 1 0 1 0 0 1 0  0  1  0  0  1  0
	//
	// case-2.
	//     0x1D: 0001-1101, 0x15: 0001-0101
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  1 0 1 0 1 0 1 1 0 0  0  1  1  0  0  1
	//   Assign-to-short: byte-0 as lower byte, reverse two bytes as 0x15-0x1D
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  0 0 0 1 0 1 0 1 0 0  0  1  1  1  0  1
	//
	// case-3.
	//     0x67: 1010-1011, 0x19: 0001-1001
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  1 0 1 0 1 0 1 1 0 0  0  1  1  0  0  1
	//   Assign-to-short: byte-0 as lower byte, reverse two bytes as 0x19-0x67
	//     index:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	//     phy-bits:  0 0 0 1 1 0 0 1 0 1  1  0  0  1  1  1
	struct {
		//** all offset() = 0
		//            case: 1  2  3
		uint16_t a : 1; //  0  1  1 the last bit:            15-bit    0
		uint16_t b : 2; //  1  2  3 continue last 2-bits: 13,14-bits   1
		uint16_t c : 3; //  2  3  4 continue last 3-bits:              10
		uint16_t d : 4; //  2  4  5 continue last 4-bits:              10
		uint16_t e : 5; // 13  5  6                                  1101
		uint16_t   : 1; //  0                                    0
	} field;

	struct { // only need 15-bits, should be index[0:14]
		// byte-0, offset(a) = 0
		uint8_t a : 1; //  0 the last bit of byte-0:   7-bit    0
		uint8_t b : 2; //  1  2-bits:                  5,6      01
		uint8_t c : 3; //  2  3-bits:                  2,3,4    010
		uint8_t   : 2; //  2  3-bits:                  0,1      10
		// byte-1, offset(d) = 1
		uint8_t d : 4; //  4 continue last 4-bits:              0100
		uint8_t   : 4; //  4 continue last 4-bits:              0011
		// byte-2 (since the whole union int allign as 4bits
		uint8_t e : 5; //  0                                    00000
	} field2;
};

union un_bitfield3 {
	unsigned char bytes[2];
	unsigned short value;

	struct {
	#ifdef LITTLE_ENDIAN
		uint16_t dir : 1;
		uint16_t reg : 5;
		uint16_t val : 8;
		uint16_t     : 1;
	#else
		uint16_t     : 1;
		uint16_t val : 8;
		uint16_t reg : 5;
		uint16_t dir : 1;
	#endif
	} field;
};

int main ()
{
	union un_bitfield1 bits;

	bits.bytes[0] = 0x12;
	bits.bytes[1] = 0x34;
	printf("0x%x 0x%x"
	       "\n a=%d b=%d c=%d d=%d"
	       "\n a=%d b=%d"
	       "\n a0=%d%d%d%d-%d%d%d%d"
	       "\n b0=%d%d%d%d-%d%d%d%d"
	       "\n value=0x%x\n",
	       bits.bytes[0], bits.bytes[1],
	       bits.field.a, bits.field.b, bits.field.c, bits.field.d,
	       bits.byte.a, bits.byte.b,
	       bits.bit.a0, bits.bit.a1, bits.bit.a2, bits.bit.a3, bits.bit.a4, bits.bit.a5, bits.bit.a6, bits.bit.a7,
	       bits.bit.b0, bits.bit.b1, bits.bit.b2, bits.bit.b3, bits.bit.b4, bits.bit.b5, bits.bit.b6, bits.bit.b7,
	       bits.value);

	union un_bitfield2 bits2;
	// case-1:
	bits2.bytes[0] = 0x92; bits2.bytes[1] = 0x34;
	// case-2:
	//bits2.field.a = 1; bits2.field.b = 2; bits2.field.c = 3; bits2.field.d = 4; bits2.field.e = 5;
	// case-3:
	//bits2.field.a = 1; bits2.field.b = 3; bits2.field.c = 4; bits2.field.d = 5; bits2.field.e = 6;
	printf("0x%x 0x%x"
	       "\n a=%d b=%d c=%d d=%d e=%d"
	       "\n value=0x%x\n",
	       bits2.bytes[0], bits2.bytes[1],
	       bits2.field.a, bits2.field.b, bits2.field.c, bits2.field.d, bits2.field.e,
	       bits2.value);

	return(0);
}


