# QuickStart

## Samples

编译程序的时候打开调试模式（gcc编译器的-g选项）
当检查的是C++程序的时候，还应该考虑另一个选项 -fno-inline。它使得函数调用链很清晰。
最好不要使用编译优化选项(比如-O0)
如果程序是通过脚本启动的，可以修改脚本里启动程序的代码，或者使用--trace-children=yes选项来运行脚本

	$ valgrind --tool=memcheck --track-origins=yes --leak-check=full --show-leak-kinds=all --verbose ../bin/test_acsm

## docs

http://valgrind.org/docs/manual/cl-manual.html
https://github.com/jess-sys/22Docs/blob/master/docs/valgrind.rst
转自：http://wenku.baidu.com/view/2583052acfc789eb172dc881.html
http://blog.dccmx.com/2011/01/callgrind/
‘让程序飞’ 的文章 http://blog.dccmx.com/tag/let-the-program-fly/ 

## Valgrind的局限

Valgrind不对静态数组(分配在栈上)进行边界检查。如果在程序中声明了一个数组:
```c
int main()
{
    char x[10];
    x[11] = 'a';
}
```

Valgrind则不会警告你，你可以把数组改为动态在堆上分配的数组，这样就可能进行边界检查了。这个方法好像有点得不偿失的感觉。

## Valgrind包含的工具

Valgrind支持很多工具, 在运行Valgrind时，你必须指明想用的工具,如果省略工具名，默认运行memcheck:
 - Memcheck
 - Addrcheck
 - Cachegrind
 - Massif
 - Helgrind
 - Callgrind

## Valgrind的参数

valgrind [options] prog-and-args [options]

常用选项，适用于所有Valgrind工具
```ini
	--tool=<name>		<<< 最常用的选项。运行 valgrind中名为toolname的工具。默认memcheck。
	-h --help	<<< 显示所有选项的帮助，包括内核和选定的工具两者。
	--version	<<< 显示valgrind内核的版本，每个工具都有各自的版本。
	-q --quiet	<<< 安静地运行，只打印错误信息。
	--verbose	<<< 更详细的信息
	--trace-children=<yes|no>	<<< 跟踪子线程? [default: no]
	--track-fds=<yes|no>		<<< 跟踪打开的文件描述？[default: no]
	--time-stamp=<yes|no>	<<< 增加时间戳到LOG信息? [default: no]
	--log-fd=<number>		<<< 输出LOG到描述符文件 [2=stderr]
	--log-file=<file>		<<< 将输出的信息写入到filename.PID的文件里，PID是运行程序的进行ID
	--log-file-exactly=<file>	<<< 输出LOG信息到 file
	--xml=yes			<<< LOG信息输出以xml格式输出，只有memcheck可用
	--num-callers=<number>	<<< show <number> callers in stack traces [12]
	--error-exitcode=<number>	<<< 如果发现错误则返回错误代码 [0=disable]
	--db-attach=<yes|no>		<<< 当出现错误，valgrind会自动启动调试器gdb。[default: no]
	--db-command=<command>	<<< 启动调试器的命令行选项[gdb -nw %f %p]

	适用于Memcheck工具的相关选项：
	--leak-check=<no|summary|full>	<<< [default: summary], 要求对leak给出详细信息? Leak是指，存在一块没有被引用的内存空间，或没有被释放的内存空间，如summary，只反馈一些总结信息，告诉你有多少个malloc，多少个free 等；如果是full将输出所有的leaks，也就是定位到某一个malloc/free。 
	--show-reachable=<yes|no>		<<< [default: no], 如果为no，只输出没有引用的内存leaks，或指向malloc返回的内存块中部某处的leaks 
```
## 1、memcheck

memcheck探测程序中内存管理存在的问题。它检查所有对内存的读/写操作，并截取所有的malloc/new/free/delete调用。常见的内存分配方式分三种：静态存储，栈上分配，堆上分配。全局变量属于静态存储，它们是在编译时就被分配了存储空间，函数内的局部变量属于栈上分配，而最灵活的内存使用方式当属堆上分配，也叫做内存动态分配了。常用的内存动态分配函数包括：malloc, alloc, realloc, new等，动态释放函数包括free, delete。

因此memcheck工具能够探测到以下问题：
 - 1）使用未初始化的内存
 - 2）读/写已经被释放的内存
 - 3）读/写内存越界
 - 4）读/写不恰当的内存栈空间
 - 5）内存泄漏
 - 6）使用malloc, free不匹配。
 - 7）src和dst的重叠
```c
	$ gcc –o test –g test.c
	$ valgrind --tool=memcheck --leak-check=full --log-file=valg.log ./test
	$ valgrind --tool=memcheck --track-origins=yes --verbose ./test

	Options:
	leak-check=full	输出内存泄漏的完整信息
	log-file=valg.log	将检查结果输出到log文件啦
```

## 2、cachegrind

cachegrind是一个cache剖析器。它模拟执行CPU中的L1, D1和L2 cache，因此它能很精确的指出代码中的cache未命中。如果你需要，它可以打印出cache未命中的次数，内存引用和发生cache未命中的每一行代码，每一个函数，每一个模块和整个程序的摘要。如果你要求更细致的信息，它可以打印出每一行机器码的未命中次数。在x86和amd64上， cachegrind通过CPUID自动探测机器的cache配置，所以在多数情况下它不再需要更多的配置信息了。

## 3、helgrind

helgrind查找多线程程序中的竞争数据。helgrind查找内存地址，那些被多于一条线程访问的内存地址，但是没有使用一致的锁就会被查出。这表示这些地址在多线程间访问的时候没有进行同步，很可能会引起很难查找的时序问题。

它主要用来检查多线程程序中出现的竞争问题。Helgrind 寻找内存中被多个线程访问，而又没有一贯加锁的区域，这些区域往往是线程之间失去同步的地方，而且会导致难以发掘的错误。Helgrind实现了名为”Eraser” 的竞争检测算法，并做了进一步改进，减少了报告错误的次数。

## 4、Callgrind

Callgrind收集程序运行时的一些数据，函数调用关系等信息，还可以有选择地进行cache 模拟。在运行结束时，它会把分析数据写入一个文件。callgrind_annotate可以把这个文件的内容转化成可读的形式。

```sh
	### valgrind --tool=callgrind [callgrind options] your-program [program options]
	$ callgrind_control -b	<<< While the simulation is running, you can observe the execution
	$ callgrind_control -e -b	<<< This will print out the current backtrace. To annotate the backtrace with event counts
	$ callgrind_annotate [options] callgrind.out.<pid>	<<< To generate a function-by-function summary from the profile data file

	$ valgrind --tool=callgrind ./sec_infod		<<<在当前目录下生成callgrind.out.[pid],, 可以
	$ killall callgrind				<<<结束程序
	$ callgrind_annotate --auto=yes callgrind.out.[pid] > log	<<< 分析生成的日志，或者使用图形前端kcachegrind打开callgrind.out.[pid]
	$ vi log
	4.1 Same-tools: linux gprof
	linux下常用的性能工具就是跟gcc一起的gprof：找出这个程序运行时cpu都用来干什么了。
	$ gcc -g -pg test.c -o test	<<< 启用gprof，gcc编译的时候带上-pg参数
	$ ./test				<<< 生成gprof的日志文件gmon.out，记录了程序运行cpu的使用信息。：
	$ gprof ./test gmon.out > report.txt		<<< 分析生成文件，生成报表（其实是图）工具：gprof2dot
	两张表：
	1.每个函数占用cpu的时间以及百分比了  
	2.函数相互调用关系
	$ gprof2dot report.txt > test.dot	<<< 将报表转化为dot文件（graphviz http://www.graphviz.org/图像文件格式）
	$ dot -Tpng -o test.png		<<< 将这个文件再转为png格式
```
## 5、Massif

堆栈分析器，它能测量程序在堆栈中使用了多少内存，告诉我们堆块，堆管理块和栈的大小。Massif能帮助我们减少内存的使用，在带有虚拟内存的现代系统中，它还能够加速我们程序的运行，减少程序停留在交换区中的几率。
```sh
	$ g++ –o test –g test.cpp
	$ valgrind --tool=massif ./test		<<< 生成massif.out.****, massif工作的时候会每隔一定时间对程序的内存使用取个快照
	$ ms_print massif.out.*** >massif.log	<<< 分析生成文件，或者 massif-visualizer 图形前端
```

## 6、lackey

lackey是一个示例程序，以其为模版可以创建你自己的工具。在程序结束后，它打印出一些基本的关于程序执行统计数据。

# Valgrind `memcheck` sample

## 1．Use uninitial memory

```c
	#include <stdio.h>

	int main()
	{
		int x;
		if(x == 0)
		{
			printf("X is zero");
		}
		return 0;
	}

	==14222== Conditional jump or move depends on uninitialised value(s)
	==14222== at 0x400484: main (sample2.c:6)
	X is zero==14222==
	==14222== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 5 from 1)
	==14222== malloc/free: in use at exit: 0 bytes in 0 blocks.
	==14222== malloc/free: 0 allocs, 0 frees, 0 bytes allocated.
	==14222== For counts of detected errors, rerun with: -v
	==14222== All heap blocks were freed -- no leaks are possible.
```


## 2．src overlap with dst

```c
	#include <stdlib.h>
	#include <stdio.h>
	#include <string.h>

	int main(int argc,char *argv[])
	{ 
		char x[50];
		int i;
		for(i=0;i<50;i++)
		{x[i]=i;}
		strncpy(x+20,x,20); //Good
		strncpy(x+20,x,21); //Overlap
		x[39]=’’;
		strcpy(x,x+20); //Good
		x[39]=40;
		x[40]=’’;
		strcpy(x,x+20); //Overlap
		return 0;
	}

	==24139== Source and destination overlap in strncpy(0x7FEFFFC09, 0x7FEFFFBF5, 21)
	==24139== at 0x4A0724F: strncpy (mc_replace_strmem.c:116)
	==24139== by 0x400527: main (sample3.c:10)
	==24139==
	==24139== Source and destination overlap in strcpy(0x7FEFFFBE0, 0x7FEFFFBF4)
	==24139== at 0x4A06E47: strcpy (mc_replace_strmem.c:106)
	==24139== by 0x400555: main (sample3.c:15)
	==24139==
	==24139== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 5 from 1)
	==24139== malloc/free: in use at exit: 0 bytes in 0 blocks.
	==24139== malloc/free: 0 allocs, 0 frees, 0 bytes allocated.
	==24139== For counts of detected errors, rerun with: -v
	==24139== All heap blocks were freed -- no leaks are possible.
```

## 3. mismatched malloc/free, new/delete

- 申请和释放不一致
- 申请和释放不匹配
- 释放后仍然读写

```c
	#include <stdlib.h>
	#include <stdio.h>

	int main(int argc,char *argv[])
	{ 
		char *p=(char*)malloc(10);
		char *pt=p;
		int i;
		for(i=0;i<10;i++)
		{p[i]=’z’;}
		delete p;
		p[1]=’a’;
		free(pt);
		return 0;
	}


	==25811== Mismatched free() / delete / delete []
	==25811== at 0x4A05130: operator delete(void*) (vg_replace_malloc.c:244)
	==25811== by 0x400654: main (sample4.c:9)
	==25811== Address 0x4C2F030 is 0 bytes inside a block of size 10 alloc'd
	==25811== at 0x4A05809: malloc (vg_replace_malloc.c:149)
	==25811== by 0x400620: main (sample4.c:4)
	==25811==
	==25811== Invalid write of size 1
	==25811== at 0x40065D: main (sample4.c:10)
	==25811== Address 0x4C2F031 is 1 bytes inside a block of size 10 free'd
	==25811== at 0x4A05130: operator delete(void*) (vg_replace_malloc.c:244)
	==25811== by 0x400654: main (sample4.c:9)
	==25811==
	==25811== Invalid free() / delete / delete[]
	==25811== at 0x4A0541E: free (vg_replace_malloc.c:233)
	==25811== by 0x400668: main (sample4.c:11)
	==25811== Address 0x4C2F030 is 0 bytes inside a block of size 10 free'd
	==25811== at 0x4A05130: operator delete(void*) (vg_replace_malloc.c:244)
	==25811== by 0x400654: main (sample4.c:9)
	==25811==
	==25811== ERROR SUMMARY: 3 errors from 3 contexts (suppressed: 5 from 1)
	==25811== malloc/free: in use at exit: 0 bytes in 0 blocks.
	==25811== malloc/free: 1 allocs, 2 frees, 10 bytes allocated.
	==25811== For counts of detected errors, rerun with: -v
	==25811== All heap blocks were freed -- no leaks are possible.
```

## 4. Memory Leak

```c
	#include <stdlib.h>

	int main()
	{
		char *x = (char*)malloc(20);
		char *y = (char*)malloc(20);
		x=y;
		free(x);
		free(y);
		return 0;
	}

	==19013== Invalid free() / delete / delete[]
	==19013== at 0x4A0541E: free (vg_replace_malloc.c:233)
	==19013== by 0x4004F5: main (sample5.c:8)
	==19013== Address 0x4C2E078 is 0 bytes inside a block of size 20 free'd
	==19013== at 0x4A0541E: free (vg_replace_malloc.c:233)
	==19013== by 0x4004EC: main (sample5.c:7)
	==19013==
	==19013== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 5 from 1)
	==19013== malloc/free: in use at exit: 20 bytes in 1 blocks.
	==19013== malloc/free: 2 allocs, 2 frees, 40 bytes allocated.
	==19013== For counts of detected errors, rerun with: -v
	==19013== searching for pointers to 1 not-freed blocks.
	==19013== checked 66,584 bytes.
	==19013==
	==19013== LEAK SUMMARY:
	==19013== definitely lost: 20 bytes in 1 blocks.
	==19013== possibly lost: 0 bytes in 0 blocks.
	==19013== still reachable: 0 bytes in 0 blocks.
	==19013== suppressed: 0 bytes in 0 blocks.
	==19013== Use --leak-check=full to see details of leaked memory.
```

## 5．Overwrite

```c
	#include <stdlib.h>

	int main()
	{
		char *x = malloc(10);
		x[10] = 'a';
		free(x);
		return 0;
	}


	==15262== Invalid write of size 1
	==15262== at 0x4004D6: main (sample7.c:5)
	==15262== Address 0x4C2E03A is 0 bytes after a block of size 10 alloc'd
	==15262== at 0x4A05809: malloc (vg_replace_malloc.c:149)
	==15262== by 0x4004C9: main (sample7.c:4)
	==15262==
	==15262== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 5 from 1)
	==15262== malloc/free: in use at exit: 0 bytes in 0 blocks.
	==15262== malloc/free: 1 allocs, 1 frees, 10 bytes allocated.
	==15262== For counts of detected errors, rerun with: -v
	==15262== All heap blocks were freed -- no leaks are possible.
```

## 6．double free

```c
	#include <stdlib.h>

	int main()
	{
		char *x = malloc(10);
		free(x);
		free(x);
		return 0;
	}


	==15005== Invalid free() / delete / delete[]
	==15005== at 0x4A0541E: free (vg_replace_malloc.c:233)
	==15005== by 0x4004DF: main (sample8.c:6)
	==15005== Address 0x4C2E030 is 0 bytes inside a block of size 10 free'd
	==15005== at 0x4A0541E: free (vg_replace_malloc.c:233)
	==15005== by 0x4004D6: main (sample8.c:5)
	==15005==
	==15005== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 5 from 1)
	==15005== malloc/free: in use at exit: 0 bytes in 0 blocks.
	==15005== malloc/free: 1 allocs, 2 frees, 10 bytes allocated.
	==15005== For counts of detected errors, rerun with: -v
	==15005== All heap blocks were freed -- no leaks are possible.
```

# Valgrind `massif` sample

http://valgrind.org/docs/manual/ms-manual.html
https://courses.cs.washington.edu/courses/cse326/05wi/valgrind-doc/ms_main.html
https://accu.org/index.php/journals/1884

## Massif options

Massif-specific options are:

	--heap=no
	--heap=yes [default]
		When enabled, profile heap usage in detail. Without it, the massif.pid.txt or massif.pid.html will be very short.

	--heap-admin=n [default: 8]
		The number of admin bytes per block to use. This can only be an estimate of the average, since it may vary. The allocator used by glibc requires somewhere between 4--15 bytes per block, depending on various factors. It also requires admin space for freed blocks, although Massif does not count this.

	--stacks=no
	--stacks=yes [default]
		When enabled, include stack(s) in the profile. Threaded programs can have multiple stacks.

	--depth=n [default: 3]
		Depth of call chains to present in the detailed heap information. Increasing it will give more information, but Massif will run the program more slowly, using more memory, and produce a bigger .txt/.hp file.

	--alloc-fn=name
		Specify a function that allocates memory. This is useful for functions that are wrappers to malloc(), which can fill up the context information uselessly (and give very uninformative bands on the graph). Functions specified will be ignored in contexts, i.e. treated as though they were malloc(). This option can be specified multiple times on the command line, to name multiple functions.

	--format=text [default]
	--format=html
		Produce the detailed heap information in text or HTML format. The file suffix used will be either .txt or .html.


## Install massif-visualizer

```sh
	$ sudo apt-get install massif-visualizer
```

## Sample

```sh
	$ g++ -o test -g test.cpp

	### 生成massif.out.****, massif工作的时候会每隔一定时间对程序的内存使用取个快照
	$ valgrind --tool=massif ./test		

	### 分析生成文件，或者 massif-visualizer 图形前端
	$ ms_print massif.out.*** >massif.log	
	$ massif-visualizer massif.out.*** >massif.log	
```
