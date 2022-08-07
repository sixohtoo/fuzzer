// gcc -m32 -fno-stack-protector -z execstack -no-pie test_binary1.c -o test_binary1

#include <stdlib.h>
#include <stdio.h>

int main(int argc, char const *argv[])
{
	char input[64];

	printf("Gimmie some input please!!\n");

	// This binary has a simple buffer overflow vulnerbility
	gets(input);

	return 0;
}