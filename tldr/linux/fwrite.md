# fwrite: fread signal interrupt

> Description.
> [More information](https://url-to-upstream.tld).

# Interrupts

Interrupts can occur during the fread() and fwrite() functions (and during the read() and write()
system calls — there's no way to stop that. However, it is not so clear what happens if an
interrupt occurs — whether the signal is delivered or not. It depends on how your application
(thread?) is set up to handle interrupts.

* If it ignores them, then there'll be no effect on fread() or fwrite().
* If it has default handling, the program will stop; the functions will not return.
* If your signal handler exits or use siglongjmp() (or longjmp()), then the system call won't return.
* If your handler returns, it will depend on what you specified to sigaction() when you set up the handler.
  - SA_RESTART means that the underlying read or write will be retried
  - No SA_RESTART will mean that the read or write will terminate — possibly with a short read or write, or possibly with an error and errno set to EINTR.
  - If the system call indicates failure, it is probable that fread() and fwrite() will report failure too if no data was read or written before the interrupt occurred.
  - If some data was read or written, you'll probably get the short read or write response.
