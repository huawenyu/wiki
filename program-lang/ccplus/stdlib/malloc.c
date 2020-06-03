#include <malloc.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <locale.h>


int with_other_locale (char *new_locale,
		       int (*subroutine) (char *header, struct mallinfo *old_mi, int force),
		       char *header, struct mallinfo *old_mi, int force)
{
	char *old_locale, *saved_locale;
	int ret;

	/* Get the name of the current locale.  */
	old_locale = setlocale (LC_ALL, NULL);

	/* Copy the name so it won’t be clobbered by setlocale. */
	saved_locale = strdup (old_locale);
	if (saved_locale == NULL)
		exit(1); //("Out of memory");

	/* Now change the locale and do some stuff with it. */
	//setlocale (LC_ALL, new_locale);
	setlocale (LC_NUMERIC, "");
	ret = (*subroutine) (header, old_mi, force);

	/* Restore the original locale. */
	setlocale (LC_ALL, saved_locale);
	free (saved_locale);

	return ret;
}

void* create_shared_memory(size_t size)
{
	// Our memory buffer will be readable and writable:
	int protection = PROT_READ | PROT_WRITE;

	// The buffer will be shared (meaning other processes can access it), but
	// anonymous (meaning third-party processes cannot obtain an address for it),
	// so only this process and its children will be able to use it:
	int visibility = MAP_SHARED | MAP_ANONYMOUS;

	// The remaining parameters to `mmap()` are not important for this use case,
	// but the manpage for `mmap` explains their purpose.
	return mmap(NULL, size, protection, visibility, -1, 0);
}

int is_mallinfo_changed(struct mallinfo *mi, struct mallinfo *old_mi)
{
	if (!old_mi)
		return 0;
	if (mi->arena != old_mi->arena)
		return 1;
	return 0;
}

int print_mallinfo(char *header, struct mallinfo *old_mi, int force)
{
	static int i = -1;
	static int count = 0;

	struct mallinfo mi = mallinfo();
	int is_print = 0;

	if (old_mi)
		i ++;
	if (is_mallinfo_changed(&mi, old_mi))
		count ++;
	else if (!force) {
		goto out;
	}

	is_print = 1;
	fprintf(stderr, "%s"
		   "  mallinfo: i=%d +=%d\n"
		   "  totals:\n"
		   "    - all:\t%'u\t(total taken from the system: arena+hblkhd)\n"
		   "    - used:\t%'u\t(total in use by program: uordblks+usmblks+hblkhd)\n"
		   "    - free:\t%'u\t(total free within program: fordblks+fsmblks)\n"
		   "    =================\n"
		   "    - arena:\t%'u\t(bytes from sbrk(); total space in heap, non-mmapped space)\n"
		   "    - hblkhd:\t%'u\t(bytes from mmap(); space in mmapped regions)\n"
		   "      + hblks:\t%'u\t(number of mmapped regions)\n"
		   "  the arena amount:\n"
		   "    - ordblks:\t%'u\t(number of chunks not in use, number of free chunks)\n"
		   "    - uordblks:\t%'u\t(bytes in use, ordinary blocks; total amount of space allocated by malloc, total allocated space)\n"
		   "    - fordblks:\t%'u\t(free bytes, ordinary blocks; total amount of space not in use, total free space)\n"
		   "    - usmblks:\t%'u\t(bytes in use, small blocks; maximum total allocated space, always 0, preserved for backwards compatibility)\n"
		   "    - fsmblks:\t%'u\t(free bytes, small blocks; space available in freed fastbin blocks)\n"
		   "    - keepcost:\t%'u\t(part of fordblks or fsmblks at top; size of topmost memory block, top-most, releasable (via malloc_trim) space)\n"
		   "  extra:\n"
		   "      smblks:\t%'u\t(number of fastbin blocks)\n"
		   "  end%s\n",
		   header,
		   i, count,
		   (uint32_t)mi.arena + (uint32_t)mi.hblkhd,
		   (uint32_t)mi.uordblks + (uint32_t)mi.usmblks + (uint32_t)mi.hblkhd,
		   (uint32_t)mi.fordblks + (uint32_t)mi.fsmblks,
		   (uint32_t)mi.arena,
		   (uint32_t)mi.hblkhd,
		   (uint32_t)mi.hblks,
		   (uint32_t)mi.ordblks,
		   (uint32_t)mi.uordblks,
		   (uint32_t)mi.fordblks,
		   (uint32_t)mi.usmblks,
		   (uint32_t)mi.fsmblks,
		   (uint32_t)mi.keepcost,
		   (uint32_t)mi.smblks,
		   "");

out:
	if (old_mi)
		*old_mi = mi;
	if (is_print)
		return count;
	return 0;
}

int main(void)
{
	size_t unit = 1024, size;
	size_t sum_malloc = 0;
	size_t sum_map = 0;
	void *shmem;
	uint8_t *bytes;
	struct mallinfo mi = {0};
	char header[64] = "Init ";
	int inc_cnt = 0;

	setbuf(stdout, NULL);
	print_mallinfo(header, &mi, 1);
	fprintf(stderr, "\n================================================\n");
	//getchar();

	// Turn off malloc trimming.
	//mallopt(M_TRIM_THRESHOLD, -1);

	// Turn off mmap usage.
	mallopt(M_MMAP_MAX, 0);
	//
	mallopt(M_MMAP_THRESHOLD, 4096);

	for (int i = 1; i < 4000 && inc_cnt < 10; i++) {
		int has_print = 0;

		size = unit * i;

		snprintf(header, sizeof(header), "\nAllocating %lu byte\n", size);
		bytes = (uint8_t*)malloc(size);
		if (bytes)
			memset(bytes, 0x1234, size);
		sum_malloc += size;
		//has_print = print_mallinfo(header, &mi, 0);
		has_print = with_other_locale("", print_mallinfo, header, &mi, 0);

		snprintf(header, sizeof(header), "\nAllocating %lu byte by mmap\n", size);
		shmem = create_shared_memory(size);
		if (shmem)
			memset(shmem, 0x1234, size);
		sum_map += size;
		//inc_cnt = print_mallinfo(header, NULL, has_print);
		inc_cnt = with_other_locale("", print_mallinfo, header, NULL, has_print);
	}

	snprintf(header, sizeof(header), "\nFinish as allocating %lu byte\n", size);
	//print_mallinfo(header, &mi, 1);
	with_other_locale("", print_mallinfo, header, &mi, 1);
	fprintf(stderr, "\nSum=%lu SumMalloc=%lu SumMap=%lu\n", sum_malloc+sum_map, sum_malloc, sum_map);
	return 0;
}

