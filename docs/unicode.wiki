# UTF-8 vs UTF-*
https://stackoverflow.com/questions/496321/utf-8-utf-16-and-utf-32

The file maybe have prefix code to sign the order (BOM): https://en.wikipedia.org/wiki/Byte_order_mark

- UTF-8: Variable-width encoding, backwards compatible with ASCII.
    + ASCII characters (U+0000 to U+007F) take 1 byte,
    + code points U+0080 to U+07FF take 2 bytes,
    + code points U+0800 to U+FFFF take 3 bytes,
    + code points U+10000 to U+10FFFF take 4 bytes.
    + Good for English text, not so good for Asian text.
- UTF-16: Variable-width encoding.
    + Code points U+0000 to U+FFFF take 2 bytes,
    + code points U+10000 to U+10FFFF take 4 bytes.
    + Bad for English text, good for Asian text.
- UTF-32: Fixed-width encoding.
    + All code points take four bytes. An enormous memory hog, but fast to operate on. Rarely used.
