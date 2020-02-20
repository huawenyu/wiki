# ferror

```c
#include <string.h>
#include <stdio.h>

void check_error(void)
{
	FILE *fp;
	char c;

	fp = fopen("file.txt", "w");

	c = fgetc(fp);
	if( ferror(fp) ) {
		printf("Error in reading from file : file.txt\n");
	}
	clearerr(fp);

	if( ferror(fp) ) {
		printf("Error in reading from file : file.txt\n");
	}
	fclose(fp);
}

//[Ref](https://beej.us/guide/bgc/html/multi/feof.html)
// read binary data, checking for eof or error
int safe_read(void)
{
    int a;
    FILE *fp;

    fp = fopen("binaryints.dat", "rb");

    // read single ints at a time, stopping on EOF or error:

    while(fread(&a, sizeof(int), 1, fp), !feof(fp) && !ferror(fp)) {
        printf("I read %d\n", a);
    }

    if (feof(fp))
        printf("End of file was reached.\n");

    if (ferror(fp))
        printf("An error occurred.\n");

    fclose(fp);
}

int main(void)
{
    safe_read();
    check_error();
    return 0;
}

```

